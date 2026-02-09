#!/usr/bin/env python3
"""
DRISTI - Integrated Vision Assistant
Complete application combining all modules
"""
import os
import sys

# Disable OpenCV GUI if no display available
if not os.getenv('DISPLAY') and not os.getenv('WAYLAND_DISPLAY'):
    os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
    
import cv2

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from vision.object_detector import ObjectDetector
from vision.depth_estimator import DepthEstimator
from vision.scene_analyzer import SceneAnalyzer
from audio.voice_engine import VoiceEngine
from core.dristi_system import DristiSystem

def main(headless=False):
    print("=" * 70)
    print("🚀 DRISTI - Vision-Based Voice Assistant")
    print("   For Visually Impaired Users")
    print("=" * 70)
    
    # Initialize Voice Engine
    print("\n🔊 Initializing Text-to-Speech...")
    voice = VoiceEngine(rate=150, volume=1.0, use_female_voice=True)
    voice.speak("Initializing Dristi vision assistant. Please wait.", async_mode=True)
    
    # Initialize Vision Modules
    print("\n📦 Loading AI models...")
    
    try:
        detector = ObjectDetector(model_path='yolov8n.pt', confidence=0.5, device='cuda')
        print("✅ YOLO Object Detector loaded (GPU)")
    except Exception as e:
        print(f"❌ Failed to load YOLO: {e}")
        voice.speak("Error loading object detection model.")
        sys.exit(1)
    
    # Try to load optional modules
    depth = None
    analyzer = None
    
    try:
        depth = DepthEstimator(device='cuda')
        print("✅ MiDaS Depth Estimator loaded")
    except Exception as e:
        print(f"⚠️  Depth estimation not available: {e}")
    
    try:
        analyzer = SceneAnalyzer(device='cuda', model_name='ViT-B/32')
        print("✅ CLIP Scene Analyzer loaded (GPU)")
    except Exception as e:
        print(f"⚠️  Scene analysis not available: {e}")
    
    voice.speak("All systems ready. I am Dristi, your vision assistant.", async_mode=True)
    
    # Open camera (auto-detect available camera)
    cap = None
    for camera_index in range(5):
        test_cap = cv2.VideoCapture(camera_index)
        if test_cap.isOpened():
            ret, frame = test_cap.read()
            if ret:
                print(f"✅ Using camera {camera_index}")
                cap = test_cap
                break
            test_cap.release()
    
    if cap is None:
        print("❌ Camera not accessible!")
        voice.speak("Error. Camera not accessible. Please check connection.")
        sys.exit(1)
    
    voice.speak("Camera active. I am ready to assist you.")
    
    # Get camera properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"✅ Camera ready! Resolution: {width}x{height}")
    
    # Initialize Dristi System
    system = DristiSystem(
        object_detector=detector,
        depth_estimator=depth,
        scene_analyzer=analyzer,
        voice_engine=voice
    )
    
    # Print controls
    print("\n" + "=" * 70)
    print("🎯 DRISTI VOICE ASSISTANT - ACTIVE")
    print("=" * 70)
    print("\n📋 VOICE COMMANDS:")
    print("   SPACE    - What do you see? (full description)")
    print("   'h'      - Any hazards? (safety check)")
    print("   'l'      - Where am I? (location)")
    print("   'o'      - What objects? (object list)")
    print("   'p'      - People nearby? (people count)")
    print("   'r'      - Repeat last description")
    print("   'a'      - Toggle auto-narration (every 15 seconds)")
    print("   'd'      - Toggle depth visualization (if available)")
    print("   's'      - Save screenshot")
    print("   'q'      - Exit system")
    print("\n⚠️  IMPORTANT: Use headphones/speakers for audio!")
    print("=" * 70 + "\n")
    
    show_depth = False
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("❌ Failed to grab frame")
                break
            
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            
            # Process frame through Dristi system
            annotated_frame, detected_objects, current_scene = system.process_frame(frame)
            
            # Add visual overlay
            annotated_frame = system.add_overlay(annotated_frame)
            
            # Display depth map if toggled (and available)
            if not headless:
                try:
                    if show_depth and depth and depth.get_colored_depth() is not None:
                        depth_colored = depth.get_colored_depth()
                        blended = cv2.addWeighted(annotated_frame, 0.5, depth_colored, 0.5, 0)
                        cv2.imshow('Dristi - Voice Assistant (Depth View)', blended)
                    else:
                        cv2.imshow('Dristi - Voice Assistant', annotated_frame)
                except:
                    pass  # Skip display if not available
            
            # Handle keyboard commands (non-blocking)
            try:
                if not headless:
                    key = cv2.waitKey(1) & 0xFF
                else:
                    # In headless mode, use a small sleep instead of cv2.waitKey
                    import time
                    time.sleep(0.001)
                    key = -1
            except:
                key = -1
            
            if key == ord('q'):
                print("\n👋 Shutting down...")
                voice.speak("Shutting down Dristi. Stay safe. Goodbye.")
                break
            
            elif key == ord('d') and depth:
                show_depth = not show_depth
                status = "ON (blended view)" if show_depth else "OFF (detection only)"
                print(f"🔄 Depth visualization: {status}")
                voice.speak(f"Depth visualization {status}")
            
            elif key == ord('s'):
                filename = f"dristi_screenshot_{system.frame_count}.jpg"
                cv2.imwrite(filename, annotated_frame)
                print(f"📸 Saved: {filename}")
                voice.speak("Screenshot saved.")
            
            else:
                # Handle other voice commands
                system.handle_command(key, current_time)
    
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        voice.speak("System interrupted.", async_mode=True)
    
    finally:
        cap.release()
        if not headless:
            cv2.destroyAllWindows()
        voice.speak("Dristi shutdown complete. Thank you for using Dristi.", async_mode=True)
        print("\n✅ Dristi closed successfully")
        print("=" * 70)

if __name__ == '__main__':
    # Default to headless=True to avoid display blocking issues
    headless = '--display' not in sys.argv
    if '--headless' in sys.argv:
        headless = True
    main(headless=headless)
