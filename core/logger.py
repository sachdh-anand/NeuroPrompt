"""
Logging configuration with colored terminal output and clean log files.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()

class LogSymbols:
    """Symbols for different log levels and states."""
    DEBUG = "🔍"
    INFO = "ℹ️ "
    SUCCESS = "✅"
    WARNING = "⚠️ "
    ERROR = "❌"
    CRITICAL = "🚨"
    START = "▶️ "
    END = "⏹️ "
    DIVIDER = "━"
    TEST = "🧪"
    API = "🌐"
    MODEL = "🤖"

class ConsoleFormatter(logging.Formatter):
    """Formatter for console output with colors and symbols."""
    
    def format(self, record):
        # Store original message and level
        original_msg = record.msg
        original_levelname = record.levelname
        
        # Determine color and symbol first
        symbol = LogSymbols.INFO
        color = Fore.CYAN
        
        # Check log level and content to determine appropriate color and symbol
        is_success = "success" in original_msg.lower() or "completed" in original_msg.lower()
        
        if record.levelno >= logging.ERROR:
            symbol = LogSymbols.ERROR
            color = Fore.RED
            record.levelname = "ERROR"
        elif record.levelno >= logging.WARNING:
            symbol = LogSymbols.WARNING
            color = Fore.YELLOW
            record.levelname = "WARN"
        elif is_success:
            symbol = LogSymbols.SUCCESS
            color = Fore.GREEN
        elif "test" in original_msg.lower():
            symbol = LogSymbols.TEST
        elif "api" in original_msg.lower():
            symbol = LogSymbols.API
        elif "model" in original_msg.lower():
            symbol = LogSymbols.MODEL
            
        # Add context symbols
        if "starting" in original_msg.lower():
            symbol = LogSymbols.START
        elif "finished" in original_msg.lower() or "completed" in original_msg.lower():
            symbol = LogSymbols.END
        
        # Apply color to the entire formatted line
        record.msg = f"{symbol}  {original_msg}"
        formatted_msg = super().format(record)
        
        # Apply appropriate color to the entire line
        if record.levelno >= logging.ERROR:
            colored_msg = f"{Fore.RED}{formatted_msg}{Style.RESET_ALL}"
        elif record.levelno >= logging.WARNING:
            colored_msg = f"{Fore.YELLOW}{formatted_msg}{Style.RESET_ALL}"
        elif is_success:
            colored_msg = f"{Fore.GREEN}{formatted_msg}{Style.RESET_ALL}"
        else:
            colored_msg = f"{color}{formatted_msg}{Style.RESET_ALL}"
        
        # Restore original record state
        record.msg = original_msg
        record.levelname = original_levelname
        
        return colored_msg

class FileFormatter(logging.Formatter):
    """Clean formatter for file output without escape codes."""
    
    def format(self, record):
        # Add symbols based on content without color codes
        symbol = LogSymbols.INFO
        
        if record.levelno >= logging.ERROR:
            symbol = LogSymbols.ERROR
        elif record.levelno >= logging.WARNING:
            symbol = LogSymbols.WARNING
        elif "success" in record.msg.lower() or "completed" in record.msg.lower():
            symbol = LogSymbols.SUCCESS
        elif "test" in record.msg.lower():
            symbol = LogSymbols.TEST
        elif "api" in record.msg.lower():
            symbol = LogSymbols.API
        elif "model" in record.msg.lower():
            symbol = LogSymbols.MODEL
            
        # Add context symbols
        if "starting" in record.msg.lower():
            symbol = LogSymbols.START
        elif "finished" in record.msg.lower() or "completed" in record.msg.lower():
            symbol = LogSymbols.END
        
        # Format message with symbol but no color
        original_msg = record.msg
        record.msg = f"{symbol}  {record.msg}"
        
        # Format and return
        formatted = super().format(record)
        record.msg = original_msg
        return formatted
        
class Logger:
    """Clean logger configuration with separate formatters for console and file."""
    
    @staticmethod
    def get_default_log_file() -> str:
        """Get the default log file path."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        return str(log_dir / f"NeuroPrompt_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log")

    @staticmethod
    def setup(log_file: Optional[str] = None) -> logging.Logger:
        """Set up and configure the logger.
        
        Args:
            log_file: Optional path to the log file. If None, logs to console only.
            
        Returns:
            logging.Logger: Configured logger instance.
        """
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            
        # Create console handler with colored formatter
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = ConsoleFormatter(
            fmt='%(asctime)s │ %(levelname)-7s │ %(name)-12s │ %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        root_logger.addHandler(console_handler)
        
        # File handler if specified with clean formatter
        if log_file:
            try:
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_formatter = FileFormatter(
                    fmt='%(asctime)s │ %(levelname)-7s │ %(name)-12s │ %(message)s',
                    datefmt='%H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                file_handler.setLevel(logging.INFO)
                root_logger.addHandler(file_handler)
                print(f"{LogSymbols.SUCCESS} Log file: {log_file}")
            except Exception as e:
                print(f"{LogSymbols.ERROR} Could not create log file: {e}")
        
        # Log startup
        divider = f"{LogSymbols.DIVIDER * 50}"
        root_logger.info(f"NeuroPrompt Starting {LogSymbols.START}")
        root_logger.info(divider)
        
        return root_logger

# Create the default logger instance
default_log_file = Logger.get_default_log_file()
main_logger = Logger.setup(log_file=default_log_file)

def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    module_name = name.split('.')[-1]
    return logging.getLogger(module_name) 