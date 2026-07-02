"""Logging configuration and utilities"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime


def setup_logging(log_dir: str = "logs", level: int = logging.INFO) -> logging.Logger:
    """Configure application logging"""
    log_dir = Path(log_dir)
    log_dir.mkdir(exist_ok=True)
    
    # Main logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    fh = logging.handlers.RotatingFileHandler(
        log_dir / 'app.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger
