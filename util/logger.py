"""
Logger Utility Module
Provides centralized logging functionality for the framework
"""
import logging
import os
from datetime import datetime
import colorlog


class Logger:
    """Centralized logger class for the framework"""
    
    _loggers = {}
    
    @staticmethod
    def get_logger(name: str, log_level: str = "INFO") -> logging.Logger:
        """
        Get or create logger instance
        
        Args:
            name: Logger name (usually module name)
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            logging.Logger: Configured logger instance
        """
        if name in Logger._loggers:
            return Logger._loggers[name]
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Avoid duplicate handlers
        if logger.handlers:
            return logger
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Create log file with timestamp
        log_file = os.path.join(
            log_dir, 
            f"automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler with colors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Store logger
        Logger._loggers[name] = logger
        
        return logger

