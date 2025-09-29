"""Configuration package for Resume Ranking System"""

from .settings import Config, config_dict
from .logging_config import setup_logging

__version__ = "1.0.0"
__author__ = "Resume Ranking Team"

# Export main configuration classes
__all__ = [
    'Config',
    'config_dict', 
    'setup_logging'
]
