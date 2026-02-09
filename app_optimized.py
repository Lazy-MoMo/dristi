#!/usr/bin/env python3
"""
DRISTI - Integrated Vision Assistant (OPTIMIZED VERSION)
Complete application with performance improvements
"""
import os
import sys
import time
import threading

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

class OptimizedDristiApp:
    """Optimized Dristi application with performance improvements"""
    
    def __init__(self, enable_depth=False, enable_scene=True, 
                 target_fps=15, frame_width=640, headless=False):
        """Initialize with optimization parameters"""
        self.target_fps = target_fps
        self.frame_width = frame_width
        self.enable_depth = enable_depth
        self.enable_scene = enable_scene
        self.headless = headless
        
        print("=" * 70)
        print("🚀 DRISTI - Optimized Vision Assistant")
        print("   For Visually Impaired Users")
        print("=" * 70)
        
        # Initialize Voice Engine
        print("\n🔊 Initializing Text-to-Speech...")
        self.voice = VoiceEngine(rate=150, volume=1.0, use_female_voice=True)
        self.voice.speak("Initializing Dristi. Please wait.", async_mode=True)
        
        # Initialize Vision Modules
        print("\n📦 Loading AI models...")
        
        try:
            # Smaller input size = faster detection, GPU accelerated
            self.detector = ObjectDetector(model_path='yolov8n.pt', confidence=0.5, input_size=320, device='cuda')
            print("✅ YOLO Object Detector loaded (GPU optimized)")
        except Exception as e:
            print(f"❌ Failed to load YOLO: {e}")
            self.voice.speak("Error loading object detection model.")
            sys.exit(1)
        
        # Depth estimation (optional)
        self.depth = None
        if self.enable_depth:
            try:
                self.depth = DepthEstimator(device='cuda')
                print("✅ MiDaS Depth Estimator loaded (optimized)")
            except Exception as e:
                print(f"⚠️  Depth estimation not available: {e}")
        
        # Scene analysis (optional)
        self.analyzer = None
        if self.enable_scene:
            try:
                self.analyzer = SceneAnalyzer(device='cuda', model_name='ViT-B/32')
                print("✅ CLIP Scene Analyzer loaded (GPU)")
            except Exception as e:
                print(f"⚠️  Scene analysis not available: {e}")
        
        self.voice.speak("Systems ready. Camera starting.", async_mode=True)
        
        # Open camera (auto-detect available camera)
        self.cap = None
        for camera_index in range(5):
            test_cap = cv2.VideoCapture(camera_index)
            if test_cap.isOpened():
                ret, frame = test_cap.read()
                if ret:
                    print(f"✅ Using camera {camera_index}")
                    self.cap = test_cap
                    break
                test_cap.release()
        
        if self.cap is None:
            print("❌ Camera not accessible!")
            self.voice.speak("Error. Camera not accessible.")
            sys.exit(1)
        
        # Set camera resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(frame_width * 9 / 16))
        self.cap.set(cv2.CAP_PROP_FPS, target_fps)
        
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"✅ Camera ready! Resolution: {width}x{height}")
        
        # Initialize Dristi System
        self.system = DristiSystem(
            object_detector=self.detector,
            depth_estimator=self.depth,
            scene_analyzer=self.analyzer,
            voice_engine=self.voice
        )
        
        # Optimize processing intervals (GPU accelerated, can afford faster)
        self.system.detection_interval = 1  # Every frame (GPU is fast)
        self.system.scene_analysis_interval = 30  # Every 30 frames (GPU accelerated)
        self.system.depth_estimation_interval = 2  # Every 2 frames (GPU accelerated)
        
        self.show_depth = False
        self.running = True
    
    def print_controls(self):
        """Print control information"""
        print("\n" + "=" * 70)
        print("🎯 DRISTI OPTIMIZED - ACTIVE")
        print("=" * 70)
        print("\n📋 VOICE COMMANDS:")
        print("   SPACE    - What do you see?")
        print("   'h'      - Any hazards?")
        print("   'l'      - Where am I?")
        print("   'o'      - What objects?")
        print("   'p'      - People nearby?")
        print("   'r'      - Repeat last description")
        print("   'a'      - Toggle auto-narration")
        if self.enable_depth:
            print("   'd'      - Toggle depth view")
        print("   's'      - Save screenshot")
        print("   'q'      - Exit")
        print("\n⚠️  Performance optimized for faster response!")
        print("=" * 70 + "\n")
    
    def run(self):
        """Main loop"""
        self.print_controls()
        
        frame_time = 1.0 / self.target_fps
        last_frame_time = time.time()
        
        try:
            while self.running:
                # Control frame rate
                current_time = time.time()
                elapsed = current_time - last_frame_time
                
                if elapsed < frame_time:
                    time.sleep(frame_time - elapsed)
                    current_time = time.time()
                
                last_frame_time = current_time
                
                # Read frame
                ret, frame = self.cap.read()
                if not ret:
                    print("❌ Failed to grab frame")
                    break
                
                # Resize frame for faster processing
                h, w = frame.shape[:2]
                if w != self.frame_width:
                    scale = self.frame_width / w
                    frame = cv2.resize(frame, (self.frame_width, int(h * scale)))
                
                # Process frame
                annotated_frame, _, _ = self.system.process_frame(frame)
                annotated_frame = self.system.add_overlay(annotated_frame)
                
                # Display (skip if headless)
                if not self.headless:
                    try:
                        if self.show_depth and self.depth and self.depth.get_colored_depth() is not None:
                            depth_colored = self.depth.get_colored_depth()
                            depth_colored = cv2.resize(depth_colored, (annotated_frame.shape[1], annotated_frame.shape[0]))
                            blended = cv2.addWeighted(annotated_frame, 0.5, depth_colored, 0.5, 0)
                            cv2.imshow('Dristi (Optimized)', blended)
                        else:
                            cv2.imshow('Dristi (Optimized)', annotated_frame)
                    except:
                        pass  # Skip display if not available
                
                # Handle input
                try:
                    if not self.headless:
                        key = cv2.waitKey(1) & 0xFF
                    else:
                        # In headless mode, use a small sleep instead of cv2.waitKey
                        time.sleep(0.001)
                        key = -1
                except:
                    key = -1
                self.handle_key(key, current_time)
        
        except KeyboardInterrupt:
            print("\n⚠️  Interrupted by user")
        
        finally:
            self.cleanup()
    
    def handle_key(self, key, current_time):
        """Handle keyboard input"""
        if key == ord('q'):
            self.voice.speak("Shutting down.")
            self.running = False
        elif key == ord('d') and self.enable_depth:
            self.show_depth = not self.show_depth
            status = "ON" if self.show_depth else "OFF"
            self.voice.speak(f"Depth view {status}")
        elif key == ord('s'):
            filename = f"dristi_opt_{self.system.frame_count}.jpg"
            self.cap.release()
            cap_temp = cv2.VideoCapture(0)
            ret, frame = cap_temp.read()
            if ret:
                cv2.imwrite(filename, frame)
                self.voice.speak("Screenshot saved.")
            self.cap = cap_temp
        else:
            self.system.handle_command(key, current_time)
    
    def cleanup(self):
        """Cleanup resources"""
        self.cap.release()
        if not self.headless:
            cv2.destroyAllWindows()
        self.voice.speak("Dristi closed. Thank you.", async_mode=True)
        print("\n✅ Shutdown complete")
        print("=" * 70)

