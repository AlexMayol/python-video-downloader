"""
Enhanced command-line interface for video processing operations.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.video_processor import VideoProcessor
from services.downloader import VideoDownloader
from utils.config import ConfigManager
from utils.video_finder import VideoFinder
from cli.interactive import InteractiveInterface


class VideoCLI:
    """Main CLI interface for video processing."""
    
    def __init__(self):
        self.processor = VideoProcessor()
        self.downloader = VideoDownloader()
        self.video_finder = VideoFinder()
        self.interactive = InteractiveInterface()
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create the main argument parser."""
        parser = argparse.ArgumentParser(
            description='Video Processing Suite - Download, optimize, and convert videos',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Interactive mode
  python -m src.cli.main --interactive
  
  # Process from config file
  python -m src.cli.main --config config.json
  
  # Optimize local video
  python -m src.cli.main optimize input.mp4 --compression medium --max-width 1280
  
  # Convert video format
  python -m src.cli.main convert input.mp4 --format webm --quality high
  
  # Download and process video
  python -m src.cli.main download "https://example.com/video.mp4" --optimize
            """
        )
        
        # Global options
        parser.add_argument('--config', '-c', help='Configuration file path')
        parser.add_argument('--output-dir', '-o', default='output', help='Output directory')
        parser.add_argument('--interactive', '-i', action='store_true', help='Launch interactive mode')
        parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        
        # Subcommands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Optimize command
        optimize_parser = subparsers.add_parser('optimize', help='Optimize local video')
        optimize_parser.add_argument('input', help='Video name/index from local_videos/ or full path')
        optimize_parser.add_argument('--output', help='Output file path')
        optimize_parser.add_argument('--compression', choices=['lossless', 'high', 'medium', 'low', 'very_low'], 
                                   default='medium', help='Compression level')
        optimize_parser.add_argument('--max-width', type=int, help='Maximum width')
        optimize_parser.add_argument('--max-height', type=int, help='Maximum height')
        optimize_parser.add_argument('--scale', type=float, help='Scale factor (e.g., 0.5 for half size)')
        optimize_parser.add_argument('--format', help='Output format')
        optimize_parser.add_argument('--lossless', action='store_true', help='Force lossless compression')
        
        # Convert command
        convert_parser = subparsers.add_parser('convert', help='Convert video format')
        convert_parser.add_argument('input', help='Video name/index from local_videos/ or full path')
        convert_parser.add_argument('--format', '-f', required=True, help='Target format')
        convert_parser.add_argument('--output', help='Output file path')
        convert_parser.add_argument('--quality', choices=['lossless', 'high', 'medium', 'low', 'very_low'],
                                  default='medium', help='Conversion quality')
        
        # Download command
        download_parser = subparsers.add_parser('download', help='Download video from URL')
        download_parser.add_argument('url', help='Video URL to download')
        download_parser.add_argument('--filename', help='Custom filename')
        download_parser.add_argument('--optimize', action='store_true', help='Optimize after download')
        download_parser.add_argument('--compression', choices=['lossless', 'high', 'medium', 'low', 'very_low'],
                                   default='medium', help='Compression level (if optimizing)')
        
        # Batch command
        batch_parser = subparsers.add_parser('batch', help='Process videos from config file')
        batch_parser.add_argument('config_file', help='Configuration file path')
        
        # Info command
        info_parser = subparsers.add_parser('info', help='Show video information')
        info_parser.add_argument('input', help='Video name/index from local_videos/ or full path')
        
        # List formats command
        subparsers.add_parser('formats', help='List supported formats and compression presets')
        
        # List videos command
        subparsers.add_parser('list', help='List available videos in local_videos folder')
        
        return parser
    
    def resolve_video_input(self, input_str: str) -> str:
        """
        Resolve video input which can be:
        - A number (index in local_videos folder)
        - A name (without extension)
        - A full file path
        """
        # Check if it's a number (index)
        try:
            index = int(input_str) - 1  # Convert to 0-based index
            video = self.video_finder.get_video_by_index(index)
            if video:
                return video['path']
            else:
                raise ValueError(f"Invalid video index: {int(input_str)}")
        except ValueError:
            pass
        
        # Check if it's a video name (without extension)
        video = self.video_finder.get_video_by_name(input_str)
        if video:
            return video['path']
        
        # Check if it's a full path
        if Path(input_str).exists():
            return input_str
        
        # If nothing matches, show available videos and raise error
        print(f"\n📹 Available videos in local_videos/:")
        videos = self.video_finder.find_videos()
        if videos:
            for i, video in enumerate(videos, 1):
                print(f"   {i}. {video['name']}")
            print(f"\n💡 You can use:")
            print(f"   - Video index (1-{len(videos)})")
            print(f"   - Video name (e.g., '{videos[0]['name']}')")
            print(f"   - Full file path")
        else:
            print("   No videos found! Add videos to local_videos/ folder first.")
        
        raise ValueError(f"Could not find video: {input_str}")
    
    def run(self, args=None):
        """Run the CLI application."""
        parser = self.create_parser()
        args = parser.parse_args(args)
        
        try:
            if args.interactive:
                self.interactive.run()
            elif args.command == 'optimize':
                self.optimize_video(args)
            elif args.command == 'convert':
                self.convert_video(args)
            elif args.command == 'download':
                self.download_video(args)
            elif args.command == 'batch':
                self.process_batch(args)
            elif args.command == 'info':
                self.show_info(args)
            elif args.command == 'formats':
                self.list_formats()
            elif args.command == 'list':
                self.list_videos()
            elif args.config:
                self.process_from_config(args.config, args.output_dir)
            else:
                parser.print_help()
                
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    def optimize_video(self, args):
        """Handle video optimization."""
        input_path = self.resolve_video_input(args.input)
        output_path = self.processor.optimize_video(
            input_path=input_path,
            output_path=args.output,
            compression_level=args.compression,
            max_width=args.max_width,
            max_height=args.max_height,
            scale_factor=args.scale,
            output_format=args.format,
            lossless=args.lossless
        )
        print(f"Optimization complete: {output_path}")
    
    def convert_video(self, args):
        """Handle video format conversion."""
        input_path = self.resolve_video_input(args.input)
        output_path = self.processor.convert_format(
            input_path=input_path,
            target_format=args.format,
            output_path=args.output,
            quality=args.quality
        )
        print(f"Conversion complete: {output_path}")
    
    def download_video(self, args):
        """Handle video download."""
        output_path = self.downloader.download_video(
            url=args.url,
            filename=args.filename
        )
        
        if args.optimize:
            print("Optimizing downloaded video...")
            optimized_path = self.processor.optimize_video(
                input_path=output_path,
                compression_level=args.compression
            )
            print(f"Download and optimization complete: {optimized_path}")
        else:
            print(f"Download complete: {output_path}")
    
    def process_batch(self, args):
        """Handle batch processing from config file."""
        self.process_from_config(args.config_file)
    
    def show_info(self, args):
        """Show video information."""
        input_path = self.resolve_video_input(args.input)
        info = self.processor.get_video_info(input_path)
        print(f"Video Information for: {Path(input_path).name}")
        print(f"Duration: {info['duration']:.2f} seconds")
        print(f"Dimensions: {info['width']}x{info['height']}")
        print(f"FPS: {info['fps']:.2f}")
        print(f"Size: {info['size_mb']:.2f} MB")
        print(f"Format: {info['format']}")
        if 'bitrate_mbps' in info:
            print(f"Bitrate: {info['bitrate_mbps']:.3f} Mbps ({info['bitrate_kbps']:.2f} kbps)")
    
    def list_formats(self):
        """List supported formats and compression presets."""
        print("Supported Output Formats:")
        for fmt, codecs in VideoProcessor.list_supported_formats().items():
            print(f"  {fmt.upper()}: {codecs['video_codec']} + {codecs['audio_codec']}")
        
        print("\nCompression Presets:")
        for preset, settings in VideoProcessor.list_compression_presets().items():
            print(f"  {preset}: {settings['description']}")
    
    def list_videos(self):
        """List available videos in local_videos folder."""
        print(self.video_finder.list_videos_formatted())
    
    def process_from_config(self, config_path: str, output_dir: str = 'output'):
        """Process videos from configuration file."""
        config = ConfigManager.load_config(config_path)
        ConfigManager.validate_config(config)
        
        self.processor = VideoProcessor(output_dir)
        self.downloader = VideoDownloader(f"{output_dir}/downloads")
        
        # Process downloaded videos
        for video_config in config.get('videos', []):
            print(f"\nProcessing video: {video_config.get('name', 'unnamed')}")
            
            # Download video
            downloaded_path = self.downloader.download_from_config(video_config)
            
            # Optimize video
            processing_config = config['processing']
            optimized_path = self.processor.optimize_video(
                input_path=downloaded_path,
                compression_level=processing_config.get('compression_level', 'medium'),
                max_width=processing_config.get('max_width'),
                max_height=processing_config.get('max_height'),
                output_format=video_config.get('output_format') or processing_config.get('output_format'),
                lossless=processing_config.get('lossless', False)
            )
            
            print(f"Video processed successfully: {optimized_path}")
        
        # Process local videos
        for video_config in config.get('local_videos', []):
            print(f"\nProcessing local video: {video_config.get('name', 'unnamed')}")
            
            local_path = video_config.get('local_path')
            if not local_path or not Path(local_path).exists():
                print(f"Local video not found: {local_path}")
                continue
            
            # Get processing settings (video-specific overrides global)
            processing_config = config['processing'].copy()
            video_processing = video_config.get('processing', {})
            processing_config.update(video_processing)
            
            optimized_path = self.processor.optimize_video(
                input_path=local_path,
                compression_level=processing_config.get('compression_level', 'medium'),
                max_width=processing_config.get('max_width'),
                max_height=processing_config.get('max_height'),
                output_format=video_config.get('output_format') or processing_config.get('output_format'),
                lossless=processing_config.get('lossless', False)
            )
            
            print(f"Local video processed successfully: {optimized_path}")


def main():
    """Entry point for CLI."""
    cli = VideoCLI()
    cli.run()


if __name__ == '__main__':
    main()
