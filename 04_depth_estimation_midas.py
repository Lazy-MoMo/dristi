# 04_depth_estimation_midas.py
# Dristi - Real Depth Estimation with MiDaS + Object Detection
import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time

print("=" * 70)
print("📏 DRISTI - MiDaS Depth Estimation + Object Detection")
print("=" * 70)

# Load YOLO model
print("\n📦 Loading YOLO model...")
yolo_model = YOLO('yolov8n.pt')
print("✅ YOLO loaded")

# Load MiDaS depth estimation model
print("\n📦 Loading MiDaS depth model (this may take a minute)...")
print("⏳ Downloading model if first time...")

try:
    midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small", trust_repo=True)
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
    transform = midas_transforms.small_transform
    
    device = torch.device("cpu")
    midas.to(device)
    midas.eval()
    print("✅ MiDaS depth model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading MiDaS: {e}")
    print("\n💡 Tip: Make sure you installed timm:")
    print("   pip install timm")
    exit()

def estimate_distance_from_depth(depth_map, bbox):
    """Estimate distance category from depth map"""
    x1, y1, x2, y2 = map(int, bbox)
    
    # Ensure bbox is within frame
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(depth_map.shape[1], x2), min(depth_map.shape[0], y2)
    
    # Get region of interest
    roi = depth_map[y1:y2, x1:x2]
    
    if roi.size == 0:
        return "Unknown", 0.5, (255, 255, 255)
    
    # Get median depth (more robust than mean)
    median_depth = np.median(roi)
    
    # Normalize depth value (0-1, where 1 is closest)
    # MiDaS outputs inverse depth, so higher values = closer
    normalized_depth = median_depth
    
    # Categorize distance and assign colors
    if normalized_depth > 0.75:
        distance_text = "Very Close (< 0.5m)"
        color = (0, 0, 255)  # Red - danger!
        distance_val = 0.3
    elif normalized_depth > 0.55:
        distance_text = "Close (0.5-1m)"
        color = (0, 165, 255)  # Orange
        distance_val = 0.8
    elif normalized_depth > 0.35:
        distance_text = "Medium (1-2m)"
        color = (0, 255, 255)  # Yellow
        distance_val = 1.5
    elif normalized_depth > 0.20:
        distance_text = "Far (2-3m)"
        color = (0, 255, 0)  # Green
        distance_val = 2.5
    else:
        distance_text = "Very Far (> 3m)"
        color = (0, 200, 0)  # Dark green
        distance_val = 4.0
    
    return distance_text, distance_val, color

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera error!")
    exit()

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"✅ Camera ready! Resolution: {width}x{height}")

print("\n" + "=" * 70)
print("🚀 Starting Real-Time Depth Estimation...")
print("=" * 70)
print("\n📋 Controls:")
print("   'q'     - Quit")
print("   'd'     - Toggle depth map view")
print("   's'     - Save screenshot")
print("   'SPACE' - Describe scene with distances")
print("\n⚠️  Note: Depth processing is compute-intensive")
print("   FPS may be lower than object detection alone")
print("=" * 70 + "\n")

frame_count = 0
fps = 0
fps_start_time = time.time()
show_depth = False
detected_info = []

# Cache for depth map (update less frequently)
depth_map_normalized = None
depth_colored = None

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        current_time = time.time()
        
        # Calculate FPS
        if frame_count % 30 == 0:
            fps = 30 / (current_time - fps_start_time)
            fps_start_time = current_time
        
        # Create annotated frame
        annotated_frame = frame.copy()
        
        # Run depth estimation every 5 frames (performance optimization)
        if frame_count % 5 == 0:
            # Prepare image for MiDaS
            img_for_depth = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            input_batch = transform(img_for_depth).to(device)
            
            # Run depth estimation
            with torch.no_grad():
                prediction = midas(input_batch)
                prediction = torch.nn.functional.interpolate(
                    prediction.unsqueeze(1),
                    size=frame.shape[:2],
                    mode="bicubic",
                    align_corners=False,
                ).squeeze()
            
            depth_map = prediction.cpu().numpy()
            
            # Normalize depth map for display (0-255)
            depth_map_normalized = cv2.normalize(depth_map, None, 0, 1, 
                                                 cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            
            # Create colored depth map
            depth_map_8bit = (depth_map_normalized * 255).astype(np.uint8)
            depth_colored = cv2.applyColorMap(depth_map_8bit, cv2.COLORMAP_MAGMA)
        
        # Object detection every 3 frames
        if frame_count % 3 == 0:
            results = yolo_model(frame, conf=0.5, verbose=False)
            detections = results[0].boxes
            
            detected_info = []
            
            for box in detections:
                # Get box info
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                class_id = int(box.cls[0])
                class_name = yolo_model.names[class_id]
                confidence = float(box.conf[0])
                
                # Estimate distance from depth map
                if depth_map_normalized is not None:
                    distance_text, distance_val, color = estimate_distance_from_depth(
                        depth_map_normalized, [x1, y1, x2, y2]
                    )
                else:
                    distance_text = "Calculating..."
                    color = (255, 255, 255)
                    distance_val = 0
                
                # Draw bounding box
                cv2.rectangle(annotated_frame,
                            (int(x1), int(y1)), (int(x2), int(y2)),
                            color, 3)
                
                # Prepare labels
                label = f"{class_name} ({confidence:.2f})"
                
                # Draw label background
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                cv2.rectangle(annotated_frame,
                            (int(x1), int(y1) - 60),
                            (int(x1) + max(label_size[0], 180), int(y1)),
                            (0, 0, 0), -1)
                
                # Draw text
                cv2.putText(annotated_frame, label,
                          (int(x1) + 5, int(y1) - 38),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(annotated_frame, distance_text,
                          (int(x1) + 5, int(y1) - 12),
                          cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                
                detected_info.append({
                    'name': class_name,
                    'confidence': confidence,
                    'distance_text': distance_text,
                    'distance_val': distance_val
                })
            
            # Print detections periodically
            if frame_count % 60 == 0 and detected_info:
                print(f"\n📊 Frame {frame_count}:")
                # Sort by distance (closest first)
                sorted_info = sorted(detected_info, key=lambda x: x['distance_val'])
                for info in sorted_info:
                    print(f"   {info['name']:15s} | "
                          f"Conf: {info['confidence']*100:5.1f}% | "
                          f"{info['distance_text']}")
        
        # Add overlay info
        cv2.putText(annotated_frame, f"FPS: {fps:.1f} | Objects: {len(detected_info)}",
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, "Press 'd' for depth view",
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Distance legend
        legend_y = frame.shape[0] - 110
        cv2.rectangle(annotated_frame, (10, legend_y), (280, frame.shape[0] - 10),
                     (0, 0, 0), -1)
        cv2.putText(annotated_frame, "Distance Guide:", (15, legend_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(annotated_frame, "Red: <0.5m (Very Close)", (15, legend_y + 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
        cv2.putText(annotated_frame, "Orange: 0.5-1m (Close)", (15, legend_y + 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 165, 255), 1)
        cv2.putText(annotated_frame, "Yellow: 1-2m (Medium)", (15, legend_y + 80),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)
        cv2.putText(annotated_frame, "Green: >2m (Far)", (15, legend_y + 100),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
        
        # Show appropriate view
        if show_depth and depth_colored is not None:
            # Blend detection with depth map
            blended = cv2.addWeighted(annotated_frame, 0.5, depth_colored, 0.5, 0)
            cv2.imshow('Dristi - MiDaS Depth Estimation', blended)
        else:
            cv2.imshow('Dristi - MiDaS Depth Estimation', annotated_frame)
        
        # Handle keyboard
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Shutting down...")
            break
        
        elif key == ord('d'):
            show_depth = not show_depth
            status = "ON (blended view)" if show_depth else "OFF (detection only)"
            print(f"🔄 Depth visualization: {status}")
        
        elif key == ord('s'):
            filename = f"midas_depth_{frame_count}.jpg"
            
            # Save both views side by side
            if depth_colored is not None:
                # Resize if needed
                depth_resized = cv2.resize(depth_colored, (annotated_frame.shape[1], 
                                                          annotated_frame.shape[0]))
                combined = np.hstack([annotated_frame, depth_resized])
                cv2.imwrite(filename, combined)
            else:
                cv2.imwrite(filename, annotated_frame)
            
            print(f"📸 Saved: {filename}")
        
        elif key == ord(' '):
            # Describe scene with distances
            if detected_info:
                print("\n" + "=" * 70)
                print("🗣️  SCENE DESCRIPTION")
                print("=" * 70)
                
                # Sort by distance
                sorted_objects = sorted(detected_info, key=lambda x: x['distance_val'])
                
                # Group by distance
                very_close = [o for o in sorted_objects if "Very Close" in o['distance_text']]
                close = [o for o in sorted_objects if o['distance_text'].startswith("Close")]
                medium = [o for o in sorted_objects if "Medium" in o['distance_text']]
                far = [o for o in sorted_objects if "Far" in o['distance_text'] and "Very" not in o['distance_text']]
                
                if very_close:
                    print(f"\n⚠️  WARNING - Very close objects:")
                    for obj in very_close:
                        print(f"   • {obj['name']} right in front of you!")
                
                if close:
                    print(f"\n📍 Close by:")
                    for obj in close:
                        print(f"   • {obj['name']}")
                
                if medium:
                    print(f"\n👀 Within view:")
                    for obj in medium:
                        print(f"   • {obj['name']}")
                
                if far:
                    print(f"\n🌄 In the distance:")
                    for obj in far:
                        print(f"   • {obj['name']}")
                
                print("=" * 70 + "\n")
            else:
                print("\n📭 No objects detected in current frame\n")

except KeyboardInterrupt:
    print("\n⚠️ Interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ MiDaS depth estimation complete!")
    print(f"📊 Total frames processed: {frame_count}")
    print("=" * 70)