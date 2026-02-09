# DRISTI - Vision-Based Voice Assistant for Visually Impaired Users

A comprehensive AI-powered real-time vision system that combines object detection, depth estimation, and scene understanding to provide audio descriptions for visually impaired users. Optimized for GPU acceleration with graceful CPU fallback.

## 🎯 Project Overview

**Dristi** (meaning "vision" in Sanskrit) is a semester project that creates an accessible vision assistance system using state-of-the-art deep learning models. The system processes live camera feed to provide voice-based environmental awareness, hazard detection, and scene comprehension.

### Project Status
- ✅ **Core Features**: Fully implemented and tested
- ✅ **GPU Optimization**: CUDA-accelerated with CPU fallback
- ✅ **Modular Architecture**: Decoupled vision, audio, and core modules
- ✅ **Two Deployment Options**: Full-featured and optimized versions
- 🔄 **Active Development**: Performance improvements and feature enhancements

## 🌟 Key Features

- **Real-time Object Detection** - YOLOv8 nano with GPU acceleration (80%+ accuracy)
- **Depth Estimation** - MiDaS-based distance awareness with 5-category classification
- **Scene Understanding** - CLIP-based semantic scene analysis (indoor/outdoor, lighting, activity)
- **Intelligent Hazard Detection** - Priority-based warnings for vehicles, obstacles, and animals
- **Natural Language Descriptions** - Context-aware voice output with multiple query modes
- **Auto-Narration** - Continuous environmental awareness every 15 seconds
- **Optimized Performance** - 15-30 FPS depending on hardware (with GPU: 20-25+ FPS)
- **Hardware Flexibility** - Runs on CPU or GPU, configurable FPS/resolution

## 📊 Architecture

```
┌─────────────┐
│  Camera     │
└──────┬──────┘
       │
       ▼
┌──────────────────────────────────────┐
│     DRISTI SYSTEM (Core)             │
├──────────────────────────────────────┤
│ ┌──────────────────────────────────┐ │
│ │ VISION MODULES                   │ │
│ ├──────────────────────────────────┤ │
│ │ • ObjectDetector (YOLOv8)        │ │
│ │ • DepthEstimator (MiDaS)         │ │
│ │ • SceneAnalyzer (CLIP)           │ │
│ └──────────────────────────────────┘ │
│ ┌──────────────────────────────────┐ │
│ │ AUDIO MODULE                     │ │
│ ├──────────────────────────────────┤ │
│ │ • VoiceEngine (pyttsx3)          │ │
│ │ • Description Generator          │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│   TEXT-TO-SPEECH OUTPUT              │
│   (Speaker/Headphones)               │
└──────────────────────────────────────┘
```

## 📁 Project Structure

```
dristi/
├── src/                              # Core application modules
│   ├── vision/
│   │   ├── object_detector.py        # YOLOv8 COCO detection (GPU optimized)
│   │   ├── depth_estimator.py        # MiDaS depth + distance categorization
│   │   └── scene_analyzer.py         # CLIP scene understanding
│   ├── audio/
│   │   └── voice_engine.py           # pyttsx3 TTS + description generation
│   └── core/
│       └── dristi_system.py          # Main integration & orchestration
│
├── app.py                            # Full-featured integrated application
├── app_optimized.py                  # Performance-optimized with GPU acceleration
├── main.py                           # Module selector menu
├── config.yaml                       # Configuration profiles (low-power, balanced, high-quality)
│
├── documentations/
│   └── system_architecture.md        # Detailed architecture documentation
│
├── runs/                             # Output directory for screenshots
├── data/
│   └── models/                       # Downloaded AI models
│
└── requirements.txt                  # Python dependencies
```

## 📋 System Requirements

### Hardware
- **Processor**: Intel Core i5/i7 or equivalent (GPU recommended)
- **RAM**: 4GB minimum (8GB+ recommended)
- **GPU**: NVIDIA CUDA-capable GPU (CUDA compute capability 3.5+)
- **Camera**: USB webcam or integrated camera

### Software
- **Python**: 3.8+
- **CUDA**: 11.8+ (optional, for GPU acceleration)
- **cuDNN**: 8.0+ (optional, for GPU acceleration)

