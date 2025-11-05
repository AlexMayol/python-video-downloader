"""
Video downloading service supporting various sources.
"""

import os
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse


class VideoDownloader:
    """Service for downloading videos from URLs."""
    
    def __init__(self, output_dir: str = "output/downloads"):
        """Initialize downloader with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_video(
        self,
        url: str,
        output_path: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Download video from URL.
        
        Args:
            url: Video URL to download
            output_path: Specific output path (optional)
            filename: Custom filename (optional)
            
        Returns:
            Path to downloaded video
        """
        if not output_path:
            if not filename:
                # Extract filename from URL
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename or '.' not in filename:
                    filename = "downloaded_video.mp4"
            
            output_path = self.output_dir / filename
        else:
            output_path = Path(output_path)
        
        print(f"Downloading video from: {url}")
        print(f"Saving to: {output_path}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Simple progress indicator
                        if total_size > 0:
                            progress = (downloaded_size / total_size) * 100
                            print(f"\rProgress: {progress:.1f}%", end='', flush=True)
            
            print(f"\nDownload complete: {output_path}")
            return str(output_path)
            
        except requests.RequestException as e:
            raise RuntimeError(f"Error downloading video: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during download: {str(e)}")
    
    def download_from_config(self, video_config: Dict[str, Any]) -> str:
        """Download video using configuration dict."""
        url = video_config.get('url')
        if not url:
            raise ValueError("Video configuration must include 'url'")
        
        name = video_config.get('name')
        format_ext = video_config.get('format', 'mp4')
        
        filename = f"{name}.{format_ext}" if name else None
        
        return self.download_video(url, filename=filename)
