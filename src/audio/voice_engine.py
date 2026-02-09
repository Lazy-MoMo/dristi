"""
Voice Interface Module using pyttsx3
"""
import pyttsx3
import threading
from collections import Counter

class VoiceEngine:
    """Handles text-to-speech and voice output"""
    
    def __init__(self, rate=150, volume=1.0, use_female_voice=True):
        """Initialize TTS engine"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Set voice preference
        voices = self.engine.getProperty('voices')
        if use_female_voice and len(voices) > 1:
            self.engine.setProperty('voice', voices[1].id)
    
    def speak(self, text, async_mode=True):
        """Convert text to speech"""
        print(f"🔊 Dristi: {text}")
        
        if async_mode:
            # Non-blocking speech
            threading.Thread(
                target=lambda: self.engine.say(text) or self.engine.runAndWait(),
                daemon=True
            ).start()
        else:
            # Blocking speech
            self.engine.say(text)
            self.engine.runAndWait()
    
    @staticmethod
    def generate_description(objects, scene_info, depth_info=None, mode='full'):
        """Generate natural language description"""
        
        if mode == 'hazards':
            # Hazard-focused description
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
            
            warnings = []
            
            if detected_hazards['vehicles']:
                vehicle_names = [h['name'] for h in detected_hazards['vehicles']]
                counts = Counter(vehicle_names)
                vehicle_desc = ', '.join(
                    [f"{count} {name}" if count > 1 else name for name, count in counts.items()]
                )
                warnings.append(f"Warning! {vehicle_desc} detected")
            
            if detected_hazards['obstacles']:
                warnings.append(f"{len(detected_hazards['obstacles'])} obstacles in path")
            
            if detected_hazards['animals']:
                animal_names = [h['name'] for h in detected_hazards['animals']]
                warnings.append(f"{', '.join(animal_names)} detected nearby")
            
            if warnings:
                return "Hazard alert. " + ". ".join(warnings) + ". Please be careful."
            else:
                return "No immediate hazards detected. Path appears clear."
        
        elif mode == 'location':
            # Location-focused description
            scene = scene_info['scene_type'].replace("a ", "").replace("an ", "")
            return f"You appear to be in {scene}."
        
        elif mode == 'objects':
            # Object-focused description
            if not objects:
                return "No objects detected in current view."
            
            counts = Counter([obj['name'] for obj in objects])
            total = len(objects)
            unique = len(counts)
            
            if unique <= 3:
                obj_list = ', '.join(
                    [f"{count} {obj}" if count > 1 else obj for obj, count in counts.most_common()]
                )
                return f"I see {obj_list}."
            else:
                top_3 = counts.most_common(3)
                obj_desc = ', '.join(
                    [f"{count} {obj}" if count > 1 else obj for obj, count in top_3]
                )
                return f"I see {total} objects. Mainly {obj_desc}. Plus {unique - 3} other types."
        
        elif mode == 'people':
            # People-focused description
            people = [obj for obj in objects if obj['name'] == 'person']
            count = len(people)
            
            if count == 0:
                return "No people detected nearby."
            elif count == 1:
                return "One person detected nearby."
            else:
                return f"{count} people detected in the area."
        
        else:  # mode == 'full'
            # Comprehensive description
            description_parts = []
            
            # Scene context
            scene = scene_info['scene_type'].replace("a ", "").replace("an ", "")
            if scene_info['scene_confidence'] > 25:
                description_parts.append(f"You are in {scene}.")
            
            # Priority check: hazards first
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
            
            if detected_hazards['vehicles']:
                vehicle_count = len(detected_hazards['vehicles'])
                description_parts.append(
                    f"Warning! {vehicle_count} vehicle{'s' if vehicle_count > 1 else ''} detected."
                )
            
            # Objects
            if objects:
                counts = Counter([obj['name'] for obj in objects])
                
                # Priority objects
                priority = ['person', 'door', 'chair', 'stairs', 'bench']
                priority_detected = [obj for obj in counts if obj in priority]
                
                if priority_detected:
                    priority_list = []
                    for obj in priority_detected[:2]:
                        count = counts[obj]
                        priority_list.append(f"{count} {obj}" if count > 1 else obj)
                    description_parts.append(f"Important: {', '.join(priority_list)} detected.")
                
                # General count
                total = len(objects)
                if total > len(priority_detected):
                    description_parts.append(f"{total} total objects in view.")
            else:
                description_parts.append("No objects detected in immediate area.")
            
            return " ".join(description_parts)
