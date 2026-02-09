"""
Object Detection Module using YOLOv8 - OPTIMIZED
"""
from ultralytics import YOLO
import cv2
import numpy as np
import threading

class ObjectDetector:
    """Handles real-time object detection with GPU optimization"""
    
    def __init__(self, model_path='yolov8n.pt', confidence=0.5, input_size=416, device='cuda'):
        """Initialize YOLO model with GPU support"""
        self.model = YOLO(model_path)
        self.device = device
        self.model.to(device)  # Move model to GPU
        self.confidence = confidence
        self.input_size = input_size  # Smaller input = faster inference
        self.last_detections = []
        self.last_annotated = None
        self.processing = False
        self.lock = threading.Lock()
        # Warmup GPU
        self._gpu_warmup()
    
    def detect(self, frame):
        """
        Detect objects in frame with GPU optimization
        Returns: (annotated_frame, list of detected objects)
        """
        import torch
        
        # Resize frame for faster processing
        h, w = frame.shape[:2]
        scale = self.input_size / max(h, w)
        resized = cv2.resize(frame, (int(w * scale), int(h * scale)))
        
        # Run detection on GPU with half precision for speed
        results = self.model(resized, conf=self.confidence, verbose=False, device=self.device)
        
        detected_objects = []
        if results[0].boxes is not None:
            for box in results[0].boxes:
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                confidence = float(box.conf[0])
                
                # Scale bbox back to original frame size (keep on GPU briefly)
                bbox = box.xyxy[0].cpu().numpy()
                bbox = bbox / scale
                
                detected_objects.append({
                    'name': class_name,
                    'confidence': confidence,
                    'bbox': bbox,
                    'class_id': class_id
                })
        
        with self.lock:
            self.last_detections = detected_objects
        
        # Draw on original frame for visualization
        annotated_frame = frame.copy()
        for obj in detected_objects:
            x1, y1, x2, y2 = map(int, obj['bbox'])
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"{obj['name']} {obj['confidence']:.2f}"
            cv2.putText(annotated_frame, label, (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return annotated_frame, detected_objects
    
    def get_last_detections(self):
        """Get last detected objects (thread-safe)"""
        with self.lock:
            return self.last_detections.copy()
    
    def set_input_size(self, size):
        """Adjust input size for speed/accuracy tradeoff"""
        self.input_size = size
    
    def _gpu_warmup(self):
        """Warmup GPU with a dummy forward pass"""
        import torch
        try:
            dummy_input = torch.zeros(1, 3, 320, 320).to(self.device)
            with torch.no_grad():
                _ = self.model.model(dummy_input)
        except:
            pass  # Silently skip if warmup fails