### Dependencies
```
opencv-python >= 4.13.0
torch >= 2.0.0
torchvision (via torch)
numpy >= 2.0.0
ultralytics >= 8.0.0
timm >= 0.9.0
pyttsx3 >= 2.90
Pillow >= 9.0.0
CLIP (via git+https://github.com/openai/CLIP.git)
```

## 🚀 Getting Started

### 1. Clone Repository
```bash
git clone https://github.com/Lazy-MoMo/dristi
cd dristi
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download YOLO Model
```bash
python 02_download_yolo.py
```

### 5. Run Application

**🎯 OPTIMIZED VERSION (RECOMMENDED)**
```bash
python app_optimized.py
```
Interactive GPU-optimized version with configuration options:
- Choose target FPS (5-30)
- Set frame width (320-1280)
- Enable/disable depth estimation
- Enable/disable scene analysis

**Full-Featured Version**
```bash
python app.py
```
All modules enabled by default (higher resource usage).

**Legacy Module Menu**
```bash
python main.py
```
Run individual modules separately for testing.

## 🎮 Voice Commands

When the application is running, use these keys to query your environment:

| Key | Command | Description |
|-----|---------|-------------|
| `SPACE` | What do you see? | Full scene analysis & object description |
| `h` | Hazards? | Safety check (vehicles, obstacles, animals) |
| `l` | Where am I? | Location/scene type identification |
| `o` | Objects? | Detailed object list with counts |
| `p` | People? | Count of people nearby |
| `r` | Repeat | Repeat last description |
| `a` | Auto-narrate | Toggle continuous narration (every 15 sec) |
| `d` | Depth view | Toggle depth map visualization (if available) |
| `s` | Screenshot | Save current frame to disk |
| `q` | Quit | Exit application |

## 🔧 Module Details

### Vision Modules

#### ObjectDetector (`src/vision/object_detector.py`)
- **Model**: YOLOv8 nano (3.2M parameters)
- **Classes**: 80 COCO dataset classes
- **Input Size**: Configurable (320-416px for speed/accuracy tradeoff)
- **GPU Optimization**: 
  - Input resizing before detection
  - GPU warmup on initialization
  - Thread-safe detection caching
- **Output**: Bounding boxes, class names, confidence scores (0-1)
- **Performance**: 
  - GPU: 50-80 FPS at 320px input
  - CPU: 8-12 FPS

#### DepthEstimator (`src/vision/depth_estimator.py`)
- **Model**: MiDaS small (efficient version)
- **Distance Categories**: 5-level classification
  - Very Close (< 0.5m) - Red
  - Close (0.5-1m) - Orange
  - Medium (1-2m) - Yellow
  - Far (2-3m) - Green
  - Very Far (> 3m) - Dark Green
- **GPU Acceleration**: GPU tensor operations, CPU transfer on output only
- **Output**: Normalized depth map, colored visualization, distance estimates
- **Performance**: 20-40 FPS (GPU-accelerated)

#### SceneAnalyzer (`src/vision/scene_analyzer.py`)
- **Model**: CLIP ViT-B/32 (vision-language model)
- **Analysis Types**: 
  - **Scene Type**: 10 categories (indoor, outdoor, kitchen, bedroom, office, etc.)
  - **Environmental Condition**: 6 categories (crowded, quiet, bright, dark, clean, cluttered)
  - **Activity**: 6 categories (walking, sitting, working, eating, talking, none)
- **Batch Processing**: All text encodings done at once on GPU
- **Confidence Scores**: Top-2 predictions for scene type, single for conditions/activity
- **Performance**: 5-15 FPS (CLIP is computationally intensive)

### Audio Module

#### VoiceEngine (`src/audio/voice_engine.py`)
- **TTS Engine**: pyttsx3 (cross-platform offline TTS)
- **Voice Options**: System-provided male/female voices
- **Speech Rate**: 50-300 words per minute (default: 150)
- **Volume**: 0.0-1.0 scale
- **Threading**: Async (non-blocking) speech for responsive UI
- **Description Modes**:
  - **Full**: Scene context + hazards + priority objects + counts
  - **Hazards**: Vehicles, obstacles, animals with warnings
  - **Location**: Scene type identification
  - **Objects**: Detected object list with smart grouping
  - **People**: People count in view

### Core System

#### DristiSystem (`src/core/dristi_system.py`)
- **Integration Hub**: Orchestrates all modules
- **State Management**: FPS tracking, frame counting, scene caching
- **Processing Intervals** (GPU-optimized):
  - Detection: Every frame (GPU is fast)
  - Depth: Every 2 frames (GPU-accelerated)
  - Scene Analysis: Every 30 frames (computationally heavy)
- **Auto-Narration**: Optional continuous descriptions
- **Command Handling**: Keyboard input processing
- **Visual Overlay**: FPS, status, object count, scene type display

## 📊 Performance Metrics

### Actual Performance (Tested on Intel i7-1165G7, 8GB RAM)

**Object Detection Accuracy**
- Detection Rate: 80%+ for common objects
- False Positives: <5% at confidence 0.5
- Confidence Range: 65-92% for detected objects
- Processing: ~55ms per frame (18 FPS)

**Overall System Performance**

| Hardware | Configuration | FPS | Latency | Memory |
|----------|---------------|-----|---------|---------|
| Intel i5 + CPU | Detection only | 8-12 | 80ms | 300-400MB |
| Intel i7 + CPU | + Scene analysis | 10-15 | 100ms | 400-600MB |
| NVIDIA GPU | All modules | 20-25 | 40-50ms | 800-1200MB |
| NVIDIA GPU | Optimized (320px) | 25-30 | 30-40ms | 600-800MB |

### Optimization Profiles (config.yaml)

**Low-Power Profile** (for older/slower hardware)
- 480px resolution, 10 FPS
- Detection only, depth/scene disabled
- Best for: Older laptops, single-core systems

**Balanced Profile** (recommended)
- 640px resolution, 15 FPS
- Object detection + scene analysis
- Depth disabled for speed
- Best for: Typical laptops/desktops

**High-Quality Profile** (for modern GPUs)
- 1280px resolution, 20+ FPS
- All modules enabled
- Best for: NVIDIA GPUs, real-time applications

## 🛡️ Safety Features

### Hazard Detection System
- **Vehicle Detection**: Cars, trucks, buses, motorcycles, bicycles
- **Obstacle Detection**: Benches, fire hydrants, parking meters
- **Animal Detection**: Dogs, cats, birds, horses
- **Traffic Signs**: Traffic lights, stop signs
- **Priority Warning**: Hazards announced before general descriptions

### Distance Awareness
- Real-time depth estimation for each detected object
- Distance categorization from depth maps
- Integration into descriptions: "Vehicle at medium distance"

### Voice Feedback
- Async speech for non-blocking operation
- Multiple description modes for different query types
- Repeat capability for clarification

## 🧠 AI Models Used

| Module | Model | Source | Size | GPU Memory |
|--------|-------|--------|------|-----------|
| Object Detection | YOLOv8 nano | Ultralytics | 6.3MB | 200MB |
| Depth Estimation | MiDaS small | Intel ISL | 49MB | 400MB |
| Scene Understanding | CLIP ViT-B/32 | OpenAI | 340MB | 600MB |

**Note**: First run downloads models automatically. Total: ~400MB

## 🧪 Testing Individual Modules

Each module can be tested independently:

```bash
# Test 1: Camera access
python 01_camera_test.py

