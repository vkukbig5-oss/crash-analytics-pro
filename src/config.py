"""Application configuration management"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    'app': {
        'name': 'Crash Analytics Pro',
        'version': '1.0.0',
        'debug': False,
    },
    'database': {
        'type': 'sqlite',
        'path': 'data/analytics.db',
    },
    'ui': {
        'theme': 'dark',
        'window_width': 1400,
        'window_height': 900,
    },
    'import': {
        'csv': {
            'enabled': True,
            'delimiter': ',',
        },
        'json': {
            'enabled': True,
        },
    },
}


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    config = DEFAULT_CONFIG.copy()
    
    try:
        if Path(config_path).exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    _merge_config(config, user_config)
            logger.info(f"Loaded configuration from {config_path}")
        else:
            logger.info(f"Config file not found at {config_path}, using defaults")
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
    
    return config


def _merge_config(base: Dict[str, Any], override: Dict[str, Any]) -> None:
    """Recursively merge override config into base config"""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _merge_config(base[key], value)
        else:
            base[key] = value
