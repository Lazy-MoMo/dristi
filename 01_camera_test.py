# 01_camera_test.py
import cv2
import sys

print("=" * 60)
print(" DRISTI - Camera Test")
print("=" * 60)

# Try to open camera
print("\n Searching for camera...")
cap = cv2.VideoCapture(1)  # 0 = default camera

if not cap.isOpened():
    print(" ERROR: Could not access camera!")
    print(" Try these fixes:")
    print("   1. Close any apps using camera (Zoom, Teams, etc.)")
    print("   2. Check camera permissions in Windows Settings")
    print("   3. Try running: cv2.VideoCapture(1) instead of 0")
    sys.exit()

print(" Camera opened successfully!")

# Get camera properties
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

print(f"\n Camera Properties:")
print(f"   Resolution: {width}x{height}")
print(f"   FPS: {fps}")

print("\n Starting live feed...")
print("   Press 'q' to quit")
print("   Press 's' to save a snapshot")

frame_count = 0

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Failed to grab frame")
        break
    
    frame_count += 1
    
    # Add text to frame
    cv2.putText(frame, f"Frame: {frame_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(frame, "Press 'q' to quit | 's' to save", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Show frame
    cv2.imshow('Dristi Camera Test', frame)
    
    # Handle keyboard input
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        print("\n👋 Quitting...")
        break
    elif key == ord('s'):
        filename = f"snapshot_{frame_count}.jpg"
        cv2.imwrite(filename, frame)
        print(f"📸 Saved: {filename}")

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("\n✅ Camera test complete!")
