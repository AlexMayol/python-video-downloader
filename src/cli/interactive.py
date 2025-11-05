"""
Interactive command-line interface for easy video processing.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.video_processor import VideoProcessor
from services.downloader import VideoDownloader
from utils.config import ConfigManager
from utils.video_finder import VideoFinder


class InteractiveInterface:
    """Interactive CLI for video processing operations."""
    
    def __init__(self):
        self.processor = VideoProcessor()
        self.downloader = VideoDownloader()
        self.video_finder = VideoFinder()
        
    def run(self):
        """Run the interactive interface."""
        print("🎬 Welcome to Video Processing Suite!")
        print("=" * 50)
        
        # Show available videos
        print(f"\n{self.video_finder.list_videos_formatted()}")
        
        while True:
            try:
                choice = self.show_main_menu()
                
                if choice == '1':
                    self.interactive_optimize()
                elif choice == '2':
                    self.interactive_convert()
                elif choice == '3':
                    self.interactive_download()
                elif choice == '4':
                    self.interactive_batch_local()
                elif choice == '5':
                    self.show_video_info()
                elif choice == '6':
                    self.create_config_file()
                elif choice == '7':
                    self.show_help()
                elif choice == '8':
                    print("👋 Thanks for using Video Processing Suite!")
                    break
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ An error occurred: {e}")
                input("Press Enter to continue...")
    
    def show_main_menu(self) -> str:
        """Display main menu and get user choice."""
        print("\n" + "=" * 50)
        print("🎬 Main Menu")
        print("=" * 50)
        print("1. 🔧 Optimize local video")
        print("2. 🔄 Convert video format")
        print("3. 📥 Download video from URL")
        print("4. 📁 Batch process local videos")
        print("5. ℹ️  Show video information")
        print("6. ⚙️  Create configuration file")
        print("7. ❓ Help")
        print("8. 🚪 Exit")
        print("=" * 50)
        
        return input("👉 Choose an option (1-8): ").strip()
    
    def interactive_optimize(self):
        """Interactive video optimization."""
        print("\n🔧 Video Optimization")
        print("-" * 30)
        
        # Get input file from local_videos folder
        input_path = self.select_local_video("Choose video to optimize:")
        if not input_path:
            return
        
        # Show current video info
        try:
            info = self.processor.get_video_info(input_path)
            print(f"\n📊 Current video info:")
            print(f"   Dimensions: {info['width']}x{info['height']}")
            print(f"   Duration: {info['duration']:.1f}s")
            print(f"   Size: {info['size_mb']:.1f} MB")
            print(f"   Format: {info['format'].upper()}")
        except Exception as e:
            print(f"⚠️  Could not read video info: {e}")
            return
        
        # Get optimization settings
        print(f"\n⚙️  Optimization Settings:")
        
        compression = self.choose_compression_level()
        resize_option = self.choose_resize_option()
        
        max_width = max_height = scale_factor = None
        if resize_option == '1':  # Custom dimensions
            max_width = self.get_number("Maximum width (or Enter for no limit): ", optional=True)
            max_height = self.get_number("Maximum height (or Enter for no limit): ", optional=True)
        elif resize_option == '2':  # Scale factor
            scale_factor = self.get_number("Scale factor (e.g., 0.5 for half size): ", is_float=True)
        
        output_format = self.choose_output_format(info['format'])
        lossless = input("🔒 Use lossless compression? (y/N): ").lower().startswith('y')
        
        # Get output path
        default_output = f"{Path(input_path).stem}_optimized.{output_format}"
        output_path = input(f"Output filename (Enter for '{default_output}'): ").strip()
        if not output_path:
            output_path = None
        
        # Perform optimization
        print(f"\n🚀 Starting optimization...")
        try:
            result = self.processor.optimize_video(
                input_path=input_path,
                output_path=output_path,
                compression_level=compression,
                max_width=max_width,
                max_height=max_height,
                scale_factor=scale_factor,
                output_format=output_format,
                lossless=lossless
            )
            print(f"✅ Optimization complete: {result}")
        except Exception as e:
            print(f"❌ Optimization failed: {e}")
    
    def interactive_convert(self):
        """Interactive video format conversion."""
        print("\n🔄 Video Format Conversion")
        print("-" * 30)
        
        # Get input file from local_videos folder
        input_path = self.select_local_video("Choose video to convert:")
        if not input_path:
            return
        
        # Show supported formats
        formats = list(VideoProcessor.list_supported_formats().keys())
        print(f"\n📋 Supported formats: {', '.join(f.upper() for f in formats)}")
        
        # Get target format
        while True:
            target_format = input("Target format: ").strip().lower()
            if target_format in formats:
                break
            print(f"❌ Invalid format. Supported: {', '.join(formats)}")
        
        # Get quality setting
        quality = self.choose_compression_level("Choose conversion quality:")
        
        # Get output path
        default_output = f"{Path(input_path).stem}_converted.{target_format}"
        output_path = input(f"Output filename (Enter for '{default_output}'): ").strip()
        if not output_path:
            output_path = None
        
        # Perform conversion
        print(f"\n🚀 Starting conversion...")
        try:
            result = self.processor.convert_format(
                input_path=input_path,
                target_format=target_format,
                output_path=output_path,
                quality=quality
            )
            print(f"✅ Conversion complete: {result}")
        except Exception as e:
            print(f"❌ Conversion failed: {e}")
    
    def interactive_download(self):
        """Interactive video download."""
        print("\n📥 Video Download")
        print("-" * 20)
        
        url = input("Enter video URL: ").strip()
        if not url:
            print("❌ URL is required")
            return
        
        filename = input("Custom filename (or Enter for auto): ").strip()
        if not filename:
            filename = None
        
        optimize_after = input("🔧 Optimize after download? (y/N): ").lower().startswith('y')
        compression = None
        if optimize_after:
            compression = self.choose_compression_level()
        
        # Perform download
        print(f"\n🚀 Starting download...")
        try:
            result = self.downloader.download_video(url, filename=filename)
            print(f"✅ Download complete: {result}")
            
            if optimize_after:
                print(f"🔧 Optimizing downloaded video...")
                optimized = self.processor.optimize_video(
                    input_path=result,
                    compression_level=compression
                )
                print(f"✅ Optimization complete: {optimized}")
                
        except Exception as e:
            print(f"❌ Download failed: {e}")
    
    def interactive_batch_local(self):
        """Interactive batch processing of local videos."""
        print("\n📁 Batch Process Local Videos")
        print("-" * 35)
        
        # Get directory (default to local_videos/ when empty)
        directory = input("Enter directory path containing videos (Enter for local_videos/): ").strip()
        if not directory:
            directory = self.video_finder.ensure_local_videos_dir()
            print(f"Using default folder: {directory}")
        elif not Path(directory).exists():
            print("❌ Invalid directory path")
            return
        
        # Find video files
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(Path(directory).glob(f"*{ext}"))
            video_files.extend(Path(directory).glob(f"*{ext.upper()}"))
        
        if not video_files:
            print(f"❌ No video files found in {directory}")
            return
        
        print(f"\n📋 Found {len(video_files)} video files:")
        for i, file in enumerate(video_files, 1):
            print(f"   {i}. {file.name}")
        
        # Get processing settings
        print(f"\n⚙️  Batch Processing Settings:")
        compression = self.choose_compression_level()
        output_format = self.choose_output_format()
        
        # Confirm processing
        if not input(f"\n🚀 Process all {len(video_files)} videos? (y/N): ").lower().startswith('y'):
            return
        
        # Process each video
        for i, video_path in enumerate(video_files, 1):
            print(f"\n📹 Processing {i}/{len(video_files)}: {video_path.name}")
            try:
                result = self.processor.optimize_video(
                    input_path=str(video_path),
                    compression_level=compression,
                    output_format=output_format
                )
                print(f"   ✅ Complete: {Path(result).name}")
            except Exception as e:
                print(f"   ❌ Failed: {e}")
        
        print(f"\n🎉 Batch processing complete!")
    
    def show_video_info(self):
        """Show detailed video information."""
        print("\nℹ️  Video Information")
        print("-" * 20)
        
        input_path = self.select_local_video("Choose video to analyze:")
        if not input_path:
            return
        
        try:
            info = self.processor.get_video_info(input_path)
            print(f"\n📊 Video Information:")
            print(f"   📄 File: {Path(input_path).name}")
            print(f"   📐 Dimensions: {info['width']} × {info['height']} pixels")
            print(f"   ⏱️  Duration: {info['duration']:.1f} seconds ({info['duration']/60:.1f} minutes)")
            print(f"   🎬 Frame Rate: {info['fps']:.2f} FPS")
            print(f"   💾 File Size: {info['size_mb']:.1f} MB")
            print(f"   🎞️  Format: {info['format'].upper()}")
            if 'bitrate_mbps' in info:
                print(f"   🚀 Bitrate: {info['bitrate_mbps']:.3f} Mbps ({info['bitrate_kbps']:.2f} kbps)")
        except Exception as e:
            print(f"❌ Could not read video info: {e}")
    
    def create_config_file(self):
        """Create a configuration file."""
        print("\n⚙️  Create Configuration File")
        print("-" * 35)
        
        print("Choose configuration type:")
        print("1. Download and process videos from URLs")
        print("2. Process local videos")
        
        choice = input("Choose type (1-2): ").strip()
        
        if choice == '1':
            config = ConfigManager.create_default_config()
        elif choice == '2':
            config = ConfigManager.create_local_processing_config()
        else:
            print("❌ Invalid choice")
            return
        
        # Get filename
        default_name = "config.json"
        filename = input(f"Config filename (Enter for '{default_name}'): ").strip()
        if not filename:
            filename = default_name
        
        # Save config
        try:
            ConfigManager.save_config(config, filename)
            print(f"✅ Configuration saved: {filename}")
            print(f"📝 Edit this file to customize your settings")
        except Exception as e:
            print(f"❌ Failed to save config: {e}")
    
    def show_help(self):
        """Show help information."""
        print("\n❓ Help")
        print("-" * 10)
        print("""
