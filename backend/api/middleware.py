from flask import request, g, jsonify, current_app
import time
import logging
import json
from functools import wraps
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

def setup_middleware(app):
    """Setup comprehensive middleware for the application"""
    
    @app.before_request
    def before_request():
        """Execute before each request"""
        g.start_time = time.time()
        g.request_id = f"req_{int(time.time())}_{hash(request.path) % 10000}"
        
        # Log incoming request
        logger.info(f"[{g.request_id}] {request.method} {request.path} - Start")
        
        # Add request context
        g.request_context = {
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_agent': request.user_agent.string[:200] if request.user_agent else 'Unknown',
            'content_type': request.content_type,
            'content_length': request.content_length
        }
    
    @app.after_request
    def after_request(response):
        """Execute after each request"""
        if hasattr(g, 'start_time'):
            total_time = time.time() - g.start_time
            
            # Log response
            logger.info(f"[{g.request_id}] {response.status_code} - {total_time:.3f}s")
            
            # Add performance headers
            response.headers['X-Response-Time'] = f"{total_time:.3f}s"
            response.headers['X-Request-ID'] = g.request_id
        
        # Add security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Processing-Methods, X-Files-Count'
        response.headers['Access-Control-Expose-Headers'] = 'X-Response-Time, X-Request-ID'
        
        return response
    
    @app.before_request
    def handle_preflight():
        """Handle CORS preflight requests"""
        if request.method == "OPTIONS":
            response = jsonify({'message': 'OK'})
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Processing-Methods, X-Files-Count'
            return response
    
    @app.before_request
    def rate_limiting():
        """Simple rate limiting (can be enhanced with Redis)"""
        # Skip rate limiting for health checks
        if request.path == '/api/health':
            return
        
        # Basic rate limiting logic (implement with Redis for production)
        # This is a placeholder - implement proper rate limiting as needed
        pass
    
    @app.before_request
    def request_size_limit():
        """Check request size limits"""
        if request.content_length:
            max_size = current_app.config.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024)
            if request.content_length > max_size:
                return jsonify({
                    'error': 'Request too large',
                    'max_size_mb': max_size // (1024 * 1024),
                    'received_size_mb': request.content_length // (1024 * 1024)
                }), 413

def require_api_key(f):
    """Decorator to require API key (optional middleware)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        # For development, we might skip API key validation
        if current_app.config.get('REQUIRE_API_KEY', False):
            if not api_key:
                return jsonify({'error': 'API key required'}), 401
            
            # Validate API key (implement your validation logic)
            if not _validate_api_key(api_key):
                return jsonify({'error': 'Invalid API key'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def log_request_details(f):
    """Decorator to log detailed request information"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        request_details = {
            'endpoint': request.endpoint,
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_agent': request.user_agent.string if request.user_agent else None,
            'content_type': request.content_type,
            'content_length': request.content_length,
            'files_count': len(request.files) if request.files else 0,
            'form_fields': list(request.form.keys()) if request.form else [],
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Request Details: {json.dumps(request_details)}")
        
        return f(*args, **kwargs)
    return decorated_function

def handle_file_upload_errors(f):
    """Decorator to handle file upload specific errors"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific file upload errors
            if 'file too large' in error_msg.lower():
                return jsonify({
                    'error': 'File too large',
                    'message': 'One or more files exceed the maximum size limit',
                    'max_size_mb': current_app.config.get('MAX_CONTENT_LENGTH', 0) // (1024 * 1024)
                }), 413
            
            elif 'unsupported file' in error_msg.lower():
                return jsonify({
                    'error': 'Unsupported file format',
                    'message': 'Please upload PDF, DOCX, or DOC files only',
                    'supported_formats': ['.pdf', '.docx', '.doc']
                }), 422
            
            elif 'empty file' in error_msg.lower():
                return jsonify({
                    'error': 'Empty file',
                    'message': 'One or more files appear to be empty'
                }), 422
            
            # Re-raise if not a file upload error
            raise e
    
    return decorated_function

def _validate_api_key(api_key: str) -> bool:
    """Validate API key (implement your logic here)"""
    # Placeholder implementation
    valid_keys = current_app.config.get('VALID_API_KEYS', [])
    return api_key in valid_keys

class RequestTracker:
    """Track request metrics and statistics"""
    
    def __init__(self):
        self.requests = []
        self.max_requests = 1000  # Keep last 1000 requests
    
    def add_request(self, request_data: Dict[str, Any]):
        """Add request to tracking"""
        self.requests.append(request_data)
        
        # Keep only recent requests
        if len(self.requests) > self.max_requests:
            self.requests = self.requests[-self.max_requests:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get request statistics"""
        if not self.requests:
            return {'message': 'No requests tracked'}
        
        total_requests = len(self.requests)
        avg_response_time = sum(r.get('response_time', 0) for r in self.requests) / total_requests
        
        status_codes = {}
        endpoints = {}
        
        for req in self.requests:
            status = req.get('status_code', 'unknown')
            endpoint = req.get('endpoint', 'unknown')
            
            status_codes[status] = status_codes.get(status, 0) + 1
            endpoints[endpoint] = endpoints.get(endpoint, 0) + 1
        
        return {
            'total_requests': total_requests,
            'avg_response_time': round(avg_response_time, 3),
            'status_codes': status_codes,
            'popular_endpoints': dict(sorted(endpoints.items(), key=lambda x: x[1], reverse=True)[:5])
        }

# Global request tracker instance
request_tracker = RequestTracker()
