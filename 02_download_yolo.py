# 02_download_yolo.py
from ultralytics import YOLO
import os

print("=" * 60)
print("📥 DRISTI - Downloading YOLO Model")
print("=" * 60)

# Create models folder
os.makedirs("data/models", exist_ok=True)

print("\n⏳ Downloading YOLOv8 nano model...")
print("   (This is ~6 MB, will take 1-2 minutes)")

# This will automatically download the model
model = YOLO('yolov8n.pt')

print("\n✅ Model downloaded successfully!")
print(f"📁 Saved to: {os.path.abspath('yolov8n.pt')}")

# Test the model on a dummy image
print("\n🧪 Testing model...")
import numpy as np

# Create a dummy image (black image)
dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)

# Run prediction
results = model(dummy_image, verbose=False)
print("✅ Model is working!")

print("\n📋 Model can detect these objects:")
print("=" * 60)
class_names = model.names
for idx, name in class_names.items():
    print(f"   {idx:2d}. {name}")

print("\n" + "=" * 60)
print("🎉 Setup complete! Ready for object detection!")
print("=" * 60)