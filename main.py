import os
import argparse
from video_processor import process_videos_from_urls

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Video Downloader and Processor')
    parser.add_argument('--max-width', type=int, default=720, help='Maximum video width in pixels (default: 720)')
    parser.add_argument('--max-height', type=int, default=480, help='Maximum video height in pixels (default: 480)')
    parser.add_argument('--urls-file', default='urls.txt', help='Path to the file containing URLs (default: urls.txt)')
    
    args = parser.parse_args()
    
    # Print arguments being used
    print("\nUsing the following parameters:")
    print(f"Max width: {args.max_width}px")
    print(f"Max height: {args.max_height}px")
    print(f"URLs file: {args.urls_file}")
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    urls_file = os.path.join(script_dir, args.urls_file)
    
    # Process videos using the existing function with custom dimensions
    process_videos_from_urls(urls_file, max_width=args.max_width, max_height=args.max_height)

if __name__ == "__main__":
    main() 
