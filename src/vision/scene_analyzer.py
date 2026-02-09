"""
Scene Understanding Module using CLIP
"""
import torch
import clip
import cv2
from PIL import Image
from collections import Counter

class SceneAnalyzer:
    """Handles scene understanding using CLIP"""
    
    def __init__(self, device='cpu', model_name='ViT-B/32'):
        """Initialize CLIP model"""
        self.device = device
        self.model, self.preprocess = clip.load(model_name, device=device)
        
        # Define scene understanding queries
        self.scene_type_queries = [
            "an indoor room", "an outdoor area", "a kitchen with appliances",
            "a bedroom with bed", "an office with desk and computer",
            "a living room with furniture", "a street with buildings",
            "a park with trees and grass", "a store or shop", "a bathroom"
        ]
        
        self.scene_condition_queries = [
            "a crowded busy place with many people", "a quiet empty space with few objects",
            "a well-lit bright environment", "a dark dimly-lit space",
            "a clean organized area", "a cluttered messy space"
        ]
        
        self.activity_queries = [
            "people walking or moving", "people sitting and resting",
            "people working at desk or computer", "people eating or drinking",
            "people talking or interacting", "no visible human activity"
        ]
    
    def analyze(self, frame):
        """
        Analyze scene in frame with GPU acceleration
        Returns: dictionary with scene analysis results
        """
        # Convert to PIL Image and move to GPU
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            # Encode image once on GPU
            image_features = self.model.encode_image(image_input)
            
            # Pre-tokenize all queries for batch processing
            scene_type_text = clip.tokenize(self.scene_type_queries).to(self.device)
            condition_text = clip.tokenize(self.scene_condition_queries).to(self.device)
            activity_text = clip.tokenize(self.activity_queries).to(self.device)
            
            # Batch encode all text at once
            scene_type_features = self.model.encode_text(scene_type_text)
            condition_features = self.model.encode_text(condition_text)
            activity_features = self.model.encode_text(activity_text)
            
            # Compute similarities on GPU (batch operations)
            scene_type_similarity = (100.0 * image_features @ scene_type_features.T).softmax(dim=-1)
            condition_similarity = (100.0 * image_features @ condition_features.T).softmax(dim=-1)
            activity_similarity = (100.0 * image_features @ activity_features.T).softmax(dim=-1)
        
        # Get top predictions
        scene_values, scene_indices = scene_type_similarity[0].topk(2)
        condition_values, condition_indices = condition_similarity[0].topk(2)
        activity_values, activity_indices = activity_similarity[0].topk(1)
        
        return {
            'scene_type': self.scene_type_queries[scene_indices[0].item()],
            'scene_confidence': scene_values[0].item(),
            'scene_type_alt': self.scene_type_queries[scene_indices[1].item()],
            'condition': self.scene_condition_queries[condition_indices[0].item()],
            'condition_confidence': condition_values[0].item(),
            'activity': self.activity_queries[activity_indices[0].item()],
            'activity_confidence': activity_values[0].item()
        }
    
    @staticmethod
    def check_hazards(objects):
        """Identify potential hazards"""
        hazard_types = {
            'vehicles': ['car', 'truck', 'bus', 'bicycle', 'motorcycle'],
            'traffic': ['traffic light', 'stop sign'],
            'obstacles': ['bench', 'fire hydrant', 'parking meter'],
            'animals': ['dog', 'cat', 'bird', 'horse']
        }
        
        detected_hazards = {'vehicles': [], 'traffic': [], 'obstacles': [], 'animals': []}
        
        for obj in objects:
            for hazard_type, hazard_list in hazard_types.items():
                if obj['name'] in hazard_list:
                    detected_hazards[hazard_type].append(obj)
        
        return detected_hazards
