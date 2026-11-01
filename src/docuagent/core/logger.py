import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger.
    """
    logger = logging.getLogger(name)
    
    # Prevent adding multiple handlers if it already exists
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Output logs to the console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Standardize the log format: [Timestamp] - [Module Name] - [Level] - Message
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger