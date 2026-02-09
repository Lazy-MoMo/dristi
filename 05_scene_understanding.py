# 05_scene_understanding.py
# Dristi - Scene Understanding with CLIP
import cv2
import torch
import clip
from PIL import Image
from ultralytics import YOLO
from collections import Counter
import time

print("=" * 70)
print("🧠 DRISTI - Scene Understanding with CLIP")
print("=" * 70)

# Load models
print("\n📦 Loading AI models...")
yolo_model = YOLO('yolov8n.pt')
print("✅ YOLO loaded")

device = "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
print("✅ CLIP loaded")

# Scene type queries
scene_type_queries = [
    "an indoor room",
    "an outdoor area", 
    "a kitchen with appliances",
    "a bedroom with bed",
    "an office with desk and computer",
    "a living room with furniture",
    "a street with buildings",
    "a park with trees and grass",
    "a store or shop",
    "a bathroom"
]

# Scene condition queries
scene_condition_queries = [
    "a crowded busy place with many people",
    "a quiet empty space with few objects",
    "a well-lit bright environment",
    "a dark dimly-lit space",
    "a clean organized area",
    "a cluttered messy space"
]

# Activity queries
activity_queries = [
    "people walking or moving",
    "people sitting and resting",
    "people working at desk or computer",
    "people eating or drinking",
    "people talking or interacting",
    "no visible human activity"
]

def analyze_scene_with_clip(frame):
    """Use CLIP to understand complete scene context"""
    # Convert to PIL Image
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image_input = clip_preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
        
        # Scene type classification
        scene_type_text = clip.tokenize(scene_type_queries).to(device)
        scene_type_features = clip_model.encode_text(scene_type_text)
        scene_type_similarity = (100.0 * image_features @ scene_type_features.T).softmax(dim=-1)
        
        # Scene condition classification
        condition_text = clip.tokenize(scene_condition_queries).to(device)
        condition_features = clip_model.encode_text(condition_text)
        condition_similarity = (100.0 * image_features @ condition_features.T).softmax(dim=-1)
        
        # Activity classification
        activity_text = clip.tokenize(activity_queries).to(device)
        activity_features = clip_model.encode_text(activity_text)
        activity_similarity = (100.0 * image_features @ activity_features.T).softmax(dim=-1)
    
    # Get top predictions
    scene_values, scene_indices = scene_type_similarity[0].topk(2)
    condition_values, condition_indices = condition_similarity[0].topk(2)
    activity_values, activity_indices = activity_similarity[0].topk(1)
    
    return {
        'scene_type': scene_type_queries[scene_indices[0]],
        'scene_confidence': scene_values[0].item(),
        'scene_type_alt': scene_type_queries[scene_indices[1]],
        'condition': scene_condition_queries[condition_indices[0]],
        'condition_confidence': condition_values[0].item(),
        'activity': activity_queries[activity_indices[0]],
        'activity_confidence': activity_values[0].item()
    }

def generate_scene_description(objects, scene_info):
    """Generate natural language scene description"""
    description_parts = []
    
    # Scene type (always include if confident)
    if scene_info['scene_confidence'] > 25:
        scene = scene_info['scene_type'].replace("a ", "").replace("an ", "")
        description_parts.append(f"You are in {scene}.")
    
    # Scene condition (if confident)
    if scene_info['condition_confidence'] > 30:
        condition = scene_info['condition'].replace("a ", "").replace("an ", "")
        description_parts.append(f"It appears to be {condition}.")
    
    # Objects summary
    if objects:
        counts = Counter(objects)
        total = len(objects)
        unique = len(counts)
        
        # Priority objects for navigation
        priority_objects = ['person', 'car', 'truck', 'bus', 'bicycle', 
                           'motorcycle', 'chair', 'door', 'stairs']
        priority_detected = [obj for obj in counts if obj in priority_objects]
        
        if priority_detected:
            priority_list = []
            for obj in priority_detected[:3]:
                count = counts[obj]
                if count == 1:
                    priority_list.append(f"one {obj}")
                else:
                    priority_list.append(f"{count} {obj}s")
            description_parts.append(f"Important objects: {', '.join(priority_list)}.")
        
        # General object count
        if unique > len(priority_detected):
            other_count = total - sum(counts[obj] for obj in priority_detected)
            if other_count > 0:
                description_parts.append(f"Also {other_count} other objects present.")
    else:
        description_parts.append("No objects detected in current view.")
    
    # Activity (if confident and relevant)
    if scene_info['activity_confidence'] > 35 and "no visible" not in scene_info['activity']:
        activity = scene_info['activity']
        description_parts.append(f"Activity: {activity}.")
    
    return " ".join(description_parts)

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera error!")
    exit()

print("\n" + "=" * 70)
print("🚀 Scene Understanding Active")
print("=" * 70)
print("\n📋 Controls:")
print("   SPACE   - Analyze and describe scene")
print("   'a'     - Toggle auto-analysis (every 10 seconds)")
print("   's'     - Save screenshot with description")
print("   'q'     - Quit")
print("\n")

frame_count = 0
fps = 0
fps_start_time = time.time()
current_scene = None
auto_analyze = False
last_analysis_time = 0
analysis_interval = 10  # seconds

