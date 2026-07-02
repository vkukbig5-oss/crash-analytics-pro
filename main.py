"""Main application entry point"""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication
from src.utils.logger import setup_logging
from src.ui.main_window import MainWindow
from src.config import load_config


def main():
    """Application entry point"""
    # Setup logging
    logger = setup_logging(level=logging.INFO)
    logger.info("Starting Crash Analytics Pro")
    
    # Load configuration
    config_path = Path('config.yaml')
    config = load_config(str(config_path))
    
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = MainWindow(config)
    window.show()
    
    logger.info("Application window displayed")
    
    # Run application
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
