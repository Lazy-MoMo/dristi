# 06_voice_assistant.py
# Dristi - Complete Voice Assistant with Scene Understanding
import cv2
import torch
import clip
import pyttsx3
from PIL import Image
from ultralytics import YOLO
from collections import Counter
import threading
import time

print("=" * 70)
print("🎙️ DRISTI - Voice-Based Vision Assistant")
print("   For Visually Impaired Users")
print("=" * 70)

# Initialize TTS engine
print("\n🔊 Initializing Text-to-Speech...")
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 150)  # Speaking speed
tts_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Set voice (try to use female voice if available)
voices = tts_engine.getProperty('voices')
if len(voices) > 1:
    tts_engine.setProperty('voice', voices[1].id)  # Usually female voice

def speak(text, async_mode=True):
    """Convert text to speech"""
    print(f"🔊 Dristi: {text}")
    if async_mode:
        # Non-blocking speech
        threading.Thread(
            target=lambda: tts_engine.say(text) or tts_engine.runAndWait(),
            daemon=True
        ).start()
    else:
        # Blocking speech
        tts_engine.say(text)
        tts_engine.runAndWait()

# Load AI models
print("\n📦 Loading AI models...")
speak("Initializing Dristi vision assistant. Please wait.", async_mode=False)

yolo_model = YOLO('yolov8n.pt')
print("✅ YOLO loaded")

device = "cpu"
clip_model, clip_preprocess = clip.load("ViT-B/32", device=device)
print("✅ CLIP loaded")

speak("All systems ready. I am Dristi, your vision assistant.", async_mode=False)

# Scene understanding queries
scene_queries = [
    "an indoor room", "an outdoor area", "a kitchen", "a bedroom",
    "an office", "a living room", "a street", "a park", 
    "a crowded place", "an empty room", "a store"
]

