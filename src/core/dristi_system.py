"""
Main Dristi Integration System - OPTIMIZED
Unified module combining Vision, Audio, and Scene Understanding
"""
import cv2
import time
import threading
from collections import Counter
from queue import Queue

class DristiSystem:
    """Main integrated vision assistant system with optimization"""
    
    def __init__(self, object_detector, depth_estimator=None, scene_analyzer=None, voice_engine=None):
        """
        Initialize Dristi system with all modules
        
        Args:
            object_detector: ObjectDetector instance
            depth_estimator: DepthEstimator instance (optional)
            scene_analyzer: SceneAnalyzer instance (optional)
            voice_engine: VoiceEngine instance (optional)
        """
        self.detector = object_detector
        self.depth = depth_estimator
        self.analyzer = scene_analyzer
        self.voice = voice_engine
        
        # State management
        self.frame_count = 0
        self.fps = 0
        self.fps_start_time = time.time()
        self.detected_objects = []
        self.current_scene = None
        self.last_description = ""
        self.auto_narrate = False
        self.narration_interval = 15  # seconds
        self.last_narration_time = 0
        
        # Optimization settings (reduced intervals for GPU acceleration)
        self.detection_interval = 1  # Process detection every frame (GPU is fast)
        self.scene_analysis_interval = 30  # Process scene every 30 frames (GPU accelerated)
        self.depth_estimation_interval = 2  # Process depth every 2 frames (GPU accelerated)
        
        # Threading for parallel processing
        self.processing_threads = {}
        self.frame_queue = Queue(maxsize=2)
        self.stop_threads = False
    
    def process_frame(self, frame):
        """
        Process a single frame through the system
        Returns: (annotated_frame, detected_objects, scene_info)
        """
        self.frame_count += 1
        current_time = time.time()
        annotated_frame = frame.copy()
        
        # Calculate FPS
        if self.frame_count % 30 == 0:
            self.fps = 30 / (current_time - self.fps_start_time)
            self.fps_start_time = current_time
        
        # Object detection
        if self.frame_count % self.detection_interval == 0:
            annotated_frame, self.detected_objects = self.detector.detect(frame)
        
        # Depth estimation (if enabled)
        if self.depth and self.frame_count % self.depth_estimation_interval == 0:
            depth_map, depth_colored = self.depth.estimate(frame)
            
            # Add distance info to detected objects
            for obj in self.detected_objects:
                if depth_map is not None:
                    distance_text, distance_val, color = self.depth.estimate_distance(
                        depth_map, obj['bbox']
                    )
                    obj['distance_text'] = distance_text
                    obj['distance_val'] = distance_val
        
        # Scene analysis (if enabled)
        if self.analyzer and self.frame_count % self.scene_analysis_interval == 0:
            self.current_scene = self.analyzer.analyze(frame)
        
        # Auto-narration
        if self.voice and self.auto_narrate:
            if current_time - self.last_narration_time > self.narration_interval:
                if self.current_scene:
                    description = self.voice.generate_description(
                        self.detected_objects, self.current_scene, mode='full'
                    )
                    self.voice.speak(description)
                    self.last_description = description
                    self.last_narration_time = current_time
        
        return annotated_frame, self.detected_objects, self.current_scene
    
    def add_overlay(self, frame):
        """Add visual overlay to frame (for sighted helper/developer)"""
        cv2.putText(frame, f"Dristi Active | FPS: {self.fps:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        status = "AUTO-NARRATION: ON" if self.auto_narrate else "Listening for commands..."
        color = (0, 255, 255) if self.auto_narrate else (255, 255, 255)
        cv2.putText(frame, status, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cv2.putText(frame, f"Objects: {len(self.detected_objects)}", 
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        if self.current_scene:
            scene = self.current_scene['scene_type'].replace("a ", "").replace("an ", "")
            cv2.putText(frame, f"Scene: {scene}", 
                       (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        
        return frame
    
    def handle_command(self, key, current_time):
        """Handle keyboard commands"""
        if not self.voice:
            return
        
        if key == ord(' '):  # Full description
            if self.current_scene:
                self.voice.speak("Analyzing environment")
                description = self.voice.generate_description(
                    self.detected_objects, self.current_scene, mode='full'
                )
                self.voice.speak(description)
                self.last_description = description
            else:
                self.voice.speak("Still analyzing. Please wait.")
        
        elif key == ord('h'):  # Hazards
            description = self.voice.generate_description(
                self.detected_objects, self.current_scene, mode='hazards'
            )
            self.voice.speak(description)
            self.last_description = description
        
        elif key == ord('l'):  # Location
            if self.current_scene:
                description = self.voice.generate_description(
                    self.detected_objects, self.current_scene, mode='location'
                )
                self.voice.speak(description)
                self.last_description = description
            else:
                self.voice.speak("Determining location. Please wait.")
        
        elif key == ord('o'):  # Objects
            description = self.voice.generate_description(
                self.detected_objects, self.current_scene, mode='objects'
            )
            self.voice.speak(description)
            self.last_description = description
        
        elif key == ord('p'):  # People
            description = self.voice.generate_description(
                self.detected_objects, self.current_scene, mode='people'
            )
            self.voice.speak(description)
            self.last_description = description
        
        elif key == ord('r'):  # Repeat
            if self.last_description:
                self.voice.speak(self.last_description)
            else:
                self.voice.speak("No previous description available")
        
        elif key == ord('a'):  # Toggle auto-narration
            self.auto_narrate = not self.auto_narrate
            if self.auto_narrate:
                self.voice.speak("Auto narration enabled. I will describe your surroundings every 15 seconds.")
                self.last_narration_time = current_time
            else:
                self.voice.speak("Auto narration disabled. Press space for descriptions.")
    
    def reset_fps(self):
        """Reset FPS counter"""
        self.fps_start_time = time.time()
        self.fps = 0
