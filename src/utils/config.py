"""
Configuration management utilities.
"""

import json
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
from typing import Dict, Any, Union, Optional
from dataclasses import dataclass, asdict


@dataclass
class ProcessingConfig:
    """Configuration for video processing operations."""
    max_width: Optional[int] = None
    max_height: Optional[int] = None
    scale_factor: Optional[float] = None
    compression_level: str = 'medium'
    output_format: Optional[str] = None
    lossless: bool = False
    output_dir: str = 'output'


@dataclass
class VideoConfig:
    """Configuration for individual video processing."""
    name: Optional[str] = None
    url: Optional[str] = None
    local_path: Optional[str] = None
    output_format: Optional[str] = None
    processing: Optional[ProcessingConfig] = None


class ConfigManager:
    """Manages configuration loading and saving."""
    
    SUPPORTED_FORMATS = ['.json', '.yaml', '.yml']
    
    @classmethod
    def load_config(cls, config_path: Union[str, Path]) -> Dict[str, Any]:
        """Load configuration from file."""
        config_path = Path(config_path)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        suffix = config_path.suffix.lower()
        
        if suffix == '.json':
            return cls._load_json(config_path)
        elif suffix in ['.yaml', '.yml']:
            return cls._load_yaml(config_path)
        else:
            raise ValueError(f"Unsupported config format: {suffix}")
    
    @classmethod
    def save_config(cls, config: Dict[str, Any], config_path: Union[str, Path]) -> None:
        """Save configuration to file."""
        config_path = Path(config_path)
        suffix = config_path.suffix.lower()
        
        if suffix == '.json':
            cls._save_json(config, config_path)
        elif suffix in ['.yaml', '.yml']:
            cls._save_yaml(config, config_path)
        else:
            raise ValueError(f"Unsupported config format: {suffix}")
    
    @staticmethod
    def _load_json(path: Path) -> Dict[str, Any]:
        """Load JSON configuration."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def _save_json(config: Dict[str, Any], path: Path) -> None:
        """Save JSON configuration."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def _load_yaml(path: Path) -> Dict[str, Any]:
        """Load YAML configuration."""
        if not HAS_YAML:
            raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    @staticmethod
    def _save_yaml(config: Dict[str, Any], path: Path) -> None:
        """Save YAML configuration."""
        if not HAS_YAML:
            raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    @staticmethod
    def create_default_config() -> Dict[str, Any]:
        """Create a default configuration."""
        return {
            "processing": {
                "max_width": 1920,
                "max_height": 1080,
                "compression_level": "medium",
                "output_format": "mp4",
                "lossless": False,
                "output_dir": "output"
            },
            "videos": [
                {
                    "name": "example_video",
                    "url": "https://example.com/video.mp4",
                    "output_format": "mp4"
                }
            ]
        }
    
    @staticmethod
    def create_local_processing_config() -> Dict[str, Any]:
        """Create a configuration template for local video processing."""
        return {
            "processing": {
                "max_width": 1920,
                "max_height": 1080,
                "compression_level": "medium",
                "output_format": "mp4",
                "lossless": False,
                "output_dir": "output"
            },
            "local_videos": [
                {
                    "name": "my_video",
                    "local_path": "/path/to/video.mp4",
                    "output_format": "webm",
                    "processing": {
                        "max_width": 1280,
                        "compression_level": "high"
                    }
                }
            ]
        }
    
    @staticmethod
    def validate_config(config: Dict[str, Any]) -> bool:
        """Validate configuration structure."""
        required_keys = ['processing']
        
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required configuration key: {key}")
        
        # Validate processing config
        processing = config['processing']
        valid_compression_levels = ['lossless', 'high', 'medium', 'low', 'very_low']
        
        if 'compression_level' in processing:
            if processing['compression_level'] not in valid_compression_levels:
                raise ValueError(f"Invalid compression level. Must be one of: {valid_compression_levels}")
        
        return True
