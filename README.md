# DRISTI - Vision-Based Voice Assistant for Visually Impaired Users

A comprehensive AI-powered vision system that combines object detection, depth estimation, and scene understanding to provide real-time audio descriptions for visually impaired users.

## 🎯 Project Overview

**Dristi** (meaning "vision" in Sanskrit) is a semester project that creates an accessible vision assistance system using state-of-the-art deep learning models. The system processes real-time camera feed to provide voice-based environmental awareness.

### Key Features

- **Real-time Object Detection** using YOLOv8
- **Depth Estimation** using MiDaS
- **Scene Understanding** using CLIP
- **Text-to-Speech** output for accessibility
- **Modular Architecture** for easy integration and extension
- **Hazard Detection** prioritizing user safety
- **Auto-narration** capability for continuous awareness

## 🏗️ System Architecture

```
Camera Input
    ↓
[Object Detector] → Identifies objects in scene
    ↓
[Depth Estimator] → Estimates object distances
    ↓
[Scene Analyzer] → Understands context
    ↓
[Voice Engine] → Generates speech output
    ↓
User (Audio Output)
```

### Module Structure

```
src/
├── vision/
│   ├── object_detector.py    # YOLOv8-based detection
│   ├── depth_estimator.py    # MiDaS depth estimation
│   └── scene_analyzer.py     # CLIP-based scene understanding
├── audio/
│   └── voice_engine.py       # pyttsx3 text-to-speech
└── core/
    └── dristi_system.py      # Main integration system
```

## 📋 Requirements

- Python 3.8+
- Webcam/Camera
- 4GB+ RAM (8GB+ recommended)
- GPU recommended (but CPU works)

## 🚀 Quick Start

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

**🎯 OPTIMIZED VERSION (RECOMMENDED):**
```bash
python app_optimized.py
```
- Interactive setup for your hardware
- Better performance (15+ FPS)
- Configurable modules
- **Start here!**

**Full-Featured Version (All Modules):**
```bash
python app.py
```

**Individual Module Tests:**
```bash
python 01_camera_test.py
python 02_download_yolo.py
python 03_object_detection.py
python 04_depth_estimation_midas.py
python 05_scene_understanding.py
python 06_voice_assistant.py
```

See [QUICK_START.md](QUICK_START.md) for detailed setup instructions.

## 🎮 Voice Commands

When running the integrated application (`app.py`):

| Key | Command | Description |
|-----|---------|-------------|
| `SPACE` | What do you see? | Full comprehensive description |
| `h` | Hazards? | Safety check - identifies obstacles/dangers |
| `l` | Where am I? | Location/scene type description |
| `o` | Objects? | Lists detected objects |
| `p` | People? | Count of people nearby |
| `r` | Repeat | Repeat last description |
| `a` | Auto-narrate | Toggle continuous narration (every 15 sec) |
| `d` | Depth view | Toggle depth map visualization |
| `s` | Screenshot | Save current frame |
| `q` | Quit | Exit application |

## 🔧 Module Details

### Object Detector (`vision/object_detector.py`)
- **Model**: YOLOv8 nano
- **Classes**: 80 COCO classes (persons, vehicles, animals, etc.)
- **Output**: Bounding boxes, class names, confidence scores

### Depth Estimator (`vision/depth_estimator.py`)
- **Model**: MiDaS small
- **Output**: Depth maps, distance categorization (Very Close, Close, Medium, Far, Very Far)
- **Uses**: Assigns distance to detected objects

### Scene Analyzer (`vision/scene_analyzer.py`)
- **Model**: CLIP ViT-B/32
- **Analysis**: Scene type, environmental condition, human activity
- **Examples**: "indoor room", "outdoor area", "crowded place", etc.

### Voice Engine (`audio/voice_engine.py`)
- **Engine**: pyttsx3
- **Features**: Adjustable speed, volume, voice selection
- **Modes**: Full, hazards, location, objects, people

### Dristi System (`core/dristi_system.py`)
- **Integration**: Combines all modules
- **State Management**: FPS, frame count, scene state
- **Command Handling**: Processes user input

## 📊 Performance

### Optimized Version (app_optimized.py)
- **FPS**: 15-20 FPS on Intel i5/i7 (configurable)
- **Latency**: ~100ms per command
- **Detection Accuracy**: 85%+ in good lighting
- **Memory**: ~400-800MB (depends on modules)

