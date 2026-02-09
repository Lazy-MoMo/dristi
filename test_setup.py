# test_setup.py
print("=" * 50)
print("🚀 DRISTI SETUP TEST")
print("=" * 50)

# Test imports
print("\n📦 Testing imports...")

try:
    import cv2
    print("✅ OpenCV:", cv2.__version__)
except:
    print("❌ OpenCV failed")

try:
    import torch
    print("✅ PyTorch:", torch.__version__)
except:
    print("❌ PyTorch failed")

try:
    from ultralytics import YOLO
    print("✅ YOLO/Ultralytics: OK")
except:
    print("❌ YOLO failed")

try:
    import clip
    print("✅ CLIP: OK")
except:
    print("❌ CLIP failed")

try:
    import numpy as np
    print("✅ NumPy:", np.__version__)
except:
    print("❌ NumPy failed")

print("\n📷 Testing camera...")
cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("✅ Camera is accessible!")
    ret, frame = cap.read()
    if ret:
        print(f"✅ Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
    cap.release()
else:
    print("❌ Camera not accessible")

print("\n" + "=" * 50)
print("🎉 Setup test complete!")
print("=" * 50)