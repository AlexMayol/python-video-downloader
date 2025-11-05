# 🎬 Video Processing Suite

A comprehensive Python tool for downloading, optimizing, and converting videos. This enhanced version supports both online video downloading and local video processing with advanced compression and format conversion capabilities.

## ✨ Features

### 🔧 Video Optimization
- **Lossless compression** for archival purposes
- **Multiple compression levels** (lossless, high, medium, low, very_low)
- **Intelligent resizing** with aspect ratio preservation
- **Format-specific optimization** for web delivery

### 🔄 Format Conversion
- Support for **8 popular formats**: MP4, WebM, AVI, MOV, MKV, WMV, FLV, M4V
- **Quality presets** for different use cases
- **Batch conversion** of multiple files
- **Optimized codec settings** for each format

### 📥 Video Downloading
- Download videos from URLs
- **Automatic optimization** after download
- **Custom filename** support
- **Progress tracking**

### 🖥️ User-Friendly Interface
- **Interactive mode** with guided prompts
- **Command-line interface** for automation
- **Configuration files** (JSON/YAML) for batch processing
- **Detailed help** and format information

## 🚀 Quick Start

### Interactive Mode (Recommended for Beginners)
```bash
python main.py --interactive
```

### Command Line Examples

#### Optimize Local Video
```bash
# Basic optimization
python main.py optimize input.mp4 --compression medium

# Resize and compress
python main.py optimize large_video.mov --max-width 1280 --compression high --format mp4

# Scale down by 50%
python main.py optimize input.avi --scale 0.5 --compression medium
```

#### Convert Video Format
```bash
# Convert to WebM with high quality
python main.py convert input.mp4 --format webm --quality high

# Convert to MP4 with medium quality
python main.py convert input.avi --format mp4 --quality medium
```

#### Download and Process
```bash
# Download and optimize
python main.py download "https://example.com/video.mp4" --optimize --compression medium

# Download with custom filename
python main.py download "https://example.com/video.mp4" --filename "my_video.mp4"
```

#### Batch Processing
```bash
# Process from config file
python main.py batch config/local_processing.json

# Legacy compatibility
python main.py --config videos.json
```

#### Video Information
```bash
# Show detailed video info
python main.py info my_video.mp4

# List supported formats
python main.py formats
```

## 📁 Project Structure

```
video-processing-suite/
├── src/                          # Source code
│   ├── core/                     # Core processing logic
│   │   └── video_processor.py    # Main video processing class
│   ├── services/                 # External services
│   │   └── downloader.py         # Video downloading service
│   ├── utils/                    # Utilities
│   │   └── config.py             # Configuration management
│   └── cli/                      # Command-line interfaces
│       ├── main.py               # Main CLI application
│       └── interactive.py        # Interactive interface
├── config/                       # Configuration templates
│   ├── default.json              # Basic download config
│   ├── local_processing.json     # Local video processing
│   └── batch_convert.yaml        # Batch conversion example
├── output/                       # Processing outputs
│   ├── downloads/                # Downloaded videos
│   ├── optimized/                # Optimized videos
│   ├── converted/                # Format conversions
│   ├── frames/                   # Extracted frames
│   └── temp/                     # Temporary files
├── tests/                        # Test files
├── main.py                       # Main entry point
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## ⚙️ Configuration

### Processing Settings

| Setting | Description | Options |
|---------|-------------|---------|
| `compression_level` | Quality vs size trade-off | `lossless`, `high`, `medium`, `low`, `very_low` |
| `max_width` | Maximum width in pixels | Any positive integer |
| `max_height` | Maximum height in pixels | Any positive integer |
| `scale_factor` | Resize multiplier | 0.1 to 2.0 (e.g., 0.5 = half size) |
| `output_format` | Target video format | `mp4`, `webm`, `avi`, `mov`, `mkv`, `wmv`, `flv`, `m4v` |
| `lossless` | Force lossless compression | `true` or `false` |

### Configuration Files

#### For Local Video Processing (`config/local_processing.json`):
```json
{
  "processing": {
    "max_width": 1920,
    "max_height": 1080,
    "compression_level": "medium",
    "output_format": "mp4",
    "lossless": false,
    "output_dir": "output"
  },
  "local_videos": [
    {
      "name": "my_video",
      "local_path": "/path/to/video.mp4",
      "output_format": "webm",
      "processing": {
        "max_width": 1280,
        "compression_level": "high"
      }
    }
  ]
}
```

#### For Video Downloads (`config/default.json`):
```json
{
  "processing": {
    "compression_level": "medium",
    "max_width": 1920,
    "max_height": 1080
  },
  "videos": [
    {
      "name": "example_video",
      "url": "https://example.com/video.mp4",
      "output_format": "mp4"
    }
  ]
}
```

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AlexMayol/python-video-downloader
   cd python-video-downloader
   ```

2. **Install dependencies**:
   ```bash
   # Using make (recommended)
   make deps
   
   # Or manually
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (required for video processing):
   - **macOS**: `brew install ffmpeg`
   - **Ubuntu/Debian**: `sudo apt install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

4. **Test installation**:
   ```bash
   python main.py --help
   ```

## 💡 Tips & Best Practices

### Compression Levels
- **Lossless**: Perfect quality, largest files - use for archival
- **High**: Near-perfect quality, good for professional work
- **Medium**: Balanced quality/size - recommended for most uses
- **Low**: Smaller files, some quality loss - good for web/streaming
- **Very Low**: Smallest files, noticeable quality loss - use sparingly

### Format Recommendations
- **MP4**: Best compatibility across devices and platforms
- **WebM**: Excellent compression, ideal for web delivery
- **AVI**: Good quality but larger files
- **MOV**: Apple ecosystem, good quality

### Performance Tips
- Use **batch processing** for multiple files
- **Resize videos** before compression for better results
- Keep **original files** as backups
- Use **SSD storage** for faster processing

## 🔄 Migration from v1.0

If you're upgrading from the original version:

1. **Old command**: `python main.py --json-file videos.json`
   **New command**: `python main.py batch videos.json`

2. **Configuration files**: Your existing `videos.json` files are still supported
3. **New features**: Use `python main.py --interactive` to explore new capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:
1. Check that FFmpeg is properly installed
2. Verify input file formats are supported
3. Ensure sufficient disk space for processing
4. Check the GitHub issues page for known problems

---

## Legacy Documentation (v1.0)

<details>
<summary>Click to view original documentation</summary>

# Video Processor

A tool for downloading and processing videos with configurable compression strategies.

## Features

- Download videos from URLs
- Multiple compression strategies
- Automatic thumbnail generation
- Output to zip archive

## Usage

### 1. Prepare your video list (videos.json)

Before running the project, create or edit a `videos.json` file in the project directory. This file should contain the list of videos you want to download and process, along with configuration options. For example:

```json
{
  "config": {
    "max_width": 300,
    "max_height": 300,
    "compression_strategy": "balanced"
  },
  "videos": [
    {
      "name": "video1",
      "url": "https://example.com/video1.mp4"
    },
    {
      "name": "video2",
      "url": "https://example.com/video2.mp4"
    }
  ]
}
```

### 2. Run the Project

```bash
make run
```

### Compression Strategies

- `original`: No compression, keeps the original video file as-is
- `relaxed`: Lossless compression with high quality (larger file size)
- `balanced`: Balanced compression (default)
- `aggressive`: Lossy compression for smaller file size

</details>
