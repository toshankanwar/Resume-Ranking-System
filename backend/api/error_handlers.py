from flask import jsonify, request, current_app
import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
import sys
import os

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Register comprehensive error handlers for the Flask application"""
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors"""
        logger.warning(f"Bad request: {request.url} - {error.description}")
        return jsonify({
            'success': False,
            'error': 'Bad Request',
            'message': error.description or 'The request was malformed or invalid',
            'status_code': 400,
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.path,
            'method': request.method
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized access errors"""
        logger.warning(f"Unauthorized access: {request.url} - {request.remote_addr}")
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Authentication required or invalid credentials',
            'status_code': 401,
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.path
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden access errors"""
        logger.warning(f"Forbidden access: {request.url} - {request.remote_addr}")
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'Access denied. Insufficient permissions',
            'status_code': 403,
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.path
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors"""
        logger.info(f"404 Not Found: {request.url}")
        return jsonify({
            'success': False,
            'error': 'Not Found',
            'message': f'The requested endpoint {request.path} was not found',
            'status_code': 404,
            'timestamp': datetime.utcnow().isoformat(),
            'available_endpoints': _get_available_endpoints(),
            'suggestions': _get_endpoint_suggestions(request.path)
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors"""
        logger.warning(f"Method not allowed: {request.method} {request.url}")
        return jsonify({
            'success': False,
            'error': 'Method Not Allowed',
            'message': f'The {request.method} method is not allowed for {request.path}',
            'status_code': 405,
            'allowed_methods': error.valid_methods if hasattr(error, 'valid_methods') else [],
            'timestamp': datetime.utcnow().isoformat()
        }), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file/request too large errors"""
        max_size_mb = app.config.get('MAX_CONTENT_LENGTH', 0) // (1024 * 1024)
        logger.warning(f"Request too large: {request.url} - Content-Length: {request.content_length}")
        return jsonify({
            'success': False,
            'error': 'Request Entity Too Large',
            'message': f'File or request size exceeds the maximum limit of {max_size_mb}MB',
            'status_code': 413,
            'max_size_mb': max_size_mb,
            'received_size_mb': (request.content_length // (1024 * 1024)) if request.content_length else 'unknown',
            'timestamp': datetime.utcnow().isoformat(),
            'tips': [
                'Reduce file size by compressing documents',
                'Upload files in smaller batches',
                'Check if files are corrupted or unusually large'
            ]
        }), 413
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        """Handle unsupported media type errors"""
        logger.warning(f"Unsupported media type: {request.content_type} for {request.url}")
        return jsonify({
            'success': False,
            'error': 'Unsupported Media Type',
            'message': f'Content type {request.content_type} is not supported',
            'status_code': 415,
            'received_content_type': request.content_type,
            'supported_types': [
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword',
                'multipart/form-data'
            ],
            'timestamp': datetime.utcnow().isoformat()
        }), 415
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle validation/processing errors"""
        logger.warning(f"Unprocessable entity: {request.url} - {error.description}")
        return jsonify({
            'success': False,
            'error': 'Unprocessable Entity',
            'message': error.description or 'The request was well-formed but contains invalid data',
            'status_code': 422,
            'timestamp': datetime.utcnow().isoformat(),
            'path': request.path,
            'validation_help': {
                'supported_formats': ['.pdf', '.docx', '.doc'],
                'required_fields': ['jobDescription', 'methods'],
                'max_files': app.config.get('MAX_FILES_PER_REQUEST', 50),
                'job_description_min_length': 20
            }
        }), 422
    
    @app.errorhandler(429)
    def too_many_requests(error):
        """Handle rate limiting errors"""
        logger.warning(f"Rate limit exceeded: {request.remote_addr} - {request.url}")
        return jsonify({
            'success': False,
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded. Please try again later',
            'status_code': 429,
            'timestamp': datetime.utcnow().isoformat(),
            'retry_after': '60 seconds',
            'rate_limit_info': {
                'current_usage': 'exceeded',
                'reset_time': 'in 60 seconds',
                'limit_type': 'requests per minute'
            }
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors"""
        error_id = f"error_{int(datetime.utcnow().timestamp())}_{hash(str(error)) % 10000}"
        
        # Log detailed error information
        logger.error(f"Internal server error [{error_id}]: {request.url}")
        logger.error(f"Error details: {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Different response based on debug mode
        if app.debug:
            return jsonify({
                'success': False,
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred while processing your request',
                'status_code': 500,
                'error_id': error_id,
                'timestamp': datetime.utcnow().isoformat(),
                'debug_info': {
                    'error_type': type(error).__name__,
                    'error_message': str(error),
                    'traceback': traceback.format_exc().split('\n')[-10:],  # Last 10 lines
                    'request_info': {
                        'path': request.path,
                        'method': request.method,
                        'remote_addr': request.remote_addr,
                        'user_agent': str(request.user_agent)[:200]
                    }
                }
            }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred while processing your request. Please try again later.',
                'status_code': 500,
                'error_id': error_id,
                'timestamp': datetime.utcnow().isoformat(),
                'support': {
                    'contact': 'Please contact support with the error ID if the problem persists',
                    'error_id': error_id,
                    'troubleshooting': [
                        'Check if all required fields are provided',
                        'Verify file formats are supported',
                        'Try with fewer files or smaller file sizes',
                        'Check network connection stability'
                    ]
                }
            }), 500
    
    @app.errorhandler(502)
    def bad_gateway(error):
        """Handle bad gateway errors"""
        logger.error(f"Bad gateway: {request.url}")
        return jsonify({
            'success': False,
            'error': 'Bad Gateway',
            'message': 'Unable to connect to upstream service',
            'status_code': 502,
            'timestamp': datetime.utcnow().isoformat()
        }), 502
    
    @app.errorhandler(503)
    def service_unavailable(error):
        """Handle service unavailable errors"""
        logger.error(f"Service unavailable: {request.url}")
        return jsonify({
            'success': False,
            'error': 'Service Unavailable',
            'message': 'Service is temporarily unavailable. Please try again later.',
            'status_code': 503,
            'timestamp': datetime.utcnow().isoformat(),
            'estimated_recovery': '5-10 minutes',
            'status_page': 'Check system status for updates'
        }), 503
    
    @app.errorhandler(504)
    def gateway_timeout(error):
        """Handle gateway timeout errors"""
        logger.error(f"Gateway timeout: {request.url}")
        return jsonify({
            'success': False,
            'error': 'Gateway Timeout',
            'message': 'The request timed out while processing. This may be due to high server load.',
            'status_code': 504,
            'timestamp': datetime.utcnow().isoformat(),
            'suggestions': [
                'Try processing fewer files at once',
                'Use faster algorithms (cosine, jaccard) for quicker results',
                'Retry the request in a few minutes'
            ]
        }), 504
    
    # Handle specific algorithm-related errors
    @app.errorhandler(AlgorithmError)
    def algorithm_error(error):
        """Handle algorithm-specific errors"""
        logger.error(f"Algorithm error: {error.algorithm} - {error.message}")
        return jsonify({
            'success': False,
            'error': 'Algorithm Processing Error',
            'message': f'Error in {error.algorithm} algorithm: {error.message}',
            'algorithm': error.algorithm,
            'error_type': error.error_type,
            'status_code': 422,
            'timestamp': datetime.utcnow().isoformat(),
            'fallback_options': {
                'available_algorithms': ['cosine', 'jaccard', 'ner'],
                'suggestion': 'Try using different algorithms or contact support'
            }
        }), 422
    
    # Handle file processing errors
    @app.errorhandler(FileProcessingError)
    def file_processing_error(error):
        """Handle file processing errors"""
        logger.error(f"File processing error: {error.filename} - {error.message}")
        return jsonify({
            'success': False,
            'error': 'File Processing Error',
            'message': f'Error processing file {error.filename}: {error.message}',
            'filename': error.filename,
            'error_type': error.error_type,
            'status_code': 422,
            'timestamp': datetime.utcnow().isoformat(),
            'file_requirements': {
                'supported_formats': ['.pdf', '.docx', '.doc'],
                'max_size_mb': app.config.get('MAX_CONTENT_LENGTH', 0) // (1024 * 1024),
                'content_requirements': 'File must contain readable text (minimum 50 characters)'
            }
        }), 422
    
    # Handle validation errors
    @app.errorhandler(ValidationError)
    def validation_error(error):
        """Handle validation errors"""
        logger.warning(f"Validation error: {error.field} - {error.message}")
        return jsonify({
            'success': False,
            'error': 'Validation Error',
            'message': error.message,
            'field': error.field,
            'value': error.value,
            'status_code': 400,
            'timestamp': datetime.utcnow().isoformat(),
            'validation_rules': error.validation_rules if hasattr(error, 'validation_rules') else {}
        }), 400
    
    # Handle timeout errors
    @app.errorhandler(TimeoutError)
    def timeout_error(error):
        """Handle timeout errors"""
        logger.error(f"Timeout error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Processing Timeout',
            'message': 'Request timed out while processing. Try with fewer files or simpler algorithms.',
            'status_code': 504,
            'timestamp': datetime.utcnow().isoformat(),
            'recommendations': [
                'Reduce the number of files in your request',
                'Use faster algorithms like cosine similarity',
                'Split large batches into smaller ones',
                'Check file sizes and complexity'
            ]
        }), 504
    
    # Generic exception handler for unexpected errors
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle any unexpected errors"""
        error_id = f"unexpected_{int(datetime.utcnow().timestamp())}_{hash(str(error)) % 10000}"
        
        logger.error(f"Unexpected error [{error_id}]: {type(error).__name__}: {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        if app.debug:
            return jsonify({
                'success': False,
                'error': 'Unexpected Error',
                'message': f'An unexpected error occurred: {str(error)}',
                'error_type': type(error).__name__,
                'error_id': error_id,
                'status_code': 500,
                'timestamp': datetime.utcnow().isoformat(),
                'debug_traceback': traceback.format_exc().split('\n')
            }), 500
        else:
            return jsonify({
                'success': False,
                'error': 'Unexpected Error',
                'message': 'An unexpected error occurred. Please try again later.',
                'error_id': error_id,
                'status_code': 500,
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    logger.info("Error handlers registered successfully")

def _get_available_endpoints() -> list:
    """Get list of available API endpoints"""
    endpoints = []
    for rule in current_app.url_map.iter_rules():
        if rule.rule.startswith('/api/'):
            endpoints.append({
                'endpoint': rule.rule,
                'methods': list(rule.methods - {'OPTIONS', 'HEAD'})
            })
    return endpoints

def _get_endpoint_suggestions(requested_path: str) -> list:
    """Get suggestions for similar endpoints"""
    available_paths = [rule.rule for rule in current_app.url_map.iter_rules() 
                      if rule.rule.startswith('/api/')]
    
    # Simple suggestion logic - find paths with similar words
    suggestions = []
    requested_words = set(requested_path.lower().split('/'))
    
    for path in available_paths:
        path_words = set(path.lower().split('/'))
        common_words = requested_words.intersection(path_words)
        
        if common_words and len(common_words) >= 1:
            suggestions.append(path)
    
    return suggestions[:3]  # Return top 3 suggestions

# Custom exception classes
class AlgorithmError(Exception):
    """Custom exception for algorithm-related errors"""
    def __init__(self, algorithm: str, message: str, error_type: str = 'processing_error'):
        self.algorithm = algorithm
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

class FileProcessingError(Exception):
    """Custom exception for file processing errors"""
    def __init__(self, filename: str, message: str, error_type: str = 'processing_error'):
        self.filename = filename
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)

class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, field: str, message: str, value: Any = None, validation_rules: Dict = None):
        self.field = field
        self.message = message
        self.value = value
        self.validation_rules = validation_rules or {}
        super().__init__(self.message)

class ProcessingTimeoutError(Exception):
    """Custom exception for processing timeout errors"""
    def __init__(self, operation: str, timeout_seconds: int):
        self.operation = operation
        self.timeout_seconds = timeout_seconds
        message = f"Operation '{operation}' timed out after {timeout_seconds} seconds"
        super().__init__(message)

def create_error_response(error_type: str, message: str, status_code: int = 400, 
                         additional_data: Dict[str, Any] = None) -> tuple:
    """Helper function to create consistent error responses"""
    
    response_data = {
        'success': False,
        'error': error_type,
        'message': message,
        'status_code': status_code,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if additional_data:
        response_data.update(additional_data)
    
    return jsonify(response_data), status_code

def log_error_context(error: Exception, additional_context: Dict[str, Any] = None):
    """Log detailed error context for debugging"""
    
    context = {
        'error_type': type(error).__name__,
        'error_message': str(error),
        'request_path': request.path if request else 'unknown',
        'request_method': request.method if request else 'unknown',
        'remote_addr': request.remote_addr if request else 'unknown',
        'timestamp': datetime.utcnow().isoformat(),
        'python_version': sys.version,
        'working_directory': os.getcwd()
    }
    
    if additional_context:
        context.update(additional_context)
    
    logger.error(f"Error Context: {context}")
    logger.error(f"Full Traceback: {traceback.format_exc()}")
