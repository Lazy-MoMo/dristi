# 03_object_detection.py
import cv2
from ultralytics import YOLO
import time

print("=" * 60)
print("🎯 DRISTI - Real-Time Object Detection")
print("=" * 60)

# Load YOLO model
print("\n📦 Loading YOLO model...")
model = YOLO('yolov8n.pt')
print("✅ Model loaded!")

# Open camera
print("\n📷 Opening camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not accessible!")
    exit()

print("✅ Camera ready!")

# Settings
CONFIDENCE_THRESHOLD = 0.5  # Only show detections above 50% confidence
PROCESS_EVERY_N_FRAMES = 2  # Process every 2nd frame (performance optimization)

print("\n" + "=" * 60)
print("🚀 Starting Detection...")
print("=" * 60)
print("\n📋 Controls:")
print("   - Press 'q' to quit")
print("   - Press '+' to increase confidence threshold")
print("   - Press '-' to decrease confidence threshold")
print("   - Press 's' to save screenshot")
print("\n🔍 Detecting...\n")

frame_count = 0
fps_start_time = time.time()
fps = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to grab frame")
            break
        
        frame_count += 1
        
        # Calculate FPS
        if frame_count % 30 == 0:
            fps_end_time = time.time()
            fps = 30 / (fps_end_time - fps_start_time)
            fps_start_time = fps_end_time
        
        # Run detection (only on some frames to save resources)
        if frame_count % PROCESS_EVERY_N_FRAMES == 0:
            results = model(frame, conf=CONFIDENCE_THRESHOLD, verbose=False)
            annotated_frame = results[0].plot()  # Draw boxes
            
            # Get detections
            detections = results[0].boxes
            detected_objects = []
            
            for box in detections:
                class_id = int(box.cls[0])
                class_name = model.names[class_id]
                confidence = float(box.conf[0])
                detected_objects.append((class_name, confidence))
            
            # Print detections every 30 frames (once per second approx)
            if frame_count % 30 == 0 and detected_objects:
                print(f"\n📊 Frame {frame_count} - Detected:")
                for obj, conf in detected_objects:
                    print(f"   ✓ {obj}: {conf*100:.1f}%")
        else:
            annotated_frame = frame
        
        # Add info overlay
        cv2.putText(annotated_frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"Confidence: {CONFIDENCE_THRESHOLD:.2f}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, "Press 'q' to quit", (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow('Dristi - Object Detection', annotated_frame)
        
        # Handle keyboard
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Shutting down...")
            break
        elif key == ord('+') or key == ord('='):
            CONFIDENCE_THRESHOLD = min(0.95, CONFIDENCE_THRESHOLD + 0.05)
            print(f"🔼 Confidence threshold: {CONFIDENCE_THRESHOLD:.2f}")
        elif key == ord('-') or key == ord('_'):
            CONFIDENCE_THRESHOLD = max(0.1, CONFIDENCE_THRESHOLD - 0.05)
            print(f"🔽 Confidence threshold: {CONFIDENCE_THRESHOLD:.2f}")
        elif key == ord('s'):
            filename = f"detection_{frame_count}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"📸 Saved: {filename}")

except KeyboardInterrupt:
    print("\n⚠️ Interrupted by user")

finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("\n✅ Dristi closed successfully!")
    print(f"📊 Total frames processed: {frame_count}")
    print("=" * 60)