"""
Depth Estimation Module using MiDaS
"""
import torch
import cv2
import numpy as np

class DepthEstimator:
    """Handles depth estimation using MiDaS"""
    
    def __init__(self, device='cpu'):
        """Initialize MiDaS model"""
        self.device = torch.device(device)
        self.midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small", trust_repo=True)
        self.midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
        self.transform = self.midas_transforms.small_transform
        
        self.midas.to(self.device)
        self.midas.eval()
        self.depth_map_normalized = None
        self.depth_colored = None
    
    def estimate(self, frame, scale=0.5):
        """
        Estimate depth map for frame with GPU acceleration
        Returns: (depth_map_normalized, depth_colored_visualization)
        """
        # Resize for faster processing
        h, w = frame.shape[:2]
        scaled_frame = cv2.resize(frame, (int(w * scale), int(h * scale)))
        
        img_for_depth = cv2.cvtColor(scaled_frame, cv2.COLOR_BGR2RGB)
        input_batch = self.transform(img_for_depth).to(self.device)
        
        with torch.no_grad():
            prediction = self.midas(input_batch)
            # Use GPU-accelerated interpolation on tensor
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=scaled_frame.shape[:2],
                mode="bilinear",
                align_corners=False,
            ).squeeze()
        
        # Transfer to CPU only for final visualization
        depth_map = prediction.cpu().detach().numpy()
        
        # Upscale back to original size
        depth_map = cv2.resize(depth_map, (w, h), interpolation=cv2.INTER_LINEAR)
        
        # Normalize depth map
        self.depth_map_normalized = cv2.normalize(
            depth_map, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F
        )
        
        # Create colored visualization
        depth_map_8bit = (self.depth_map_normalized * 255).astype(np.uint8)
        self.depth_colored = cv2.applyColorMap(depth_map_8bit, cv2.COLORMAP_MAGMA)
        
        return self.depth_map_normalized, self.depth_colored
    
    def estimate_distance(self, depth_map, bbox):
        """
        Estimate distance category from depth map and bounding box
        Returns: (distance_text, distance_value, color)
        """
        x1, y1, x2, y2 = map(int, bbox)
        
        # Ensure bbox is within frame
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(depth_map.shape[1], x2), min(depth_map.shape[0], y2)
        
        # Get region of interest
        roi = depth_map[y1:y2, x1:x2]
        
        if roi.size == 0:
            return "Unknown", 0.5, (255, 255, 255)
        
        # Get median depth
        median_depth = np.median(roi)
        normalized_depth = median_depth
        
        # Categorize distance
        if normalized_depth > 0.75:
            distance_text = "Very Close (< 0.5m)"
            color = (0, 0, 255)  # Red
            distance_val = 0.3
        elif normalized_depth > 0.55:
            distance_text = "Close (0.5-1m)"
            color = (0, 165, 255)  # Orange
            distance_val = 0.8
        elif normalized_depth > 0.35:
            distance_text = "Medium (1-2m)"
            color = (0, 255, 255)  # Yellow
            distance_val = 1.5
        elif normalized_depth > 0.20:
            distance_text = "Far (2-3m)"
            color = (0, 255, 0)  # Green
            distance_val = 2.5
        else:
            distance_text = "Very Far (> 3m)"
            color = (0, 200, 0)  # Dark green
            distance_val = 4.0
        
        return distance_text, distance_val, color
    
    def get_colored_depth(self):
        """Get last colored depth visualization"""
        return self.depth_colored