# Test 2: Download YOLO model
python 02_download_yolo.py

# Test 3: Object detection
python 03_object_detection.py

# Test 4: Depth estimation
python 04_depth_estimation_midas.py

# Test 5: Scene understanding
python 05_scene_understanding.py

# Test 6: Voice assistant
python 06_voice_assistant.py
```

See `test_results.txt` for sample test output and accuracy benchmarks.

## 🔌 Configuration

Edit `config.yaml` to customize:

```yaml
display:
  window_width: 640
  target_fps: 15
  show_overlay: true

modules:
  object_detection:
    enabled: true
    confidence: 0.5
    input_size: 320
    process_every_n_frames: 2

  depth_estimation:
    enabled: true
    scale: 0.5
    process_every_n_frames: 2

  scene_analysis:
    enabled: true
    process_every_n_frames: 60

audio:
  speech_rate: 150
  volume: 1.0
  narration_interval: 15
```

## 🐛 Troubleshooting

### Camera Not Accessible
```bash
# Check camera
python 01_camera_test.py

# Try different camera index
# Edit app.py line 66: for camera_index in range(5):
```

### CUDA Out of Memory
```bash
# Reduce frame resolution in app_optimized.py
# Or disable depth/scene analysis
# Or use CPU: modify device parameter
```

### Model Download Issues
```bash
# Clear PyTorch cache
rm -rf ~/.cache/torch/hub

