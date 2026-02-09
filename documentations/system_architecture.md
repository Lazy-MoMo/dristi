# Dristi System Architecture

## Overview
Dristi is a vision-based voice assistant for visually impaired users.

## System Components

### 1. Vision Module
- **Object Detection**: YOLOv8 nano
- **Depth Estimation**: MiDaS small (optional)
- **Scene Understanding**: CLIP ViT-B/32

### 2. Activity Recognition
- **Pose Detection**: MediaPipe Pose
- **Activity Classification**: Rule-based + temporal analysis

### 3. Natural Language Generation
- Feature fusion from all modules
- Context-aware description generation
- Safety-first priority system

### 4. Voice Interface
- **TTS Engine**: pyttsx3
- Async speech for non-blocking operation
- Customizable voice parameters

## Data Flow
Camera → Object Detection → Scene Analysis → Activity Detection → 
Description Generation → Text-to-Speech → User

## Performance Metrics
- FPS: 15-20 on Intel i7-1165G7
- Latency: < 100ms per frame
- Detection Accuracy: 85%+ in good lighting