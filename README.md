# Video Processor

A tool for downloading and processing videos with configurable compression strategies.

## Features

- Download videos from URLs
- Multiple compression strategies
- Automatic thumbnail generation
- Output to zip archive

## Installation

### From Source

1. Clone the repository:

```bash
git clone <repository-url>
cd python-video-downloader
```

2. Install dependencies:

```bash
make deps
```

3. Build the executable:

```bash
make build
```

## Usage

### Configuration

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

### Building from Source

- Build the executable:

```bash
make build
```

- Clean build artifacts:

```bash
make clean
```

- Rebuild everything:

```bash
make rebuild
```

### Available Make Commands

```bash
make build    # Build the executable
make clean    # Clean up build artifacts
make deps     # Install dependencies
make rebuild  # Clean and rebuild
make help     # Show help message
```

## Requirements

- Python 3.11+
- Required Python packages (installed via `make deps`):
  - moviepy
  - requests
  - pillow
  - numpy

## Notes

- The application creates temporary directories (`downloads`, `optimized`, `frames`) during processing
- These directories are automatically cleaned up after processing
- The final output is available in the `dist` directory
- A zip archive is created containing all processed files