🎬 Video Processing Suite Help
=============================

This tool helps you:
- 🔧 Optimize videos (reduce file size while maintaining quality)
- 🔄 Convert between video formats (MP4, WebM, AVI, etc.)
- 📥 Download videos from URLs
- 📁 Batch process multiple videos

💡 Tips:
- Use 'lossless' compression for archival purposes
- Use 'medium' compression for general use
- Use 'low' or 'very_low' for web delivery
- WebM format often provides better compression than MP4
- Always keep backups of original files

🔧 Compression Levels:
- Lossless: No quality loss (largest files)
- High: Near-lossless quality
- Medium: Balanced quality and size (recommended)
- Low: Smaller files, some quality loss
- Very Low: Smallest files, noticeable quality loss

📊 File Formats:
- MP4: Best compatibility, good compression
- WebM: Excellent compression, good for web
- AVI: Good quality, larger files
- MOV: Apple format, good quality
        """)
        
        input("\nPress Enter to continue...")
    
    def select_local_video(self, prompt: str = "Select a video:") -> Optional[str]:
        """Select a video from the local_videos folder."""
        videos = self.video_finder.find_videos()
        
        if not videos:
            print("❌ No videos found in local_videos/ folder.")
            print("💡 Add some videos to the local_videos/ directory first!")
            return None
        
        print(f"\n📹 Available videos:")
        for i, video in enumerate(videos, 1):
            size_str = f"{video['size_mb']:.1f} MB"
            print(f"   {i}. {video['name']}{video['extension']} ({size_str})")
        
        while True:
            try:
                choice = input(f"\n{prompt} (1-{len(videos)} or 'r' to refresh): ").strip().lower()
                
                if choice == 'r':
                    # Refresh video list
                    videos = self.video_finder.find_videos()
                    if not videos:
                        print("❌ No videos found in local_videos/ folder.")
                        return None
                    print(f"\n📹 Available videos (refreshed):")
                    for i, video in enumerate(videos, 1):
                        size_str = f"{video['size_mb']:.1f} MB"
                        print(f"   {i}. {video['name']}{video['extension']} ({size_str})")
                    continue
                
                if choice == '' or choice == 'q':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(videos):
                    selected_video = videos[choice_num - 1]
                    print(f"✅ Selected: {selected_video['filename']}")
                    return selected_video['path']
                else:
                    print(f"❌ Please enter a number between 1 and {len(videos)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_file_path(self, prompt: str) -> Optional[str]:
        """Get and validate file path from user."""
        while True:
            path = input(prompt).strip()
            if not path:
                return None
            
            if Path(path).exists():
                return path
            else:
                print(f"❌ File not found: {path}")
                if not input("Try again? (Y/n): ").lower().startswith('n'):
                    continue
                return None
    
    def get_number(self, prompt: str, is_float: bool = False, optional: bool = False) -> Optional[float]:
        """Get a number from user input."""
        while True:
            value = input(prompt).strip()
            if not value and optional:
                return None
            
            try:
                return float(value) if is_float else int(value)
            except ValueError:
                print("❌ Please enter a valid number")
    
    def choose_compression_level(self, title: str = "Choose compression level:") -> str:
        """Let user choose compression level."""
        presets = VideoProcessor.list_compression_presets()
        
        print(f"\n{title}")
        for i, (preset, info) in enumerate(presets.items(), 1):
            print(f"   {i}. {preset.title()}: {info['description']}")
        
        while True:
            try:
                choice = int(input(f"Choose compression (1-{len(presets)}): ").strip())
                if 1 <= choice <= len(presets):
                    return list(presets.keys())[choice - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(presets)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def choose_resize_option(self) -> str:
        """Let user choose resize option."""
        print(f"\n📏 Resize options:")
        print(f"   1. Set maximum dimensions")
        print(f"   2. Use scale factor")
        print(f"   3. Keep original size")
        
        while True:
            choice = input("Choose option (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return choice
            print("❌ Please enter 1, 2, or 3")
    
    def choose_output_format(self, current_format: str = None) -> str:
        """Let user choose output format."""
        formats = list(VideoProcessor.list_supported_formats().keys())
        
        print(f"\n📋 Available formats:")
        for i, fmt in enumerate(formats, 1):
            current_indicator = " (current)" if fmt == current_format else ""
            print(f"   {i}. {fmt.upper()}{current_indicator}")
        
        while True:
            choice = input(f"Choose format (1-{len(formats)}) or Enter for current: ").strip()
            
            if not choice and current_format:
                return current_format
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(formats):
                    return formats[choice_num - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(formats)}")
            except ValueError:
                print("❌ Please enter a valid number")