def analyze_scene(frame):
    """Analyze scene with CLIP"""
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image_input = clip_preprocess(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
        text = clip.tokenize(scene_queries).to(device)
        text_features = clip_model.encode_text(text)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
    
    values, indices = similarity[0].topk(2)
    return {
        'scene': scene_queries[indices[0]],
        'confidence': values[0].item(),
        'alt_scene': scene_queries[indices[1]]
    }

def check_hazards(objects):
    """Identify potential hazards for blind users"""
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

def generate_voice_description(objects, scene_info, mode='full'):
    """Generate voice description optimized for blind users"""
    
    if mode == 'hazards':
        # Hazard-focused description
        hazards = check_hazards(objects)
        warnings = []
        
        if hazards['vehicles']:
            vehicle_names = [h['name'] for h in hazards['vehicles']]
            counts = Counter(vehicle_names)
            vehicle_desc = ', '.join([f"{count} {name}" if count > 1 else name 
                                     for name, count in counts.items()])
            warnings.append(f"Warning! {vehicle_desc} detected")
        
        if hazards['obstacles']:
            warnings.append(f"{len(hazards['obstacles'])} obstacles in path")
        
        if hazards['animals']:
            animal_names = [h['name'] for h in hazards['animals']]
            warnings.append(f"{', '.join(animal_names)} detected nearby")
        
        if warnings:
            return "Hazard alert. " + ". ".join(warnings) + ". Please be careful."
        else:
            return "No immediate hazards detected. Path appears clear."
    
    elif mode == 'location':
        # Location-focused description
        scene = scene_info['scene'].replace("a ", "").replace("an ", "")
        return f"You appear to be in {scene}."
    
    elif mode == 'objects':
        # Object-focused description
        if not objects:
            return "No objects detected in current view."
        
        counts = Counter([obj['name'] for obj in objects])
        total = len(objects)
        unique = len(counts)
        
        if unique <= 3:
            obj_list = ', '.join([f"{count} {obj}" if count > 1 else obj 
                                 for obj, count in counts.most_common()])
            return f"I see {obj_list}."
        else:
            top_3 = counts.most_common(3)
            obj_desc = ', '.join([f"{count} {obj}" if count > 1 else obj 
                                 for obj, count in top_3])
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
        scene = scene_info['scene'].replace("a ", "").replace("an ", "")
        if scene_info['confidence'] > 25:
            description_parts.append(f"You are in {scene}.")
        
        # Priority check: hazards first
        hazards = check_hazards(objects)
        if hazards['vehicles']:
            vehicle_count = len(hazards['vehicles'])
            description_parts.append(f"Warning! {vehicle_count} vehicle{'s' if vehicle_count > 1 else ''} detected.")
        
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

# Open camera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    speak("Error. Camera not accessible. Please check connection.")
    exit()

speak("Camera active. I am ready to assist you.")

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
print("   'q'      - Exit system")
print("\n⚠️  IMPORTANT: Use headphones/speakers for audio!")
print("=" * 70 + "\n")

frame_count = 0
fps = 0
fps_start_time = time.time()
detected_objects = []  # Initialize here!
current_scene = None
last_description = ""
auto_narrate = False
last_narration_time = 0
narration_interval = 15  # seconds

# Initialize annotated_frame
annotated_frame = None

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        current_time = time.time()
        
        # Calculate FPS
        if frame_count % 30 == 0:
            fps = 30 / (current_time - fps_start_time)
            fps_start_time = current_time
        
        # Object detection (every 3rd frame)
        if frame_count % 3 == 0:
            results = yolo_model(frame, conf=0.5, verbose=False)
            annotated_frame = results[0].plot()
            
            detected_objects = []
            for box in results[0].boxes:
                class_name = yolo_model.names[int(box.cls[0])]
                confidence = float(box.conf[0])
                detected_objects.append({
                    'name': class_name,
                    'confidence': confidence
                })
            
            # Analyze scene (less frequently)
            if frame_count % 30 == 0:
                current_scene = analyze_scene(frame)
        else:
            # Keep previous frame
            if annotated_frame is None:
                annotated_frame = frame.copy()
            else:
                annotated_frame = frame
        
        # Auto-narration
        if auto_narrate and (current_time - last_narration_time > narration_interval):
            if current_scene:
                description = generate_voice_description(detected_objects, current_scene, 'full')
                speak(description)
                last_description = description
                last_narration_time = current_time
        
        # Visual overlay (for sighted helpers/developers)
        cv2.putText(annotated_frame, f"Dristi Active | FPS: {fps:.1f}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        status = "AUTO-NARRATION: ON" if auto_narrate else "Listening for commands..."
        color = (0, 255, 255) if auto_narrate else (255, 255, 255)
        cv2.putText(annotated_frame, status, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        cv2.putText(annotated_frame, f"Objects: {len(detected_objects)}", 
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        
        cv2.imshow('Dristi Voice Assistant (Helper View)', annotated_frame)
        
        # Handle keyboard commands
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            speak("Shutting down Dristi. Stay safe. Goodbye.")
            break
        
        elif key == ord(' '):  # Full description
            if current_scene:
                speak("Analyzing environment")
                description = generate_voice_description(detected_objects, current_scene, 'full')
                speak(description)
                last_description = description
            else:
                speak("Still analyzing. Please wait.")
        
        elif key == ord('h'):  # Hazards
            description = generate_voice_description(detected_objects, current_scene, 'hazards')
            speak(description)
            last_description = description
        
        elif key == ord('l'):  # Location
            if current_scene:
                description = generate_voice_description(detected_objects, current_scene, 'location')
                speak(description)
                last_description = description
            else:
                speak("Determining location. Please wait.")
        
        elif key == ord('o'):  # Objects
            description = generate_voice_description(detected_objects, current_scene, 'objects')
            speak(description)
            last_description = description
        
        elif key == ord('p'):  # People
            description = generate_voice_description(detected_objects, current_scene, 'people')
            speak(description)
            last_description = description
        
        elif key == ord('r'):  # Repeat
            if last_description:
                speak(last_description)
            else:
                speak("No previous description available")
        
        elif key == ord('a'):  # Toggle auto-narration
            auto_narrate = not auto_narrate
            if auto_narrate:
                speak("Auto narration enabled. I will describe your surroundings every 15 seconds.")
                last_narration_time = current_time
            else:
                speak("Auto narration disabled. Press space for descriptions.")

except KeyboardInterrupt:
    speak("System interrupted")

finally:
    cap.release()
    cv2.destroyAllWindows()
    speak("Dristi shutdown complete. Thank you for using Dristi.", async_mode=False)
    print("\n✅ Voice assistant closed successfully")
    print("=" * 70)