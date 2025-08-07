# 📁 Local Videos Guide

## 🎯 Easy Local Video Processing

Your Video Processing Suite now uses a special `local_videos/` folder for convenient video management. No more typing long file paths!

## 🚀 Quick Start

1. **Add videos to process**: Place your videos in the `local_videos/` folder
2. **List available videos**: `python main.py list`
3. **Process videos easily**: Use video names or numbers instead of full paths

## 📂 Folder Structure

```
your-project/
├── local_videos/           # 👈 Put your videos here!
│   ├── vacation.mp4
│   ├── presentation.avi
│   └── family_dinner.mov
├── output/
│   ├── optimized/         # Optimized videos
│   ├── converted/         # Format conversions
│   └── ...
└── ...
```

## 🎬 Usage Examples

### List Available Videos
```bash
python main.py list
```
Output:
```
📹 Videos in local_videos/ folder:
========================================
   1. vacation.mp4 (45.2 MB)
   2. presentation.avi (120.5 MB)
   3. family_dinner.mov (89.7 MB)

Total: 3 videos
```

### Process Videos by Index
```bash
# Optimize video #1
python main.py optimize 1 --compression high

# Convert video #2 to WebM
python main.py convert 2 --format webm

# Show info for video #3
python main.py info 3
```

### Process Videos by Name
```bash
# Optimize vacation video
python main.py optimize vacation --max-width 1280

# Convert presentation to MP4
python main.py convert presentation --format mp4

# Show family dinner info
python main.py info family_dinner
```

### Still Works with Full Paths
```bash
# Traditional path-based approach still works
python main.py optimize /full/path/to/video.mp4
```

## 🔧 Interactive Mode

The interactive mode automatically shows your available videos:

```bash
python main.py --interactive
```

Output:
```
🎬 Welcome to Video Processing Suite!
==================================================

📹 Videos in local_videos/ folder:
========================================
   1. vacation.mp4 (45.2 MB)
   2. presentation.avi (120.5 MB)
   3. family_dinner.mov (89.7 MB)

Total: 3 videos

==================================================
🎬 Main Menu
==================================================
1. 🔧 Optimize local video
2. 🔄 Convert video format
...
```

When you select "Optimize local video", you'll see a list to choose from:

```
📹 Available videos:
   1. vacation.mp4 (45.2 MB)
   2. presentation.avi (120.5 MB)
   3. family_dinner.mov (89.7 MB)

Choose video to optimize: (1-3 or 'r' to refresh): 
```

## 💡 Pro Tips

### Smart Video Selection
- **By Index**: `1`, `2`, `3` - Quick numeric selection
- **By Name**: `vacation`, `presentation` - Use filename without extension
- **Refresh**: Type `r` in interactive mode to refresh the video list
- **Full Path**: Still works if you prefer traditional paths

### Workflow Examples

#### Batch Optimize Multiple Videos
```bash
# Optimize all videos to 720p
python main.py optimize 1 --max-width 1280 --compression medium
python main.py optimize 2 --max-width 1280 --compression medium
python main.py optimize 3 --max-width 1280 --compression medium
```

#### Convert Library to WebM
```bash
# Convert all videos to WebM for web use
python main.py convert vacation --format webm --quality high
python main.py convert presentation --format webm --quality medium
python main.py convert family_dinner --format webm --quality high
```

#### Quick Video Analysis
```bash
# Check all video properties
python main.py info 1
python main.py info 2
python main.py info 3
```

## 🔄 Dynamic Updates

- Add new videos to `local_videos/` anytime
- Use `python main.py list` to see updated list
- In interactive mode, type `r` to refresh the list
- No restart required!

## ⚡ Command Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `list` | Show available videos | `python main.py list` |
| `optimize {video}` | Optimize video | `python main.py optimize 1 --compression high` |
| `convert {video}` | Convert format | `python main.py convert vacation --format webm` |
| `info {video}` | Show video details | `python main.py info presentation` |
| `--interactive` | Launch interactive mode | `python main.py --interactive` |

## 🎯 Benefits

✅ **No more typing long paths**  
✅ **Visual list of available videos**  
✅ **Quick numeric selection**  
✅ **Name-based selection**  
✅ **Auto-refresh capabilities**  
✅ **Works in both CLI and interactive modes**  
✅ **Maintains backward compatibility**

---

**Start by adding some videos to `local_videos/` and try it out! 🎬**
