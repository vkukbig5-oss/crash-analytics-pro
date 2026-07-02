#!/usr/bin/env python
"""Main entry point for Crash Analytics Pro application"""

import sys
import logging
from pathlib import Path

from src.config.config_manager import ConfigManager
from src.utils.logger import setup_logging
from src.ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication


def main():
    """Initialize and run the application"""
    # Setup logging
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger = setup_logging()
    logger.info("Starting Crash Analytics Pro")
    
    # Load configuration
    try:
        config_manager = ConfigManager()
        config = config_manager.load_all_configs()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        sys.exit(1)
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    try:
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
