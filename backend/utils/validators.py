from typing import Dict, List, Any, Optional, Union
import re
import os
from datetime import datetime
from flask import Request
import logging

logger = logging.getLogger(__name__)

class RequestValidator:
    """Comprehensive request validation for resume processing API"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.max_files = self.config.get('MAX_FILES_PER_REQUEST', 50)
        self.max_file_size = self.config.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024)  # 100MB
        self.allowed_extensions = self.config.get('ALLOWED_EXTENSIONS', {'pdf', 'docx', 'doc'})
        
        # Valid algorithms
        self.valid_algorithms = {
            'bert', 'distilbert', 'sbert', 'xlm',
            'xgboost', 'random_forest', 'svm', 'neural_network',
            'cosine', 'jaccard', 'ner'
        }
        
        # Valid positions
        self.valid_positions = {
            'sde', 'swe', 'ml_engineer', 'data_scientist', 'devops',
            'frontend', 'backend', 'fullstack', 'product_manager',
            'designer', 'qa_engineer', 'security_engineer', 'general'
        }
        
        # Validation rules
        self.validation_rules = {
            'job_description': {
                'min_length': 20,
                'max_length': 10000,
                'required_patterns': [],  # Optional regex patterns
                'forbidden_patterns': [r'<script.*?>.*?</script>']  # Security patterns
            },
            'algorithms': {
                'min_count': 1,
                'max_count': 10,
                'recommended_combinations': [
                    ['bert', 'cosine', 'ner'],
                    ['distilbert', 'jaccard'],
                    ['xgboost', 'random_forest', 'cosine']
                ]
            },
            'files': {
                'min_count': 1,
                'max_count': 50,
                'min_file_size': 100,  # 100 bytes
                'max_file_size': 10 * 1024 * 1024,  # 10MB per file
                'allowed_mime_types': [
                    'application/pdf',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'application/msword'
                ]
            }
        }
    
    def validate_process_request(self, request: Request) -> Dict[str, Any]:
        """
        Comprehensive validation for resume processing requests
        
        Returns:
            Dict with 'valid' boolean and error details if invalid
        """
        
        try:
            # Validate request structure
            structure_validation = self._validate_request_structure(request)
            if not structure_validation['valid']:
                return structure_validation
            
            # Validate files
            files_validation = self._validate_files(request.files.getlist('resumes'))
            if not files_validation['valid']:
                return files_validation
            
            # Validate job description
            job_description = request.form.get('jobDescription', '').strip()
            job_validation = self._validate_job_description(job_description)
            if not job_validation['valid']:
                return job_validation
            
            # Validate position
            position = request.form.get('position', 'general')
            position_validation = self._validate_position(position)
            if not position_validation['valid']:
                return position_validation
            
            # Validate algorithms
            methods = request.form.getlist('methods')
            algorithms_validation = self._validate_algorithms(methods)
            if not algorithms_validation['valid']:
                return algorithms_validation
            
            # Validate optional parameters
            options_validation = self._validate_options(request.form.get('options', '{}'))
            if not options_validation['valid']:
                return options_validation
            
            # Cross-field validation
            cross_validation = self._validate_cross_field_constraints(
                files=request.files.getlist('resumes'),
                methods=methods,
                job_description=job_description
            )
            if not cross_validation['valid']:
                return cross_validation
            
            return {'valid': True, 'message': 'All validations passed'}
            
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return {
                'valid': False,
                'error': 'Validation process failed',
                'details': str(e)
            }
    
    def _validate_request_structure(self, request: Request) -> Dict[str, Any]:
        """Validate basic request structure"""
        
        # Check content type for file uploads
        if not request.content_type or not request.content_type.startswith('multipart/form-data'):
            return {
                'valid': False,
                'error': 'Invalid content type',
                'details': 'Request must use multipart/form-data for file uploads',
                'received_content_type': request.content_type
            }
        
        # Check request size
        if request.content_length and request.content_length > self.max_file_size:
            return {
                'valid': False,
                'error': 'Request too large',
                'details': f'Request size exceeds {self.max_file_size // (1024*1024)}MB limit',
                'max_size_mb': self.max_file_size // (1024*1024),
                'received_size_mb': request.content_length // (1024*1024)
            }
        
        # Check required form fields exist
        required_fields = ['jobDescription', 'methods']
        missing_fields = []
        
        for field in required_fields:
            if field not in request.form or not request.form.get(field):
                missing_fields.append(field)
        
        if missing_fields:
            return {
                'valid': False,
                'error': 'Missing required fields',
                'missing_fields': missing_fields,
                'required_fields': required_fields
            }
        
        return {'valid': True}
    
    def _validate_files(self, files: List) -> Dict[str, Any]:
        """Validate uploaded files"""
        
        if not files or len(files) == 0:
            return {
                'valid': False,
                'error': 'No files provided',
                'details': 'At least one resume file must be uploaded'
            }
        
        if len(files) > self.max_files:
            return {
                'valid': False,
                'error': 'Too many files',
                'details': f'Maximum {self.max_files} files allowed',
                'max_files': self.max_files,
                'received_files': len(files)
            }
        
        # Validate individual files
        for i, file in enumerate(files):
            file_validation = self._validate_single_file(file, i)
            if not file_validation['valid']:
                return file_validation
        
        return {'valid': True}
    
    def _validate_single_file(self, file, index: int) -> Dict[str, Any]:
        """Validate a single uploaded file"""
        
        if not file or not file.filename:
            return {
                'valid': False,
                'error': f'File {index + 1}: Invalid file',
                'details': 'File appears to be empty or corrupted'
            }
        
        # Validate file extension
        if '.' not in file.filename:
            return {
                'valid': False,
                'error': f'File {index + 1}: No file extension',
                'filename': file.filename,
                'supported_extensions': list(self.allowed_extensions)
            }
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in self.allowed_extensions:
            return {
                'valid': False,
                'error': f'File {index + 1}: Unsupported file format',
                'filename': file.filename,
                'received_extension': extension,
                'supported_extensions': list(self.allowed_extensions)
            }
        
        # Validate file size
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if size == 0:
            return {
                'valid': False,
                'error': f'File {index + 1}: Empty file',
                'filename': file.filename
            }
        
        if size < self.validation_rules['files']['min_file_size']:
            return {
                'valid': False,
                'error': f'File {index + 1}: File too small',
                'filename': file.filename,
                'min_size_bytes': self.validation_rules['files']['min_file_size']
            }
        
        if size > self.validation_rules['files']['max_file_size']:
            return {
                'valid': False,
                'error': f'File {index + 1}: File too large',
                'filename': file.filename,
                'max_size_mb': self.validation_rules['files']['max_file_size'] // (1024*1024),
                'received_size_mb': size // (1024*1024)
            }
        
        return {'valid': True}
    
    def _validate_filename(self, filename: str) -> Dict[str, Any]:
        """Validate filename for security and format"""
        
        # Security checks
        if not filename or filename == '':
            return {'valid': False, 'error': 'Empty filename'}
        
        # Check for dangerous characters
        dangerous_chars = ['..', '/', '\\', '<', '>', '|', ':', '*', '?', '"']
        for char in dangerous_chars:
            if char in filename:
                return {
                    'valid': False,
                    'error': f'Filename contains dangerous character: {char}'
                }
        
        # Check filename length
        if len(filename) > 255:
            return {
                'valid': False,
                'error': 'Filename too long (max 255 characters)'
            }
        
        # Check for valid characters (alphanumeric, spaces, hyphens, underscores, dots)
        if not re.match(r'^[\w\s\-\.]+$', filename):
            return {
                'valid': False,
                'error': 'Filename contains invalid characters'
            }
        
        return {'valid': True}
    
    def _validate_job_description(self, job_description: str) -> Dict[str, Any]:
        """Validate job description content"""
        
        if not job_description:
            return {
                'valid': False,
                'error': 'Job description is required',
                'details': 'Please provide a detailed job description'
            }
        
        rules = self.validation_rules['job_description']
        
        # Length validation
        if len(job_description) < rules['min_length']:
            return {
                'valid': False,
                'error': 'Job description too short',
                'min_length': rules['min_length'],
                'received_length': len(job_description),
                'details': f'Job description must be at least {rules["min_length"]} characters'
            }
        
        if len(job_description) > rules['max_length']:
            return {
                'valid': False,
                'error': 'Job description too long',
                'max_length': rules['max_length'],
                'received_length': len(job_description),
                'details': f'Job description must not exceed {rules["max_length"]} characters'
            }
        
        # Security validation - check for potentially dangerous content
        for pattern in rules['forbidden_patterns']:
            if re.search(pattern, job_description, re.IGNORECASE):
                return {
                    'valid': False,
                    'error': 'Job description contains invalid content',
                    'details': 'Please remove any script or HTML tags'
                }
        
        # Content quality validation
        word_count = len(job_description.split())
        if word_count < 5:
            return {
                'valid': False,
                'error': 'Job description too brief',
                'details': 'Please provide a more detailed job description with at least 5 words'
            }
        
        return {'valid': True}
    
    def _validate_position(self, position: str) -> Dict[str, Any]:
        """Validate position type"""
        
        if not position:
            return {
                'valid': False,
                'error': 'Position is required'
            }
        
        if position not in self.valid_positions:
            return {
                'valid': False,
                'error': 'Invalid position type',
                'received_position': position,
                'valid_positions': list(self.valid_positions),
                'suggestions': self._get_position_suggestions(position)
            }
        
        return {'valid': True}
    
    def _validate_algorithms(self, methods: List[str]) -> Dict[str, Any]:
        """Validate selected algorithms"""
        
        if not methods or len(methods) == 0:
            return {
                'valid': False,
                'error': 'No algorithms selected',
                'details': 'At least one algorithm must be selected',
                'available_algorithms': list(self.valid_algorithms)
            }
        
        rules = self.validation_rules['algorithms']
        
        if len(methods) < rules['min_count']:
            return {
                'valid': False,
                'error': 'Too few algorithms selected',
                'min_count': rules['min_count'],
                'received_count': len(methods)
            }
        
        if len(methods) > rules['max_count']:
            return {
                'valid': False,
                'error': 'Too many algorithms selected',
                'max_count': rules['max_count'],
                'received_count': len(methods),
                'details': 'Using too many algorithms may significantly increase processing time'
            }
        
        # Validate individual algorithm names
        invalid_algorithms = [method for method in methods if method not in self.valid_algorithms]
        if invalid_algorithms:
            return {
                'valid': False,
                'error': 'Invalid algorithms selected',
                'invalid_algorithms': invalid_algorithms,
                'valid_algorithms': list(self.valid_algorithms),
                'suggestions': [self._get_algorithm_suggestions(alg) for alg in invalid_algorithms]
            }
        
        # Check for duplicate algorithms
        if len(methods) != len(set(methods)):
            duplicates = [method for method in set(methods) if methods.count(method) > 1]
            return {
                'valid': False,
                'error': 'Duplicate algorithms detected',
                'duplicate_algorithms': duplicates
            }
        
        return {'valid': True}
    
    def _validate_options(self, options_str: str) -> Dict[str, Any]:
        """Validate optional parameters JSON"""
        
        if not options_str or options_str.strip() == '':
            return {'valid': True}  # Options are optional
        
        try:
            import json
            options = json.loads(options_str)
            
            # Validate options structure if provided
            if not isinstance(options, dict):
                return {
                    'valid': False,
                    'error': 'Options must be a JSON object',
                    'received_type': type(options).__name__
                }
            
            # Validate specific option fields
            valid_options = {
                'include_explanations': bool,
                'include_skill_extraction': bool,
                'include_score_breakdown': bool,
                'combine_results': bool,
                'weighting_strategy': str,
                'use_cache': bool,
                'timeout': int
            }
            
            for key, value in options.items():
                if key in valid_options:
                    expected_type = valid_options[key]
                    if not isinstance(value, expected_type):
                        return {
                            'valid': False,
                            'error': f'Invalid type for option "{key}"',
                            'expected_type': expected_type.__name__,
                            'received_type': type(value).__name__
                        }
            
            # Validate specific option values
            if 'weighting_strategy' in options:
                valid_strategies = ['balanced', 'accuracy_focused', 'speed_focused']
                if options['weighting_strategy'] not in valid_strategies:
                    return {
                        'valid': False,
                        'error': 'Invalid weighting strategy',
                        'valid_strategies': valid_strategies,
                        'received_strategy': options['weighting_strategy']
                    }
            
            if 'timeout' in options:
                timeout = options['timeout']
                if not isinstance(timeout, int) or timeout < 1 or timeout > 600:
                    return {
                        'valid': False,
                        'error': 'Invalid timeout value',
                        'details': 'Timeout must be between 1 and 600 seconds',
                        'received_timeout': timeout
                    }
            
            return {'valid': True}
            
        except json.JSONDecodeError as e:
            return {
                'valid': False,
                'error': 'Invalid JSON in options',
                'details': str(e),
                'example': '{"include_explanations": true, "use_cache": true}'
            }
    
    def _validate_cross_field_constraints(self, files: List, methods: List[str], 
                                        job_description: str) -> Dict[str, Any]:
        """Validate constraints that depend on multiple fields"""
        
        # Algorithm complexity vs file count validation
        complex_algorithms = {'bert', 'distilbert', 'sbert', 'xlm', 'neural_network'}
        complex_count = len([m for m in methods if m in complex_algorithms])
        
        if len(files) > 20 and complex_count > 2:
            return {
                'valid': False,
                'error': 'High processing load detected',
                'details': 'Too many complex algorithms for large file batch',
                'recommendation': 'Use fewer complex algorithms or process files in smaller batches',
                'file_count': len(files),
                'complex_algorithms_count': complex_count
            }
        
        # Job description relevance to algorithms
        if 'ner' in methods and len(job_description.split()) < 10:
            return {
                'valid': False,
                'error': 'Insufficient job description for NER analysis',
                'details': 'Named Entity Recognition requires detailed job description',
                'recommendation': 'Provide more detailed job requirements or remove NER algorithm'
            }
        
        return {'valid': True}
    
    def _get_position_suggestions(self, invalid_position: str) -> List[str]:
        """Get suggestions for similar position names"""
        suggestions = []
        invalid_lower = invalid_position.lower()
        
        for valid_pos in self.valid_positions:
            if (invalid_lower in valid_pos or 
                valid_pos in invalid_lower or
                self._calculate_similarity(invalid_lower, valid_pos) > 0.6):
                suggestions.append(valid_pos)
        
        return suggestions[:3]
    
    def _get_algorithm_suggestions(self, invalid_algorithm: str) -> List[str]:
        """Get suggestions for similar algorithm names"""
        suggestions = []
        invalid_lower = invalid_algorithm.lower()
        
        for valid_alg in self.valid_algorithms:
            if (invalid_lower in valid_alg or 
                valid_alg in invalid_lower or
                self._calculate_similarity(invalid_lower, valid_alg) > 0.5):
                suggestions.append(valid_alg)
        
        return suggestions[:3]
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """Calculate simple string similarity (Jaccard similarity)"""
        set1 = set(str1.lower())
        set2 = set(str2.lower())
        
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def validate_export_request(self, request: Request) -> Dict[str, Any]:
        """Validate export/download requests"""
        
        format_param = request.args.get('format', 'json')
        valid_formats = ['json', 'csv', 'xlsx', 'pdf']
        
        if format_param not in valid_formats:
            return {
                'valid': False,
                'error': 'Invalid export format',
                'valid_formats': valid_formats,
                'received_format': format_param
            }
        
        return {'valid': True}
    
    def validate_cache_request(self, request: Request) -> Dict[str, Any]:
        """Validate cache management requests"""
        
        if request.method == 'POST' and request.json:
            pattern = request.json.get('pattern')
            if pattern and not isinstance(pattern, str):
                return {
                    'valid': False,
                    'error': 'Cache pattern must be a string'
                }
            
            if pattern and len(pattern) > 100:
                return {
                    'valid': False,
                    'error': 'Cache pattern too long (max 100 characters)'
                }
        
        return {'valid': True}

# Validation decorators
def validate_json_content(f):
    """Decorator to validate JSON content"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from flask import request, jsonify
        
        if request.content_type != 'application/json':
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400
        
        try:
            if not request.json:
                return jsonify({
                    'error': 'Request body must contain valid JSON'
                }), 400
        except Exception:
            return jsonify({
                'error': 'Invalid JSON in request body'
            }), 400
        
        return f(*args, **kwargs)
    
    return decorated_function

def validate_required_fields(required_fields: List[str]):
    """Decorator to validate required fields in request"""
    def decorator(f):
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from flask import request, jsonify
            
            missing_fields = []
            
            # Check in JSON body
            if request.json:
                for field in required_fields:
                    if field not in request.json or request.json[field] is None:
                        missing_fields.append(field)
            
            # Check in form data
            elif request.form:
                for field in required_fields:
                    if field not in request.form or not request.form.get(field):
                        missing_fields.append(field)
            
            if missing_fields:
                return jsonify({
                    'error': 'Missing required fields',
                    'missing_fields': missing_fields,
                    'required_fields': required_fields
                }), 400
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
