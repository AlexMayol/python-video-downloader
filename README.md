# Video Processor

A tool for downloading and processing videos with configurable compression strategies.

## Features

- Download videos from URLs
- Multiple compression strategies
- Automatic thumbnail generation
- Output to zip archive

## Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/AlexMayol/python-video-downloader
cd python-video-downloader
```

2. **Install dependencies and set up the environment:**

```bash
make deps
```

This will create a Python virtual environment, install all required dependencies from `requirements.txt`.

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

- Each entry in the `videos` array should have a unique `name` and a direct `url` to the video file you want to download.
- The `config` section allows you to set the maximum width/height and compression strategy for all videos.

### 2. Run the Project

```bash
make run
```

This will activate the virtual environment and run the main video processing script (`video_processor.py`). The script will:

- Download each video listed in `videos.json`.
- Optimize and compress the videos according to your configuration.
- Extract a thumbnail (poster) from each video.
- Save all processed files in the `dist` directory and create a zip archive.

### Clean Up

To remove the virtual environment and all generated files/directories:

```bash
make clean
```

### Help

To see all available Makefile commands:

```bash
make help
```

## Configuration

Create a `videos.json` file in the same directory as the executable with the following structure:

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
    }
  ]
}
```

### Compression Strategies

- `original`: No compression, keeps the original video file as-is
- `relaxed`: Lossless compression with high quality (larger file size)
- `balanced`: Balanced compression (default)
- `aggressive`: Lossy compression for smaller file size

## Output

The application creates:

1. Processed videos in the `dist` directory
2. Thumbnails for each video
3. A zip archive containing all processed files

## Development

- To install or update dependencies, edit `requirements.txt` and run `make deps`.
- To run the project, use `make run`.
- To clean up, use `make clean`.

## Requirements

- Python 3.11+
- GNU Make

## Notes

- The application creates temporary directories (`downloads`, `optimized`, `frames`) during processing
- These directories are automatically cleaned up after processing
- The final output is available in the `dist` directory
- A zip archive is created containing all processed files
