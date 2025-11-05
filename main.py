#!/usr/bin/env python3
"""
Video Processing Suite - Main entry point for legacy compatibility.

This file maintains backward compatibility with the original interface
while providing access to the new enhanced functionality.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# Import the new CLI
from cli.main import VideoCLI


def main():
    """Main entry point - routes to appropriate interface."""
    # Check if we have legacy arguments
    if len(sys.argv) > 1 and any(arg in sys.argv for arg in ['--json-file', '--config']):
        # Handle legacy JSON file argument
        if '--json-file' in sys.argv:
            idx = sys.argv.index('--json-file')
            if idx + 1 < len(sys.argv):
                config_file = sys.argv[idx + 1]
                # Convert to new format
                sys.argv = ['main.py', 'batch', config_file]
    
    # Run the new CLI
    cli = VideoCLI()
    cli.run()


if __name__ == "__main__":
    main() 
