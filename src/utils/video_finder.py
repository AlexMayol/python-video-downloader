"""
Video file discovery and management utilities.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class VideoFinder:
    """Utility class for finding and managing local video files."""
    
    SUPPORTED_EXTENSIONS = [
        '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v',
        '.MP4', '.AVI', '.MOV', '.MKV', '.WMV', '.FLV', '.WEBM', '.M4V'
    ]
    
    def __init__(self, base_dir: str = "."):
        """Initialize with base directory."""
        self.base_dir = Path(base_dir)
        self.local_videos_dir = self.base_dir / "local_videos"
        
        # Create local_videos directory if it doesn't exist
        self.local_videos_dir.mkdir(exist_ok=True)
    
    def find_videos(self, directory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Find all video files in the specified directory or local_videos folder.
        
        Args:
            directory: Directory to search (defaults to local_videos/)
            
        Returns:
            List of video file information dictionaries
        """
        search_dir = Path(directory) if directory else self.local_videos_dir
        
        if not search_dir.exists():
            return []
        
        videos = []
        for ext in self.SUPPORTED_EXTENSIONS:
            for video_path in search_dir.glob(f"*{ext}"):
                if video_path.is_file():
                    videos.append(self._get_video_info(video_path))
        
        # Sort by name for consistent ordering
        return sorted(videos, key=lambda x: x['name'].lower())
    
    def _get_video_info(self, video_path: Path) -> Dict[str, Any]:
        """Get basic information about a video file."""
        stat = video_path.stat()
        return {
            'name': video_path.stem,
            'filename': video_path.name,
            'path': str(video_path),
            'size_mb': stat.st_size / (1024 * 1024),
            'extension': video_path.suffix.lower(),
            'relative_path': str(video_path.relative_to(self.base_dir))
        }
    
    def get_video_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get video info by name (without extension)."""
        videos = self.find_videos()
        for video in videos:
            if video['name'].lower() == name.lower():
                return video
        return None
    
    def get_video_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """Get video info by index in the list."""
        videos = self.find_videos()
        if 0 <= index < len(videos):
            return videos[index]
        return None
    
    def list_videos_formatted(self) -> str:
        """Return a formatted string listing all videos."""
        videos = self.find_videos()
        
        if not videos:
            return "📂 No videos found in local_videos/ folder.\n   Add some videos to get started!"
        
        output = ["📹 Videos in local_videos/ folder:", "=" * 40]
        
        for i, video in enumerate(videos, 1):
            size_str = f"{video['size_mb']:.1f} MB"
            output.append(f"  {i:2d}. {video['name']}{video['extension']} ({size_str})")
        
        output.append(f"\nTotal: {len(videos)} videos")
        return "\n".join(output)
    
    def ensure_local_videos_dir(self) -> str:
        """Ensure local_videos directory exists and return its path."""
        self.local_videos_dir.mkdir(exist_ok=True)
        return str(self.local_videos_dir)
    
    def get_video_choices(self) -> List[str]:
        """Get list of video names for command-line choices."""
        videos = self.find_videos()
        return [video['name'] for video in videos]
