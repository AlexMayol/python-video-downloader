import os
import requests
import subprocess
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
from urllib.parse import urlparse

def download_video(url, output_path):
    """
    Download video from URL
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False

def optimize_video(input_path, output_path, max_width=720, max_height=480, target_bitrate="500k"):
    """
    Optimize video size by reducing resolution and bitrate
    """
    try:
        # Load the video
        video = VideoFileClip(input_path)
        
        # Get original dimensions
        width, height = video.size
        
        # Calculate new dimensions while maintaining aspect ratio
        if width > max_width or height > max_height:
            if width/height > max_width/max_height:
                new_width = max_width
                new_height = int(height * (max_width/width))
            else:
                new_height = max_height
                new_width = int(width * (max_height/height))
        else:
            new_width, new_height = width, height
        
        # Ensure dimensions are even numbers
        new_width = new_width if new_width % 2 == 0 else new_width - 1
        new_height = new_height if new_height % 2 == 0 else new_height - 1
        
        # Resize video
        video = video.resize((new_width, new_height))
        
        # Write optimized video with more aggressive compression
        video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            bitrate=target_bitrate,
            preset='veryslow',  # More aggressive compression
            threads=4,  # Use multiple threads for faster processing
            ffmpeg_params=[
                '-crf', '28',  # Constant Rate Factor (lower = better quality, higher = smaller size)
                '-movflags', '+faststart',  # Enable fast start for web playback
                '-pix_fmt', 'yuv420p',  # Use 4:2:0 chroma subsampling
                '-profile:v', 'baseline',  # Use baseline profile for better compatibility
                '-level', '3.1'  # Adjusted level for better compatibility
            ]
        )
        
        # Get original and new file sizes
        original_size = os.path.getsize(input_path) / 1024  # KB
        new_size = os.path.getsize(output_path) / 1024  # KB
        
        print(f"Optimized {os.path.basename(input_path)}:")
        print(f"Original size: {original_size:.2f} KB")
        print(f"New size: {new_size:.2f} KB")
        print(f"Reduction: {((original_size - new_size) / original_size) * 100:.2f}%")
        
        video.close()
        return True
    except Exception as e:
        print(f"Error optimizing {input_path}: {str(e)}")
        return False

def extract_first_frame(video_path, output_path):
    """
    Extract the first frame from a video with aggressive optimization for web
    """
    try:
        # Load the video
        video = VideoFileClip(video_path)
        
        # Get the first frame (this returns RGB)
        first_frame = video.get_frame(0)
        
        # Convert numpy array to PIL Image with correct color handling
        frame_image = Image.fromarray(first_frame.astype('uint8'), 'RGB')
        
        # 1. First resize if too large (keeping aspect ratio)
        max_size = (1280, 720)  # Reduce to 720p resolution
        frame_image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 2. Convert output path to WebP (which provides better compression)
        output_path = os.path.splitext(output_path)[0] + '.webp'
        
        # 3. Save with aggressive optimization
        frame_image.save(
            output_path,
            'WEBP',
            quality=75,  # Lower quality for smaller size
            method=6,    # Highest compression method
            lossless=False,
            exact=False
        )
        
        # Print original and compressed sizes
        original_size = len(frame_image.tobytes()) / 1024  # KB
        compressed_size = os.path.getsize(output_path) / 1024  # KB
        print(f"Frame extracted and optimized:")
        print(f"Original size: {original_size:.2f} KB")
        print(f"Compressed size: {compressed_size:.2f} KB")
        print(f"Reduction: {((original_size - compressed_size) / original_size) * 100:.2f}%")
        
        video.close()
        return True
    except Exception as e:
        print(f"Error extracting frame from {video_path}: {str(e)}")
        return False

def process_videos_from_urls(urls_file):
    """
    Process videos from URLs listed in a file using keys as filenames
    """
    script_dir = os.path.dirname(urls_file)
    
    # Create all necessary directories
    downloads_dir = os.path.join(script_dir, "downloads")
    optimized_dir = os.path.join(script_dir, "optimized")
    frames_dir = os.path.join(script_dir, "frames")
    dist_dir = os.path.join(script_dir, "dist")
    
    # Create working directories
    for directory in [downloads_dir, optimized_dir, frames_dir]:
        os.makedirs(directory, exist_ok=True)
    
    # Remove old dist directory if exists and create new one
    if os.path.exists(dist_dir):
        import shutil
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Read URLs from file and parse them
    with open(urls_file, 'r') as f:
        # Skip empty lines and parse key: URL format
        lines = [line.strip() for line in f if line.strip()]
        video_data = []
        for line in lines:
            if ': ' in line:
                key, url = [part.strip() for part in line.split(':', 1)]
                video_data.append((key, url))
            else:
                print(f"Skipping malformed line: {line}")
                continue
    
    # Process each video
    for key, url in video_data:
        try:
            # Create paths with key-based names
            download_path = os.path.join(downloads_dir, f"{key}.mp4")
            optimized_path = os.path.join(optimized_dir, f"{key}.mp4")
            frame_path = os.path.join(frames_dir, f"{key}_poster.webp")
            
            print(f"\nProcessing {key}...")
            
            # Download video
            if not download_video(url, download_path):
                continue
            
            # Optimize video
            if optimize_video(download_path, optimized_path):
                # Extract first frame
                extract_first_frame(optimized_path, frame_path)
                
                # Clean up downloaded file
                os.remove(download_path)
                
        except Exception as e:
            print(f"Error processing {key}: {str(e)}")
    
    # Move processed files to dist directory
    print("\nMoving processed files to dist directory...")
    for file in os.listdir(optimized_dir):
        if file.endswith('.mp4'):
            src = os.path.join(optimized_dir, file)
            dst = os.path.join(dist_dir, file)
            os.rename(src, dst)
    
    for file in os.listdir(frames_dir):
        if file.endswith('.webp'):
            src = os.path.join(frames_dir, file)
            dst = os.path.join(dist_dir, file)
            os.rename(src, dst)
    
    # Clean up working directories
    os.rmdir(downloads_dir)
    os.rmdir(optimized_dir)
    os.rmdir(frames_dir)
    
    # Create zip archive
    print("\nCreating zip archive...")
    import subprocess
    zip_path = dist_dir + '.zip'
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    try:
        subprocess.run(['zip', '-r', zip_path, dist_dir], check=True)
        print(f"\nArchive created successfully: {os.path.basename(zip_path)}")
        
        # Get the size of the zip file
        zip_size = os.path.getsize(zip_path) / (1024 * 1024)  # Convert to MB
        print(f"Archive size: {zip_size:.2f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Error creating archive: {str(e)}")

if __name__ == "__main__":
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urls_file = os.path.join(script_dir, "urls.txt")
    process_videos_from_urls(urls_file) 
