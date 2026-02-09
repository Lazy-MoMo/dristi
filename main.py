#!/usr/bin/env python3
"""
DRISTI - Vision-based Voice Assistant for Visually Impaired Users
Main entry point to run the complete system
"""

import sys
import os

print("=" * 70)
print("🚀 DRISTI - Vision-Based Voice Assistant")
print("=" * 70)

print("\n📋 Available modules:\n")
print("1. 01_camera_test.py         - Test camera access")
print("2. 02_download_yolo.py       - Download YOLO model")
print("3. 03_object_detection.py    - Real-time object detection")
print("4. 04_depth_estimation_midas.py - Depth estimation + object detection")
print("5. 05_scene_understanding.py - Scene understanding with CLIP")
print("6. 06_voice_assistant.py     - Full voice assistant")
print("\n")

choice = input("Select which module to run (1-6) or 'all' to run all: ").strip().lower()

modules = {
    '1': '01_camera_test.py',
    '2': '02_download_yolo.py',
    '3': '03_object_detection.py',
    '4': '04_depth_estimation_midas.py',
    '5': '05_scene_understanding.py',
    '6': '06_voice_assistant.py'
}

if choice == 'all':
    print("\n🔄 Running all modules in sequence...\n")
    for i in range(1, 7):
        module = modules[str(i)]
        print(f"\n{'=' * 70}")
        print(f"Running {module}...")
        print(f"{'=' * 70}")
        os.system(f"python {module}")
        input("\nPress Enter to continue to next module...")
elif choice in modules:
    module = modules[choice]
    print(f"\n🎯 Running {module}...\n")
    os.system(f"python {module}")
else:
    print("Invalid choice!")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ DRISTI session complete!")
print("=" * 70)
