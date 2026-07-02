"""Configuration manager for loading and managing application settings"""

import logging
from pathlib import Path
from typing import Dict, Any
import yaml

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration from YAML files"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self._ensure_default_configs()
    
    def _ensure_default_configs(self):
        """Create default config files if they don't exist"""
        defaults = {
            'app.yaml': {
                'app_name': 'Crash Analytics Pro',
                'version': '0.1.0',
                'debug': False,
                'data_dir': 'data',
            },
            'database.yaml': {
                'type': 'sqlite',
                'path': 'data/analytics.db',
                'echo': False,
            },
            'readers.yaml': {
                'readers': []
            },
            'ui.yaml': {
                'window_width': 1400,
                'window_height': 900,
                'theme': 'dark',
            },
            'logging.yaml': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'handlers': ['console', 'file'],
            }
        }
        
        for filename, content in defaults.items():
            config_path = self.config_dir / filename
            if not config_path.exists():
                with open(config_path, 'w') as f:
                    yaml.dump(content, f, default_flow_style=False)
                logger.info(f"Created default config: {filename}")
    
    def load_config(self, filename: str) -> Dict[str, Any]:
        """Load a single config file"""
        config_path = self.config_dir / filename
        
        if not config_path.exists():
            logger.warning(f"Config file not found: {filename}")
            return {}
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.debug(f"Loaded config: {filename}")
                return config if config else {}
        except Exception as e:
            logger.error(f"Failed to load config {filename}: {e}")
            return {}
    
    def load_all_configs(self) -> Dict[str, Any]:
        """Load all configuration files"""
        configs = {}
        config_files = ['app.yaml', 'database.yaml', 'readers.yaml', 'ui.yaml', 'logging.yaml']
        
        for filename in config_files:
            config_name = filename.replace('.yaml', '')
            configs[config_name] = self.load_config(filename)
        
        return configs
    
    def save_config(self, filename: str, config: Dict[str, Any]) -> bool:
        """Save configuration to file"""
        config_path = self.config_dir / filename
        
        try:
            with open(config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            logger.info(f"Saved config: {filename}")
            return True
        except Exception as e:
            logger.error(f"Failed to save config {filename}: {e}")
            return False