# Clear pip cache
pip cache purge

# Re-run model setup
python 02_download_yolo.py
```

### Voice Not Working
```bash
# Check speaker connection
# Reinstall pyttsx3
pip install --upgrade pyttsx3

# Verify TTS engine
python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"
```

### Low FPS
- Reduce frame width (640 → 480)
- Disable depth estimation (`enable_depth=False`)
- Lower target FPS temporarily
- Use GPU if available (CUDA preferred)

## 👨‍💻 Development Guide

### Project Architecture

The project follows a modular design:

1. **Vision Modules** (`src/vision/`): Independent detection, depth, scene analysis
2. **Audio Module** (`src/audio/`): Speech synthesis and description generation
3. **Core System** (`src/core/`): Integration and orchestration
4. **Application Layer**: Two variants (full and optimized)

### Adding New Features

1. Create module in appropriate `src/` directory
2. Implement consistent interface with type hints
3. Integrate into `DristiSystem` class
4. Add configuration options to `config.yaml`
5. Update application files to use new module

### Code Quality Standards

- Follow PEP 8 style guide
- Add type hints to all functions
- Include comprehensive docstrings
- Use thread-safe operations for concurrent access
- Test on both CPU and GPU

### Testing Checklist

- [ ] Module works independently
- [ ] Works with other modules in DristiSystem
- [ ] Handles errors gracefully
- [ ] Performance acceptable on target hardware
- [ ] Documentation updated

## 📚 References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [MiDaS Depth Estimation](https://github.com/isl-org/MiDaS)
- [CLIP Vision-Language Model](https://github.com/openai/CLIP)
- [pyttsx3 TTS Documentation](https://pyttsx3.readthedocs.io/)
- [PyTorch Documentation](https://pytorch.org/docs/)

## 🎯 Future Enhancements

- [ ] Real-time pose detection and body positioning
- [ ] Activity recognition (sitting, walking, running)
- [ ] Voice command input (speech-to-text)
- [ ] Mobile app integration (iOS/Android)
- [ ] Cloud processing support for heavier models
- [ ] Multi-language support (Spanish, Hindi, etc.)
- [ ] Customizable alert thresholds
- [ ] Data logging and analytics dashboard
- [ ] User profile preferences
- [ ] Wearable device integration

## 🤝 Contributing

We welcome contributions! Please:

1. **Fork** the repository
2. **Create branch**: Use descriptive names (`feature/pose-detection`, `fix/cuda-memory`)
3. **Test thoroughly**: Verify on CPU and GPU
4. **Update documentation**: Add docstrings and examples
5. **Commit clearly**: Descriptive commit messages
6. **Submit PR**: Include testing results and hardware specs

### Reporting Issues

When reporting bugs, please include:
- System specs (OS, Python version, GPU/CPU model)
- Installed package versions (`pip list`)
- Reproduction steps
- Error logs/tracebacks
- Screenshots if applicable

## 📄 License

Educational project. Use for learning and research purposes.

## 📖 Documentation

- Architecture: `documentations/system_architecture.md`
- Configuration: See `config.yaml` comments
- Testing: See `test_results.txt`

## 👥 Authors

**Abhishek H** - Project Creator and Developer

## 🙏 Acknowledgments

- Ultralytics for YOLOv8
- Intel ISL for MiDaS
- OpenAI for CLIP
- PyTorch foundation
- Python community

---

**Made with ❤️ for accessibility and inclusivity**

For questions or suggestions, open an issue on GitHub.

**Last Updated**: February 2025 | **Version**: 1.0 | **Status**: Stable
