import logging
import logging.config
import os
from datetime import datetime
from typing import Dict, Any

def setup_logging(config: Dict[str, Any] = None) -> None:
    """Setup comprehensive logging configuration"""
    
    config = config or {}
    log_level = config.get('LOG_LEVEL', 'INFO')
    log_file = config.get('LOG_FILE', 'app.log')
    log_dir = config.get('LOG_DIR', 'logs')
    
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file_path = os.path.join(log_dir, log_file)
    
    # Comprehensive logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(asctime)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'simple',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': log_level,
                'formatter': 'detailed',
                'filename': log_file_path,
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': os.path.join(log_dir, 'errors.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 3,
                'encoding': 'utf8'
            },
            'algorithm_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'json',
                'filename': os.path.join(log_dir, 'algorithms.log'),
                'maxBytes': 20971520,  # 20MB
                'backupCount': 3,
                'encoding': 'utf8'
            },
            'performance_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'json',
                'filename': os.path.join(log_dir, 'performance.log'),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            # Root logger
            '': {
                'level': log_level,
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            # Algorithm-specific logging
            'algorithms': {
                'level': 'DEBUG',
                'handlers': ['algorithm_file'],
                'propagate': True
            },
            'algorithms.deep_learning': {
                'level': 'DEBUG',
                'handlers': ['algorithm_file'],
                'propagate': True
            },
            'algorithms.traditional_ml': {
                'level': 'DEBUG',
                'handlers': ['algorithm_file'],
                'propagate': True
            },
            'algorithms.similarity': {
                'level': 'DEBUG',
                'handlers': ['algorithm_file'],
                'propagate': True
            },
            # Core system logging
            'core': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': True
            },
            'core.algorithm_manager': {
                'level': 'INFO',
                'handlers': ['performance_file'],
                'propagate': True
            },
            # API logging
            'api': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': True
            },
            'flask': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': True
            },
            'werkzeug': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False
            },
            # Utilities logging
            'utils': {
                'level': 'INFO',
                'handlers': ['file'],
                'propagate': True
            },
            # Third-party libraries
            'transformers': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            },
            'torch': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            },
            'tensorflow': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            },
            'sklearn': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            },
            'xgboost': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            },
            'spacy': {
                'level': 'WARNING',
                'handlers': ['file'],
                'propagate': False
            }
        }
    }
    
    # Apply logging configuration
    logging.config.dictConfig(logging_config)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("="*50)
    logger.info("Resume Ranking System - Logging Initialized")
    logger.info(f"Log Level: {log_level}")
    logger.info(f"Log Directory: {log_dir}")
    logger.info(f"Main Log File: {log_file_path}")
    logger.info("="*50)

class PerformanceLogger:
    """Specialized logger for performance metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger('performance')
    
    def log_algorithm_performance(self, algorithm_name: str, processing_time: float, 
                                 resume_count: int, success: bool, details: Dict[str, Any] = None):
        """Log algorithm performance metrics"""
        
        performance_data = {
            'algorithm': algorithm_name,
            'processing_time': processing_time,
            'resume_count': resume_count,
            'avg_time_per_resume': processing_time / max(resume_count, 1),
            'success': success,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if details:
            performance_data.update(details)
        
        if success:
            self.logger.info(f"Algorithm Performance: {performance_data}")
        else:
            self.logger.error(f"Algorithm Failed: {performance_data}")
    
    def log_request_performance(self, endpoint: str, method: str, processing_time: float,
                               status_code: int, resume_count: int = 0, algorithm_count: int = 0):
        """Log API request performance"""
        
        request_data = {
            'endpoint': endpoint,
            'method': method,
            'processing_time': processing_time,
            'status_code': status_code,
            'resume_count': resume_count,
            'algorithm_count': algorithm_count,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        self.logger.info(f"Request Performance: {request_data}")

class AlgorithmLogger:
    """Specialized logger for algorithm-specific events"""
    
    def __init__(self):
        self.logger = logging.getLogger('algorithms')
    
    def log_model_loading(self, algorithm_name: str, model_name: str, loading_time: float, success: bool):
        """Log model loading events"""
        
        loading_data = {
            'event': 'model_loading',
            'algorithm': algorithm_name,
            'model_name': model_name,
            'loading_time': loading_time,
            'success': success,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if success:
            self.logger.info(f"Model Loaded: {loading_data}")
        else:
            self.logger.error(f"Model Loading Failed: {loading_data}")
    
    def log_processing_result(self, algorithm_name: str, resume_index: int, 
                            score: float, processing_time: float, details: Dict[str, Any] = None):
        """Log individual processing results"""
        
        result_data = {
            'event': 'processing_result',
            'algorithm': algorithm_name,
            'resume_index': resume_index,
            'score': score,
            'processing_time': processing_time,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if details:
            result_data['details'] = details
        
        self.logger.debug(f"Processing Result: {result_data}")
    
    def log_error(self, algorithm_name: str, error_type: str, error_message: str, 
                  resume_index: int = None, additional_info: Dict[str, Any] = None):
        """Log algorithm errors"""
        
        error_data = {
            'event': 'algorithm_error',
            'algorithm': algorithm_name,
            'error_type': error_type,
            'error_message': error_message,
            'resume_index': resume_index,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if additional_info:
            error_data.update(additional_info)
        
        self.logger.error(f"Algorithm Error: {error_data}")

# Global logger instances
performance_logger = PerformanceLogger()
algorithm_logger = AlgorithmLogger()
