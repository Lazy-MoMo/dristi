# DRISTI - Quick Start Guide

## Installation & Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Best for Performance (Recommended)
```bash
python app_optimized.py
```

This starts an interactive setup:
- Asks for FPS preference (default: 15)
- Asks for resolution (default: 640px)
- Asks to enable/disable modules
- Starts optimized system

### Full-Featured (All Modules)
```bash
python app.py
```

Runs with all features enabled (may lag on weak hardware)

### Individual Tests
```bash
# Test camera
python 01_camera_test.py

# Download/test YOLO
python 02_download_yolo.py

# Test each module
python 03_object_detection.py
python 04_depth_estimation_midas.py
python 05_scene_understanding.py
python 06_voice_assistant.py
```

## Voice Commands

Once running, use keyboard to control:

| Key | Action |
|-----|--------|
| **SPACE** | Full description of scene |
| **h** | Check for hazards |
| **l** | Where am I? (location) |
| **o** | List objects |
| **p** | Count people |
| **r** | Repeat last description |
| **a** | Toggle auto-narration |
| **d** | Toggle depth visualization |
| **s** | Save screenshot |
| **q** | Quit |

## Performance Tips

### System Lagging?

**Quick Fix:**
```bash
python app_optimized.py
# Select: FPS=10, Width=480, Scene=n, Depth=n
```

**For Weak Hardware:**
1. Close other applications
2. Disable scene analysis (use `-s` flag)
3. Lower frame width to 480px
4. Target FPS: 10-12

**For Good Hardware:**
1. Enable depth estimation
2. Keep scene analysis on
3. Frame width: 640-1280px
4. Target FPS: 15-20

## Troubleshooting

### Camera Not Working
```bash
python 01_camera_test.py
# If fails, check camera permissions or try different camera index
```

### Models Not Downloading
```bash
# Clear cache
rm -rf ~/.cache/torch/hub

# Re-download
python 02_download_yolo.py
```

### Audio/Voice Issues
- Check speakers/headphones connected
- Verify volume is not muted
- Try: `python -c "import pyttsx3; pyttsx3.init().say('test'); pyttsx3.init().runAndWait()"`

### Memory Issues
- Disable depth: `app = OptimizedDristiApp(enable_depth=False)`
- Disable scene: `app = OptimizedDristiApp(enable_scene=False)`
- Close other applications

## Configuration

Edit performance manually:

```python
# In app_optimized.py, modify:

app = OptimizedDristiApp(
    enable_depth=False,      # Disable depth estimation
    enable_scene=True,       # Keep scene analysis
    target_fps=15,           # Target FPS
    frame_width=640          # Frame resolution
)
```

Or use config file:
```bash
# Edit config.yaml
nano config.yaml

# Then load it in app (feature coming soon)
```

## Project Structure

```
dristi/
├── app.py                      # Full-featured version
├── app_optimized.py            # Optimized version (USE THIS!)
├── config.yaml                 # Configuration file
├── OPTIMIZATION.md             # Detailed tuning guide
│
├── src/
│   ├── vision/
│   │   ├── object_detector.py
│   │   ├── depth_estimator.py
│   │   └── scene_analyzer.py
│   ├── audio/
│   │   └── voice_engine.py
│   └── core/
│       └── dristi_system.py
│
├── 01_camera_test.py           # Individual module tests
├── 02_download_yolo.py
├── 03_object_detection.py
├── 04_depth_estimation_midas.py
├── 05_scene_understanding.py
├── 06_voice_assistant.py
│
├── requirements.txt
├── README.md                   # Full documentation
└── OPTIMIZATION.md             # Performance guide
```

## For Your Semester Project

**Main deliverable:** `app_optimized.py`

**What it demonstrates:**
- ✅ Real-time object detection (YOLOv8)
- ✅ Depth estimation (MiDaS) - optional
- ✅ Scene understanding (CLIP) - optional
- ✅ Voice interface (pyttsx3)
- ✅ Integrated system architecture
- ✅ Performance optimization
- ✅ Modular design
- ✅ Hazard detection

**How to run for demo:**
```bash
python app_optimized.py
# Keep defaults or customize for your system
# Demonstrate voice commands (SPACE, h, l, o, p)
```

## Expected Performance

### Minimum Setup
- Intel i5 or equivalent
- 8GB RAM
- Integrated graphics
- **Expected:** 10-15 FPS (with scene analysis disabled)

### Recommended Setup
- Intel i7 or equivalent
- 16GB RAM
- Dedicated GPU (optional)
- **Expected:** 15-20 FPS (all features)

### Ideal Setup
- Intel i7+ / Ryzen 5+
- 16GB+ RAM
- RTX GPU
- **Expected:** 25-30 FPS (all features)

## Next Steps

1. **Run:** `python app_optimized.py`
2. **Configure:** Based on your hardware
3. **Test:** Voice commands in order
4. **Optimize:** If lagging, see OPTIMIZATION.md
5. **Present:** Demonstrate all features

---

For detailed information, see:
- `README.md` - Full documentation
- `OPTIMIZATION.md` - Performance tuning
- `documentations/system_architecture.md` - Architecture details