def main():
    # Default to headless=True to avoid display blocking issues
    headless = '--display' not in sys.argv
    if '--headless' in sys.argv:
        headless = True
    
    # Skip interactive prompt in headless mode
    if headless:
        print("\n⚙️  OPTIMIZATION SETTINGS")
        print("-" * 70)
        print("Running in headless mode with defaults: 15 FPS, 640px width, Scene analysis ON, Depth OFF")
        app = OptimizedDristiApp(headless=headless)
    else:
        # Configuration options
        print("\n⚙️  OPTIMIZATION SETTINGS")
        print("-" * 70)
        print("Default: 15 FPS, 640px width, Scene analysis ON, Depth OFF")
        print("\nEnter 'o' for manual optimization, or press Enter for defaults")
        
        choice = input().strip().lower()
        
        if choice == 'o':
            try:
                fps = int(input("Target FPS (5-30, default 15): ") or "15")
                width = int(input("Frame width in pixels (320-1280, default 640): ") or "640")
                depth = input("Enable depth estimation? (y/n, default n): ").lower() == 'y'
                scene = input("Enable scene analysis? (y/n, default y): ").lower() != 'n'
                
                fps = max(5, min(30, fps))
                width = max(320, min(1280, width))
                
                app = OptimizedDristiApp(enable_depth=depth, enable_scene=scene, 
                                         target_fps=fps, frame_width=width, headless=headless)
            except Exception as e:
                print(f"Invalid input: {e}, using defaults")
                app = OptimizedDristiApp(headless=headless)
        else:
            app = OptimizedDristiApp(headless=headless)
    
    app.run()

if __name__ == '__main__':
    main()