# Initialize variables
detected_objects = []
annotated_frame = None

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
        
        # Object detection (every 3rd frame)
        if frame_count % 3 == 0:
            results = yolo_model(frame, conf=0.5, verbose=False)
            annotated_frame = results[0].plot()
            
            # Get detected objects
            detected_objects = []
            for box in results[0].boxes:
                class_name = yolo_model.names[int(box.cls[0])]
                detected_objects.append(class_name)
        else:
            # Keep previous frame
            if annotated_frame is None:
                annotated_frame = frame.copy()
            else:
                annotated_frame = frame
        
        # Auto-analysis mode
        if auto_analyze and (current_time - last_analysis_time > analysis_interval):
            print("\n🔄 Auto-analyzing scene...")
            current_scene = analyze_scene_with_clip(frame)
            description = generate_scene_description(detected_objects, current_scene)
            
            print("\n" + "=" * 70)
            print("📊 AUTO-ANALYSIS")
            print("=" * 70)
            print(f"💬 {description}")
            print("=" * 70 + "\n")
            
            last_analysis_time = current_time
        
        # Add overlay info
        cv2.putText(annotated_frame, f"FPS: {fps:.1f} | Objects: {len(detected_objects)}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        status = "AUTO-ANALYSIS ON" if auto_analyze else "Press SPACE to analyze"
        color = (0, 255, 255) if auto_analyze else (255, 255, 255)
        cv2.putText(annotated_frame, status, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Display scene info if available
        if current_scene:
            info_y = annotated_frame.shape[0] - 120
            cv2.rectangle(annotated_frame, (0, info_y - 5), 
                        (annotated_frame.shape[1], annotated_frame.shape[0]),
                        (0, 0, 0), -1)
            
            scene_text = current_scene['scene_type'].replace("a ", "").replace("an ", "")
            cv2.putText(annotated_frame, f"Scene: {scene_text}", 
                       (10, info_y + 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            
            condition_text = current_scene['condition'].replace("a ", "").replace("an ", "")
            cv2.putText(annotated_frame, f"Condition: {condition_text}", 
                       (10, info_y + 55),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            
            activity_text = current_scene['activity']
            cv2.putText(annotated_frame, f"Activity: {activity_text}", 
                       (10, info_y + 85),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow('Dristi - Scene Understanding', annotated_frame)
        
        # Handle keyboard
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Exiting...")
            break
        
        elif key == ord(' '):  # Analyze scene
            print("\n🔍 Analyzing scene...")
            current_scene = analyze_scene_with_clip(frame)
            description = generate_scene_description(detected_objects, current_scene)
            
            print("\n" + "=" * 70)
            print("📊 SCENE ANALYSIS")
            print("=" * 70)
            print(f"\n🏠 Scene Type: {current_scene['scene_type']}")
            print(f"   Confidence: {current_scene['scene_confidence']:.1f}%")
            print(f"   Alternative: {current_scene['scene_type_alt']}")
            
            print(f"\n🌟 Condition: {current_scene['condition']}")
            print(f"   Confidence: {current_scene['condition_confidence']:.1f}%")
            
            print(f"\n🏃 Activity: {current_scene['activity']}")
            print(f"   Confidence: {current_scene['activity_confidence']:.1f}%")
            
            print(f"\n📦 Objects Detected: {len(detected_objects)}")
            if detected_objects:
                counts = Counter(detected_objects)
                for obj, count in counts.most_common(5):
                    print(f"   • {obj}: {count}")
            
            print(f"\n💬 Natural Description:")
            print(f"   {description}")
            print("=" * 70 + "\n")
            
            last_analysis_time = current_time
        
        elif key == ord('a'):  # Toggle auto-analysis
            auto_analyze = not auto_analyze
            status = "enabled" if auto_analyze else "disabled"
            print(f"\n🔄 Auto-analysis {status}")
            if auto_analyze:
                last_analysis_time = current_time
        
        elif key == ord('s'):  # Save screenshot
            filename = f"scene_analysis_{frame_count}.jpg"
            
            # Add description to image
            if current_scene:
                description = generate_scene_description(detected_objects, current_scene)
                # Create text image
                text_img = annotated_frame.copy()
                cv2.rectangle(text_img, (0, 0), (text_img.shape[1], 150), (0, 0, 0), -1)
                
                # Wrap text
                words = description.split()
                lines = []
                current_line = []
                for word in words:
                    current_line.append(word)
                    if len(' '.join(current_line)) > 80:
                        lines.append(' '.join(current_line[:-1]))
                        current_line = [word]
                lines.append(' '.join(current_line))
                
                # Draw lines
                y_offset = 30
                for line in lines[:3]:  # Max 3 lines
                    cv2.putText(text_img, line, (10, y_offset),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    y_offset += 30
                
                cv2.imwrite(filename, text_img)
            else:
                cv2.imwrite(filename, annotated_frame)
            
            print(f"📸 Saved: {filename}")

except KeyboardInterrupt:
    print("\n⚠️ Interrupted")

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Scene understanding complete!")
    print("=" * 70)