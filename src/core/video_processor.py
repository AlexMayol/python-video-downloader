"""
Core video processing functionality including optimization, compression, and conversion.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from moviepy.editor import VideoFileClip
from moviepy.video.fx.resize import resize


class VideoProcessor:
    """Main video processing class for optimization and conversion."""
    
    SUPPORTED_FORMATS = {
        'mp4': {'video_codec': 'libx264', 'audio_codec': 'aac'},
        'webm': {'video_codec': 'libvpx-vp9', 'audio_codec': 'libvorbis'},
        'avi': {'video_codec': 'libx264', 'audio_codec': 'mp3'},
        'mov': {'video_codec': 'libx264', 'audio_codec': 'aac'},
        'mkv': {'video_codec': 'libx264', 'audio_codec': 'aac'},
        'wmv': {'video_codec': 'wmv2', 'audio_codec': 'wmav2'},
        'flv': {'video_codec': 'libx264', 'audio_codec': 'aac'},
        'm4v': {'video_codec': 'libx264', 'audio_codec': 'aac'}
    }
    
    COMPRESSION_PRESETS = {
        'lossless': {'crf': 0, 'preset': 'veryslow', 'description': 'Lossless compression (largest file)'},
        'high': {'crf': 18, 'preset': 'slow', 'description': 'High quality (near lossless)'},
        'medium': {'crf': 23, 'preset': 'medium', 'description': 'Balanced quality and size'},
        'low': {'crf': 28, 'preset': 'fast', 'description': 'Lower quality (smaller file)'},
        'very_low': {'crf': 35, 'preset': 'veryfast', 'description': 'Very low quality (smallest file)'}
    }
    
    def __init__(self, output_dir: str = "output"):
        """Initialize the video processor with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "optimized").mkdir(exist_ok=True)
        (self.output_dir / "converted").mkdir(exist_ok=True)
        (self.output_dir / "temp").mkdir(exist_ok=True)
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Get video information including dimensions, duration, format, and bitrate.

        Bitrate is retrieved via ffprobe when available; otherwise estimated from file size and duration.
        """
        try:
            with VideoFileClip(video_path) as video:
                info: Dict[str, Any] = {
                    'duration': video.duration,
                    'width': video.w,
                    'height': video.h,
                    'fps': video.fps,
                    'size_mb': os.path.getsize(video_path) / (1024 * 1024),
                    'format': Path(video_path).suffix.lower().lstrip('.')
                }

            # Try to get precise bitrate using ffprobe
            bitrate_bps: Optional[int] = None
            try:
                cmd = [
                    'ffprobe', '-v', 'error',
                    '-select_streams', 'v:0',
                    '-show_entries', 'stream=bit_rate',
                    '-show_format', 'format=bit_rate',
                    '-of', 'json',
                    video_path,
                ]
                proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
                data = json.loads(proc.stdout or '{}')

                # Prefer stream bitrate; fall back to container format bitrate
                stream_list = data.get('streams') or []
                if stream_list and isinstance(stream_list, list):
                    stream_bitrate = stream_list[0].get('bit_rate')
                    if stream_bitrate:
                        bitrate_bps = int(stream_bitrate)
                if not bitrate_bps:
                    fmt = data.get('format') or {}
                    fmt_bitrate = fmt.get('bit_rate')
                    if fmt_bitrate:
                        bitrate_bps = int(fmt_bitrate)
            except Exception:
                # Ignore ffprobe errors and estimate instead
                bitrate_bps = None

            # If ffprobe unavailable or missing value, estimate from size and duration
            if not bitrate_bps and info['duration'] and info['duration'] > 0:
                file_size_bytes = os.path.getsize(video_path)
                bitrate_bps = int((file_size_bytes * 8) / info['duration'])

            if bitrate_bps:
                info['bitrate_bps'] = int(bitrate_bps)
                info['bitrate_kbps'] = round(bitrate_bps / 1000.0, 2)
                info['bitrate_mbps'] = round(bitrate_bps / 1_000_000.0, 3)

            return info
        except Exception as e:
            raise ValueError(f"Could not read video file {video_path}: {str(e)}")
    
    def calculate_new_dimensions(
        self, 
        original_width: int, 
        original_height: int, 
        max_width: Optional[int] = None, 
        max_height: Optional[int] = None,
        scale_factor: Optional[float] = None
    ) -> Tuple[int, int]:
        """Calculate new dimensions while maintaining aspect ratio."""
        if scale_factor:
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
        elif max_width or max_height:
            if max_width and max_height:
                # Both dimensions specified - use the more restrictive one
                width_ratio = max_width / original_width
                height_ratio = max_height / original_height
                ratio = min(width_ratio, height_ratio)
            elif max_width:
                ratio = max_width / original_width
            else:  # max_height
                ratio = max_height / original_height
            
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
        else:
            # No scaling requested
            new_width, new_height = original_width, original_height
        
        # Ensure dimensions are even (required by many codecs)
        new_width = new_width if new_width % 2 == 0 else new_width - 1
        new_height = new_height if new_height % 2 == 0 else new_height - 1
        
        return new_width, new_height
    
    def optimize_video(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        compression_level: str = 'medium',
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        scale_factor: Optional[float] = None,
        output_format: Optional[str] = None,
        lossless: bool = False,
        audio_bitrate_kbps: int = 128,
        ensure_smaller: bool = True
    ) -> str:
        """
        Optimize video with compression and optional resizing.
        
        Args:
            input_path: Path to input video
            output_path: Path for output video (optional)
            compression_level: Compression preset ('lossless', 'high', 'medium', 'low', 'very_low')
            max_width: Maximum width for resizing
            max_height: Maximum height for resizing
            scale_factor: Scale factor for resizing (e.g., 0.5 for half size)
            output_format: Output format (defaults to same as input)
            lossless: Force lossless compression regardless of compression_level
            
        Returns:
            Path to optimized video
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input video not found: {input_path}")
        
        # Get video info
        video_info = self.get_video_info(str(input_path))
        
        # Determine output path and format
        if not output_path:
            output_format = output_format or video_info['format']
            output_path = self.output_dir / "optimized" / f"{input_path.stem}_optimized.{output_format}"
        else:
            output_path = Path(output_path)
            output_format = output_format or output_path.suffix.lower().lstrip('.')
        
        if output_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported output format: {output_format}")
        
        # Calculate new dimensions
        new_width, new_height = self.calculate_new_dimensions(
            video_info['width'],
            video_info['height'],
            max_width,
            max_height,
            scale_factor
        )
        
        print(f"Optimizing video: {input_path.name}")
        print(f"Original dimensions: {video_info['width']}x{video_info['height']}")
        print(f"New dimensions: {new_width}x{new_height}")
        print(f"Compression level: {compression_level}")
        print(f"Output format: {output_format}")
        
        try:
            with VideoFileClip(str(input_path)) as video:
                # Resize if needed
                if (new_width, new_height) != (video_info['width'], video_info['height']):
                    video = resize(video, (new_width, new_height))
                
                # Get compression settings
                if lossless:
                    compression_settings = self.COMPRESSION_PRESETS['lossless']
                else:
                    compression_settings = self.COMPRESSION_PRESETS.get(compression_level, self.COMPRESSION_PRESETS['medium'])
                
                format_settings = self.SUPPORTED_FORMATS[output_format]
                
                # Prepare FFmpeg parameters
                ffmpeg_params = [
                    '-crf', str(compression_settings['crf']),
                    '-preset', compression_settings['preset'],
                    '-pix_fmt', 'yuv420p'
                ]

                # Constrain bitrate relative to source when known (helps avoid size inflation)
                original_bitrate_bps = None
                try:
                    original_bitrate_bps = self.get_video_info(str(input_path)).get('bitrate_bps')
                except Exception:
                    original_bitrate_bps = None

                # Apply conservative caps for H.264 to avoid upscaling file size
                if not lossless and format_settings['video_codec'] == 'libx264' and original_bitrate_bps:
                    level_to_ratio = {
                        'high': 0.70,
                        'medium': 0.55,
                        'low': 0.40,
                        'very_low': 0.25,
                    }
                    ratio = level_to_ratio.get(compression_level, 0.55)
                    maxrate_kbps = int((original_bitrate_bps * ratio) / 1000)
                    bufsize_kbps = max(maxrate_kbps * 2, 1000)
                    ffmpeg_params.extend([
                        '-maxrate', f'{maxrate_kbps}k',
                        '-bufsize', f'{bufsize_kbps}k'
                    ])
                
                # Format-specific parameters
                if output_format == 'mp4':
                    ffmpeg_params.extend(['-movflags', '+faststart'])
                elif output_format == 'webm':
                    ffmpeg_params.extend(['-b:v', '0'])  # Use CRF mode for VP9
                
                # Write optimized video
                has_audio = video.audio is not None
                video.write_videofile(
                    str(output_path),
                    codec=format_settings['video_codec'],
                    audio_codec=format_settings['audio_codec'],
                    audio=has_audio,
                    audio_bitrate=(f"{audio_bitrate_kbps}k" if has_audio and not lossless else None),
                    ffmpeg_params=ffmpeg_params,
                    temp_audiofile=str(self.output_dir / "temp" / "temp_audio.m4a"),
                    remove_temp=True
                )
            
            # Print optimization results
            original_size = input_path.stat().st_size / (1024 * 1024)
            new_size = output_path.stat().st_size / (1024 * 1024)
            reduction = ((original_size - new_size) / original_size) * 100
            
            # If requested, ensure we do not deliver a larger file when format is unchanged
            if ensure_smaller and output_format == video_info['format'] and new_size >= original_size and not lossless:
                # Keep the smaller one (replace output with original)
                import shutil
                shutil.copy2(str(input_path), str(output_path))
                new_size = original_size
                reduction = 0.0
                print("Resulting file was larger than the original; kept the original file instead.")

            print(f"Optimization complete!")
            print(f"Original size: {original_size:.2f} MB")
            print(f"New size: {new_size:.2f} MB")
            print(f"Size reduction: {reduction:.2f}%")
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Error optimizing video: {str(e)}")
    
    def convert_format(
        self,
        input_path: str,
        target_format: str,
        output_path: Optional[str] = None,
        quality: str = 'medium',
        audio_bitrate_kbps: int = 128
    ) -> str:
        """
        Convert video to a different format.
        
        Args:
            input_path: Path to input video
            target_format: Target format (mp4, webm, avi, etc.)
            output_path: Output path (optional)
            quality: Quality preset for conversion
            
        Returns:
            Path to converted video
        """
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input video not found: {input_path}")
        
        target_format = target_format.lower().lstrip('.')
        if target_format not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported target format: {target_format}")
        
        # Determine output path
        if not output_path:
            output_path = self.output_dir / "converted" / f"{input_path.stem}_converted.{target_format}"
        else:
            output_path = Path(output_path)
        
        print(f"Converting {input_path.name} to {target_format.upper()}")
        
        try:
            with VideoFileClip(str(input_path)) as video:
                format_settings = self.SUPPORTED_FORMATS[target_format]
                quality_settings = self.COMPRESSION_PRESETS.get(quality, self.COMPRESSION_PRESETS['medium'])
                
                # Format-specific parameters
                ffmpeg_params = [
                    '-crf', str(quality_settings['crf']),
                    '-preset', quality_settings['preset'],
                    '-pix_fmt', 'yuv420p'
                ]
                
                if target_format == 'mp4':
                    ffmpeg_params.extend(['-movflags', '+faststart'])
                elif target_format == 'webm':
                    ffmpeg_params.extend(['-b:v', '0'])
                
                has_audio = video.audio is not None
                video.write_videofile(
                    str(output_path),
                    codec=format_settings['video_codec'],
                    audio_codec=format_settings['audio_codec'],
                    audio=has_audio,
                    audio_bitrate=(f"{audio_bitrate_kbps}k" if has_audio else None),
                    ffmpeg_params=ffmpeg_params,
                    temp_audiofile=str(self.output_dir / "temp" / "temp_audio.m4a"),
                    remove_temp=True
                )
            
            print(f"Conversion complete: {output_path}")
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Error converting video: {str(e)}")
    
    @classmethod
    def list_supported_formats(cls) -> Dict[str, Dict[str, str]]:
        """Return list of supported formats with their codecs."""
        return cls.SUPPORTED_FORMATS.copy()
    
    @classmethod
    def list_compression_presets(cls) -> Dict[str, Dict[str, Any]]:
        """Return list of available compression presets."""
        return cls.COMPRESSION_PRESETS.copy()