### Performance Profiles
| Hardware | Default | Low-Power | High-Quality |
|----------|---------|-----------|--------------|
| i5 + 8GB | 12-15 FPS | 15-18 FPS | N/A |
| i7 + 16GB | 15-18 FPS | 18-25 FPS | 20-25 FPS |
| i7 + GPU | 20-25 FPS | 25-30 FPS | 30+ FPS |

**See [OPTIMIZATION.md](OPTIMIZATION.md) for detailed tuning guide.**

## 🛡️ Safety Features

- **Hazard Detection**: Identifies vehicles, obstacles, animals
- **Priority System**: Emphasizes dangerous objects first
- **Distance Awareness**: Uses depth to warn of close objects
- **Obstacle Avoidance**: Tracks path hazards

## 📁 Project Files

### Main Applications
- `app_optimized.py` - **🎯 OPTIMIZED VERSION** (Start here for performance!)
  - Interactive hardware configuration
  - Configurable FPS and resolution
  - Optional module disable
  - Best for most systems

- `app.py` - Full-featured integrated application (all modules enabled)
- `main.py` - Menu-based module selector

### Individual Modules (Legacy)
- `01_camera_test.py` - Camera accessibility test
- `02_download_yolo.py` - Download YOLO model
- `03_object_detection.py` - Real-time object detection demo
- `04_depth_estimation_midas.py` - Depth estimation demo
- `05_scene_understanding.py` - Scene analysis demo
- `06_voice_assistant.py` - Voice assistant demo

### Supporting Files
- `requirements.txt` - Python dependencies
- `config.yaml` - Configuration template
- `QUICK_START.md` - Quick reference guide
- `OPTIMIZATION.md` - Detailed performance tuning
- `documentations/system_architecture.md` - Architecture details
- `data/` - Data and models directory
- `runs/` - Output and results directory

## 🔌 Integration Notes

The integrated `app.py` combines:
1. ✅ Object detection from module 03
2. ✅ Depth estimation from module 04
3. ✅ Scene understanding from module 05
4. ✅ Voice output from module 06
5. ✅ Unified control system

All modules work together seamlessly through the `DristiSystem` class.

## 🎓 Semester Project Checklist

- ✅ Real-time object detection (YOLOv8)
- ✅ Depth estimation (MiDaS)
- ✅ Scene understanding (CLIP)
- ✅ Voice interface (pyttsx3)
- ✅ Hazard detection
- ✅ Modular architecture
- ✅ Integrated main application
- ✅ Comprehensive documentation

## 🐛 Troubleshooting

### Camera not accessible
```bash
# Check camera availability
python 01_camera_test.py

# Try different camera index
# Edit app.py: cv2.VideoCapture(0) → cv2.VideoCapture(1)
```

### Model download issues
```bash
# Clear torch cache
rm -rf ~/.cache/torch/hub

# Re-run download
python 02_download_yolo.py
```

### Voice not working
- Check speaker/headphone connection
- Verify pyttsx3 installation: `pip install --upgrade pyttsx3`
- Ensure TTS engine is available on your system

### Low FPS
- Use smaller frame resolution
- Reduce detection frequency in `app.py`
- Use GPU if available: Add CUDA support to PyTorch

## 📚 References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [MiDaS Depth Estimation](https://github.com/isl-org/MiDaS)
- [CLIP: Learning Transferable Models](https://github.com/openai/CLIP)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)

## 📝 License

This is a semester project. Use for educational purposes.

## 👨‍💻 Development

### Adding New Features
1. Create module in appropriate directory under `src/`
2. Inherit from base class (if applicable)
3. Integrate with `DristiSystem` in `src/core/dristi_system.py`
4. Update `app.py` to use new module

### Testing Individual Modules
```bash
# Test vision modules
python src/vision/object_detector.py

# Test audio modules
python src/audio/voice_engine.py

# Test core system
python app.py
```

## 🎯 Future Enhancements

- [ ] Real-time pose detection
- [ ] Activity recognition
- [ ] Voice command input (STT)
- [ ] Mobile app integration
- [ ] Cloud processing support
- [ ] Multi-language support
- [ ] Customizable alerts
- [ ] Data logging and analytics

---

**Made with ❤️ for accessibility**

For questions or issues, check the documentation in `documentations/` directory.
