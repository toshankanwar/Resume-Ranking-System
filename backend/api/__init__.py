"""API package for Resume Ranking System"""

from .routes import create_routes
from .middleware import setup_middleware
from .error_handlers import register_error_handlers

__all__ = [
    'create_routes',
    'setup_middleware',
    'register_error_handlers'
]
