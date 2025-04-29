import os
import argparse
import json
from video_processor import process_videos_from_json

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Video Downloader and Processor')
    parser.add_argument('--json-file', default='videos.json', help='Path to the JSON configuration file (default: videos.json)')
    
    args = parser.parse_args()
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(script_dir, args.json_file)
    
    # Process videos using the JSON configuration
    process_videos_from_json(json_file)

if __name__ == "__main__":
    main() 
