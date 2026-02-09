# DRISTI Charts and Diagrams

## 📊 Available Chart Files

### Interactive HTML Version (Recommended)
- **`charts.html`** - Open in any web browser to view all 6 diagrams interactively
  - Click to view, right-click to save as PNG
  - Print to PDF with Ctrl+P
  - Fully responsive and interactive

### Mermaid Source Files
Raw diagram source code that can be edited and regenerated:

1. **`1_system_architecture.mmd`** - Complete system data flow
2. **`2_gpu_performance.mmd`** - GPU metrics and performance
3. **`3_voice_commands.mmd`** - Voice command processing
4. **`4_module_dependencies.mmd`** - Module relationships
5. **`5_gpu_memory.mmd`** - GPU memory allocation
6. **`6_processing_timeline.mmd`** - Frame processing timeline

## 🎨 How to View Charts

### Option 1: Open HTML File (Easiest)
```bash
# Open in default browser
open charts.html

# Or with specific browser
firefox charts.html
chromium charts.html
```

### Option 2: Online Mermaid Editor
1. Go to https://mermaid.live
2. Copy content from any `.mmd` file
3. Paste into editor to view/edit

### Option 3: Generate Images (Requires mermaid-cli)
```bash
# Install (if not already installed)
npm install -g @mermaid-js/mermaid-cli

# Convert to PNG
mmdc -i 1_system_architecture.mmd -o 1_system_architecture.png

# Convert to PDF
mmdc -i 1_system_architecture.mmd -o 1_system_architecture.pdf
```

## 💾 Save as Images

### From HTML File
1. Open `charts.html` in browser
2. Right-click on any diagram
3. "Save image as..." → Choose PNG location
4. Or use Ctrl+P to print to PDF

### From Mermaid Files Online
1. Go to https://mermaid.live
2. Paste mermaid code
3. Click "Download" button
4. Choose PNG, PDF, or SVG format

## 📈 Chart Descriptions

### 1. System Architecture Diagram
Shows the complete DRISTI pipeline:
- Camera input → Frame processing
- Three parallel GPU modules (Detection, Depth, Analysis)
- Voice output and display rendering
- User command handling

**Use case:** Understanding overall system flow

### 2. GPU Performance Metrics
Displays performance characteristics:
- Speed per operation (20-100ms)
- Memory allocation (200-250MB per module)
- Processing frequency (every frame to every 30 frames)
- Overall FPS and latency targets

**Use case:** Performance planning and optimization

### 3. Voice Command Processing Flow
Details how user input is processed:
- 10 supported keyboard commands
- Routing to appropriate description generator
- Async TTS output handling
- Display/depth visualization updates

**Use case:** Understanding user interface behavior

### 4. Module Dependencies
Shows code organization and relationships:
- app.py and app_optimized.py entry points
- Core system coordinator
- Vision modules (Object detection, Depth, Scene)
- Audio output engine
- Hardware dependencies (PyTorch, OpenCV, GPU)

**Use case:** Understanding code structure

### 5. GPU Memory Allocation
Visual breakdown of GPU memory usage:
- YOLO: 200MB (21%)
- MiDaS: 150MB (16%)
- CLIP: 250MB (27%)
- Overhead: 106MB (10%)
- **Available: 1390MB (83%)**

**Use case:** Resource planning and optimization

### 6. Processing Pipeline Timeline
Shows frame processing timing:
- 66.67ms per frame @ 15 FPS target
- Parallel GPU operations
- Sleep scheduling to maintain FPS
- Non-blocking TTS handling

**Use case:** Performance debugging and optimization

## 🔧 Edit Diagrams

### Edit Mermaid Files
```bash
# Edit any .mmd file
nano 1_system_architecture.mmd

# Or use your favorite editor
vim 4_module_dependencies.mmd
code 5_gpu_memory.mmd
```

### Edit HTML Charts
Open `charts.html` in text editor:
```bash
vim charts.html
```

Replace mermaid code blocks between `<div class="mermaid">` and `</div>`

## 📊 Export Workflows

### To PDF (From HTML)
```bash
# Using Firefox
firefox --print-to-pdf charts.html output.pdf

# Or print manually
# Ctrl+P in browser → Save as PDF
```

### To PNG (Individual Diagrams)
```bash
# If mermaid-cli is installed
for i in *.mmd; do
  mmdc -i "$i" -o "${i%.mmd}.png"
done
```

### To PowerPoint/Slides
1. Save as PDF
2. Insert PDF pages into presentation software
3. Or screenshot from browser and insert PNG

## 📱 View on Different Devices

### Mobile/Tablet
- Open `charts.html` in mobile browser
- Charts are responsive
- Pinch to zoom
- Right-tap to save

### Desktop
- Open in Chrome, Firefox, Safari, Edge
- Right-click → Save image as PNG
- Ctrl+P to print

### Print-Friendly
- Open `charts.html`
- Ctrl+P (Cmd+P on Mac)
- Select "Print to file" or PDF printer
- Adjust margins as needed

## 🎯 Use Cases

| Chart | Best For | Output Format |
|-------|----------|---------------|
| System Architecture | Documentation, training | PDF |
| GPU Performance | Reports, presentations | PNG |
| Voice Commands | User manual, quick ref | PNG |
| Module Dependencies | Code review, onboarding | PDF |
| GPU Memory | Resource planning | PNG |
| Processing Timeline | Performance analysis | PDF |

## 📚 Related Documentation

- **METRICS_AND_PERFORMANCE.md** - Detailed metrics and benchmarks
- **GPU_OPTIMIZATION_SUMMARY.md** - GPU optimization techniques
- **FIXED_ISSUES.md** - Issues fixed and solutions

## 🚀 Quick Links

- **View all charts**: Open `charts.html` in browser
- **Edit diagrams**: Use mermaid.live or edit `.mmd` files
- **Generate images**: Use mermaid-cli or web services
- **Share diagrams**: Export as PDF or PNG from HTML

## 📝 Notes

- All diagrams are auto-generated from Mermaid code
- Charts update automatically when source code changes
- No external image files needed (except for exports)
- Fully compatible with all modern browsers
- Print-friendly styling included

## 🆘 Troubleshooting

### Charts not displaying in HTML
- Refresh browser (Ctrl+F5)
- Check internet connection (needs mermaid.js from CDN)
- Try different browser
- Clear browser cache

### mermaid-cli not working
```bash
# Reinstall if broken
npm install -g @mermaid-js/mermaid-cli

# Set puppeteer cache
export PUPPETEER_CACHE_DIR=/tmp/puppeteer
mmdc -i chart.mmd -o chart.png
```

### Can't save from HTML
- Use browser's built-in screenshot tool (Shift+S in Chrome)
- Try right-click → "Open image in new tab" → Save
- Print to PDF instead
- Use Snipping Tool / Screenshot on Windows/Mac

## 📞 Support

For issues with:
- **Charts display**: Check browser compatibility
- **Mermaid syntax**: See https://mermaid.js.org/
- **DRISTI app**: See README.md and documentation files
