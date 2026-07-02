#!/usr/bin/env python
"""Main entry point for Crash Analytics Pro application"""

import sys
import logging
from pathlib import Path

# Setup path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logger import setup_logging

def main():
    """Initialize and run the application"""
    # Setup logging
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger = setup_logging()
    logger.info("Starting Crash Analytics Pro")
    
    try:
        # Import Qt after path is set
        from PySide6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        
        # Load configuration
        try:
            import yaml
            config_path = Path('config.yaml')
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                logger.info("Configuration loaded successfully")
            else:
                config = {}
                logger.warning("config.yaml not found, using defaults")
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            config = {}
        
        # Create Qt application
        app = QApplication(sys.argv)
        
        # Create and show main window
        window = MainWindow(config)
        window.show()
        logger.info("Main window created and displayed")
        
        # Run application
        sys.exit(app.exec())
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
