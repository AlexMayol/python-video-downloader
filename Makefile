# Makefile for python-video-downloader

.PHONY: deps run clean help

venv/bin/activate:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip

# Install dependencies from requirements.txt
# Also patches moviepy for Pillow >=10 compatibility

deps:
	make venv/bin/activate
	. venv/bin/activate && pip install --upgrade -r requirements.txt
	# Patch moviepy for Pillow >=10
	@find venv -name "resize.py" -path "*/moviepy/video/fx/*" -exec sed -i '' 's/Image.ANTIALIAS/Image.Resampling.LANCZOS/g' {} \;

# Run the main script
run:
	. venv/bin/activate && python3 video_processor.py

# Clean up generated files and virtual environment
clean:
	rm -rf venv dist dist.zip downloads optimized frames __pycache__

# Show help
help:
	@echo "Available targets:"
	@echo "  deps   - Set up virtual environment and install dependencies"
	@echo "  run    - Run the main video processor script"
	@echo "  clean  - Remove venv and all generated files"
	@echo "  help   - Show this help message" 
