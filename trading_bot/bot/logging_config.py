"""Logging configuration for the trading bot."""

import logging
import logging.handlers
import os
from datetime import datetime

LOG_DIR = "logs"


def setup_logging(log_name: str = "trading_bot") -> logging.Logger:
    """
    Configure and return a logger instance.
    
    Args:
        log_name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    
    # Remove existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = logging.Formatter(
        fmt='%(levelname)s - %(message)s'
    )
    
    # File handler (DEBUG level and above)
    log_file = os.path.join(LOG_DIR, f"trading_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (INFO level and above)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger
