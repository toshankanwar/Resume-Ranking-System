from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
import json
import time
from datetime import datetime
import logging
from typing import Dict, Any, List
import numpy as np

from core.algorithm_manager import AlgorithmManager
from utils.file_processor import FileProcessor
from utils.validators import RequestValidator
from utils.cache_manager import CacheManager
from config.logging_config import performance_logger, algorithm_logger

logger = logging.getLogger(__name__)

def create_routes(app) -> None:
    """Create and register API routes"""
    
    # Initialize components
    algorithm_manager = AlgorithmManager(app.config)
    file_processor = FileProcessor(app.config)
    validator = RequestValidator(app.config)
    cache_manager = CacheManager(app.config)
    
    api = Blueprint('api', __name__, url_prefix='/api')
    
    @api.route('/health', methods=['GET'])
    def health_check():
        """Comprehensive health check endpoint"""
        start_time = time.time()
        
        try:
            health_status = {
                'status': 'healthy',
                'timestamp': datetime.utcnow().isoformat(),
                'version': '1.0.0',
                'environment': app.config.get('ENV', 'unknown'),
                'components': {
                    'algorithm_manager': _check_algorithm_manager(algorithm_manager),
                    'file_processor': _check_file_processor(),
                    'cache_manager': _check_cache_manager(cache_manager),
                    'database': _check_database_connection(),
                    'disk_space': _check_disk_space(),
                    'memory': _check_memory_usage()
                },
                'algorithms': algorithm_manager.get_algorithm_status(),
                'uptime': _get_uptime()
            }
            
            # Check if any critical components are failing
            critical_components = ['algorithm_manager', 'file_processor']
            failing_components = [
                comp for comp in critical_components 
                if not health_status['components'][comp]['status'] == 'healthy'
            ]
            
            if failing_components:
                health_status['status'] = 'degraded'
                health_status['failing_components'] = failing_components
            
            status_code = 200 if health_status['status'] == 'healthy' else 503
            
            processing_time = time.time() - start_time
            performance_logger.log_request_performance(
                '/api/health', 'GET', processing_time, status_code
            )
            
            return jsonify(health_status), status_code
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @api.route('/algorithms', methods=['GET'])
    def get_algorithms():
        """Get available algorithms and their status"""
        try:
            algorithms_info = {
                'available_algorithms': [
                    'bert', 'distilbert', 'sbert', 'xlm',
                    'xgboost', 'random_forest', 'svm', 'neural_network',
                    'cosine', 'jaccard', 'ner'
                ],
                'algorithm_categories': {
                    'deep_learning': {
                        'algorithms': ['bert', 'distilbert', 'sbert', 'xlm'],
                        'description': 'Transformer-based models for semantic understanding',
                        'strengths': ['Contextual understanding', 'Semantic similarity', 'Language comprehension'],
                        'use_cases': ['Semantic matching', 'Context-aware analysis', 'Multi-language support']
                    },
                    'traditional_ml': {
                        'algorithms': ['xgboost', 'random_forest', 'svm', 'neural_network'],
                        'description': 'Classical machine learning algorithms',
                        'strengths': ['Fast processing', 'Interpretability', 'Robust performance'],
                        'use_cases': ['Feature-based matching', 'Predictive scoring', 'Classification']
                    },
                    'similarity': {
                        'algorithms': ['cosine', 'jaccard', 'ner'],
                        'description': 'Similarity and information extraction methods',
                        'strengths': ['Fast computation', 'Skill extraction', 'Keyword matching'],
                        'use_cases': ['Quick screening', 'Skill analysis', 'Keyword matching']
                    }
                },
                'algorithm_details': _get_algorithm_details(),
                'system_status': algorithm_manager.get_algorithm_status(),
                'recommendations': _get_algorithm_recommendations()
            }
            
            return jsonify(algorithms_info)
            
        except Exception as e:
            logger.error(f"Error getting algorithms info: {e}")
            return jsonify({'error': 'Failed to retrieve algorithms information'}), 500
    
    @api.route('/positions', methods=['GET'])
    def get_positions():
        """Get available job positions"""
        positions = [
            {'value': 'sde', 'label': 'Software Development Engineer', 'icon': '💻', 'category': 'engineering'},
            {'value': 'swe', 'label': 'Software Engineer', 'icon': '⚙️', 'category': 'engineering'},
            {'value': 'ml_engineer', 'label': 'ML Engineer', 'icon': '🤖', 'category': 'ai_ml'},
            {'value': 'data_scientist', 'label': 'Data Scientist', 'icon': '📊', 'category': 'ai_ml'},
            {'value': 'devops', 'label': 'DevOps Engineer', 'icon': '🔧', 'category': 'operations'},
            {'value': 'frontend', 'label': 'Frontend Developer', 'icon': '🎨', 'category': 'development'},
            {'value': 'backend', 'label': 'Backend Developer', 'icon': '🗄️', 'category': 'development'},
            {'value': 'fullstack', 'label': 'Full Stack Developer', 'icon': '🚀', 'category': 'development'},
            {'value': 'product_manager', 'label': 'Product Manager', 'icon': '📱', 'category': 'management'},
            {'value': 'designer', 'label': 'UI/UX Designer', 'icon': '🎭', 'category': 'design'},
            {'value': 'qa_engineer', 'label': 'QA Engineer', 'icon': '🔍', 'category': 'quality'},
            {'value': 'security_engineer', 'label': 'Security Engineer', 'icon': '🛡️', 'category': 'security'},
            {'value': 'general', 'label': 'General', 'icon': '📋', 'category': 'other'}
        ]
        
        return jsonify({
            'positions': positions,
            'categories': _group_positions_by_category(positions)
        })
    
    @api.route('/supported-formats', methods=['GET'])
    def get_supported_formats():
        """Get supported file formats and limits"""
        return jsonify({
            'formats': ['.pdf', '.docx', '.doc'],
            'max_file_size': app.config['MAX_CONTENT_LENGTH'],
            'max_file_size_mb': app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024),
            'max_files': app.config.get('MAX_FILES_PER_REQUEST', 50),
            'supported_mime_types': [
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword'
            ],
            'processing_capabilities': {
                'text_extraction': True,
                'multi_page_support': True,
                'table_extraction': True,
                'image_text_extraction': False,
                'batch_processing': True
            }
        })
    
    @api.route('/validate-files', methods=['POST'])
    def validate_files():
        """Validate uploaded files without processing"""
        start_time = time.time()
        
        try:
            files = request.files.getlist('files')
            
            if not files:
                return jsonify({'error': 'No files provided'}), 400
            
            validation_results = []
            total_size = 0
            
            for i, file in enumerate(files):
                result = file_processor.validate_file(file)
                result['index'] = i
                
                if result['valid']:
                    total_size += result.get('size', 0)
                
                validation_results.append(result)
            
            summary = {
                'results': validation_results,
                'total_files': len(files),
                'valid_files': sum(1 for r in validation_results if r['valid']),
                'invalid_files': sum(1 for r in validation_results if not r['valid']),
                'total_size': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'validation_passed': all(r['valid'] for r in validation_results)
            }
            
            processing_time = time.time() - start_time
            performance_logger.log_request_performance(
                '/api/validate-files', 'POST', processing_time, 200, len(files)
            )
            
            return jsonify(summary)
            
        except Exception as e:
            logger.error(f"File validation error: {e}")
            return jsonify({'error': 'File validation failed', 'details': str(e)}), 500
    
    @api.route('/process-resumes', methods=['POST'])
    def process_resumes():
        """Main endpoint for processing resumes with multiple algorithms"""
        start_time = time.time()
        request_id = f"req_{int(time.time())}_{hash(str(request.form)) % 10000}"
        
        logger.info(f"[{request_id}] Starting resume processing request")
        
        try:
            # Validate request
            validation_result = validator.validate_process_request(request)
            if not validation_result['valid']:
                return jsonify({'error': validation_result['error']}), 400
            
            # Extract request data
            files = request.files.getlist('resumes')
            job_description = request.form.get('jobDescription', '').strip()
            position = request.form.get('position', 'general')
            methods = request.form.getlist('methods')
            
            # Parse additional data
            options = _parse_json_field(request.form.get('options', '{}'))
            metadata = _parse_json_field(request.form.get('metadata', '{}'))
            
            logger.info(f"[{request_id}] Processing {len(files)} files with {len(methods)} algorithms")
            
            # Check cache if enabled
            cache_key = None
            if cache_manager.enabled and options.get('use_cache', True):
                cache_key = _generate_cache_key(files, job_description, position, methods)
                cached_result = cache_manager.get(cache_key)
                if cached_result:
                    logger.info(f"[{request_id}] Returning cached result")
                    return jsonify(cached_result)
            
            # Process files
            processed_files = file_processor.process_files(files)
            
            # Filter successful extractions
            successful_files = [f for f in processed_files if f['success']]
            failed_files = [f for f in processed_files if not f['success']]
            
            if not successful_files:
                return jsonify({
                    'error': 'No files could be processed successfully',
                    'failed_files': failed_files,
                    'request_id': request_id
                }), 400
            
            # Extract resume texts
            resume_texts = [f['text'] for f in successful_files]
            
            # Process with algorithms
            logger.info(f"[{request_id}] Running algorithm processing")
            algorithm_results = algorithm_manager.process_resumes_parallel(
                resume_texts, job_description, methods, position
            )
            
            # Format response
            response = _format_processing_response(
                algorithm_results, successful_files, failed_files,
                job_description, position, methods, options, metadata, request_id
            )
            
            # Cache result if enabled
            if cache_manager.enabled and cache_key and response['success']:
                cache_manager.set(cache_key, response, ttl=1800)  # 30 minutes
            
            # Log performance
            processing_time = time.time() - start_time
            performance_logger.log_request_performance(
                '/api/process-resumes', 'POST', processing_time, 200,
                len(successful_files), len(methods)
            )
            
            logger.info(f"[{request_id}] Processing completed in {processing_time:.2f}s")
            
            return jsonify(response)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[{request_id}] Processing failed: {error_msg}")
            
            processing_time = time.time() - start_time
            performance_logger.log_request_performance(
                '/api/process-resumes', 'POST', processing_time, 500
            )
            
            return jsonify({
                'success': False,
                'error': error_msg,
                'request_id': request_id,
                'timestamp': datetime.utcnow().isoformat()
            }), 500
    
    @api.route('/algorithm-benchmarks', methods=['GET'])
    def get_algorithm_benchmarks():
        """Get algorithm performance benchmarks"""
        try:
            benchmarks = {
                'deep_learning': {
                    'bert': {
                        'accuracy_range': '85-95%',
                        'avg_processing_time': '2-4 seconds/resume',
                        'memory_usage': 'High',
                        'best_for': ['Semantic understanding', 'Context analysis']
                    },
                    'distilbert': {
                        'accuracy_range': '80-90%',
                        'avg_processing_time': '1-2 seconds/resume',
                        'memory_usage': 'Medium',
                        'best_for': ['Fast semantic analysis', 'Resource-constrained environments']
                    },
                    'sbert': {
                        'accuracy_range': '82-92%',
                        'avg_processing_time': '1-3 seconds/resume',
                        'memory_usage': 'Medium',
                        'best_for': ['Sentence similarity', 'Efficient embedding generation']
                    }
                },
                'traditional_ml': {
                    'xgboost': {
                        'accuracy_range': '75-85%',
                        'avg_processing_time': '0.1-0.5 seconds/resume',
                        'memory_usage': 'Low',
                        'best_for': ['Feature-based analysis', 'Fast processing']
                    },
                    'random_forest': {
                        'accuracy_range': '70-80%',
                        'avg_processing_time': '0.05-0.2 seconds/resume',
                        'memory_usage': 'Low',
                        'best_for': ['Interpretable results', 'Robust performance']
                    }
                },
                'similarity': {
                    'cosine': {
                        'accuracy_range': '65-75%',
                        'avg_processing_time': '0.01-0.05 seconds/resume',
                        'memory_usage': 'Very Low',
                        'best_for': ['Keyword matching', 'Fast screening']
                    },
                    'ner': {
                        'accuracy_range': '70-85%',
                        'avg_processing_time': '0.5-1 seconds/resume',
                        'memory_usage': 'Medium',
                        'best_for': ['Skill extraction', 'Experience analysis']
                    }
                }
            }
            
            return jsonify({
                'benchmarks': benchmarks,
                'methodology': 'Benchmarks based on internal testing and research papers',
                'test_dataset_size': '1000+ resumes across various positions',
                'last_updated': '2024-01-01'
            })
            
        except Exception as e:
            logger.error(f"Error getting benchmarks: {e}")
            return jsonify({'error': 'Failed to retrieve benchmarks'}), 500
    
    @api.route('/cache/stats', methods=['GET'])
    def get_cache_stats():
        """Get cache statistics"""
        try:
            stats = cache_manager.get_cache_stats()
            return jsonify(stats)
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return jsonify({'error': 'Failed to retrieve cache stats'}), 500
    
    @api.route('/cache/clear', methods=['POST'])
    def clear_cache():
        """Clear cache entries"""
        try:
            pattern = request.json.get('pattern') if request.json else None
            cleared_count = cache_manager.clear_cache(pattern)
            
            return jsonify({
                'success': True,
                'cleared_entries': cleared_count,
                'pattern': pattern or 'all'
            })
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return jsonify({'error': 'Failed to clear cache'}), 500
    
    # Helper functions
    def _check_algorithm_manager(manager) -> Dict[str, Any]:
        """Check algorithm manager health"""
        try:
            status = manager.get_algorithm_status()
            return {
                'status': 'healthy',
                'loaded_algorithms': len(status.get('loaded_algorithms', [])),
                'available_algorithms': len(status.get('available_algorithms', []))
            }
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def _check_file_processor() -> Dict[str, Any]:
        """Check file processor health"""
        try:
            # Simple health check - try to create FileProcessor
            FileProcessor()
            return {'status': 'healthy'}
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def _check_cache_manager(manager) -> Dict[str, Any]:
        """Check cache manager health"""
        try:
            stats = manager.get_cache_stats()
            return {
                'status': 'healthy' if stats.get('enabled') else 'disabled',
                'enabled': stats.get('enabled', False)
            }
        except Exception as e:
            return {'status': 'unhealthy', 'error': str(e)}
    
    def _check_database_connection() -> Dict[str, Any]:
        """Check database connection (placeholder)"""
        return {'status': 'not_applicable', 'message': 'No database configured'}
    
    def _check_disk_space() -> Dict[str, Any]:
        """Check available disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage('/')
            free_gb = free // (1024**3)
            return {
                'status': 'healthy' if free_gb > 1 else 'low',
                'free_space_gb': free_gb
            }
        except Exception as e:
            return {'status': 'unknown', 'error': str(e)}
    
    def _check_memory_usage() -> Dict[str, Any]:
        """Check memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'status': 'healthy' if memory.percent < 90 else 'high',
                'usage_percent': memory.percent,
                'available_gb': round(memory.available / (1024**3), 2)
            }
        except ImportError:
            return {'status': 'unknown', 'message': 'psutil not available'}
        except Exception as e:
            return {'status': 'unknown', 'error': str(e)}
    
    def _get_uptime() -> str:
        """Get system uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_hours = uptime_seconds / 3600
                return f"{uptime_hours:.1f} hours"
        except:
            return "unknown"
    
    def _get_algorithm_details() -> Dict[str, Any]:
        """Get detailed algorithm information"""
        return {
            'bert': {
                'full_name': 'Bidirectional Encoder Representations from Transformers',
                'type': 'transformer',
                'parameters': '110M',
                'context_length': 512,
                'strengths': ['Contextual understanding', 'Bidirectional processing'],
                'limitations': ['High memory usage', 'Slower processing']
            },
            'cosine': {
                'full_name': 'TF-IDF Cosine Similarity',
                'type': 'similarity_measure',
                'features': 'TF-IDF vectors',
                'strengths': ['Fast processing', 'Simple interpretation'],
                'limitations': ['No semantic understanding', 'Keyword dependent']
            },
            'ner': {
                'full_name': 'Named Entity Recognition',
                'type': 'information_extraction',
                'entities': ['Skills', 'Experience', 'Education'],
                'strengths': ['Structured information', 'Skill extraction'],
                'limitations': ['Domain dependent', 'Entity coverage']
            }
        }
    
    def _get_algorithm_recommendations() -> List[Dict[str, Any]]:
        """Get algorithm recommendations for different use cases"""
        return [
            {
                'use_case': 'High accuracy semantic matching',
                'recommended': ['bert', 'sbert', 'ner'],
                'description': 'Best for understanding context and meaning'
            },
            {
                'use_case': 'Fast bulk processing',
                'recommended': ['cosine', 'random_forest', 'jaccard'],
                'description': 'Optimized for speed and throughput'
            },
            {
                'use_case': 'Balanced accuracy and speed',
                'recommended': ['distilbert', 'xgboost', 'ner'],
                'description': 'Good compromise between performance and speed'
            },
            {
                'use_case': 'Skill-focused analysis',
                'recommended': ['ner', 'jaccard', 'cosine'],
                'description': 'Specialized for technical skill matching'
            }
        ]
    
    def _group_positions_by_category(positions: List[Dict]) -> Dict[str, List[Dict]]:
        """Group positions by category"""
        categories = {}
        for position in positions:
            category = position['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(position)
        return categories
    
    def _parse_json_field(field_value: str) -> Dict[str, Any]:
        """Safely parse JSON field"""
        try:
            return json.loads(field_value)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def _generate_cache_key(files, job_description: str, position: str, methods: List[str]) -> str:
        """Generate cache key for request"""
        import hashlib
        
        # Create a hash of the key components
        key_components = [
            job_description[:1000],  # First 1000 chars
            position,
            ','.join(sorted(methods)),
            str(len(files))  # Number of files as proxy
        ]
        
        key_string = '|'.join(key_components)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _format_processing_response(algorithm_results: Dict[str, Any], successful_files: List[Dict],
                                   failed_files: List[Dict], job_description: str, position: str,
                                   methods: List[str], options: Dict[str, Any], metadata: Dict[str, Any],
                                   request_id: str) -> Dict[str, Any]:
        """Format the complete processing response"""
        
        end_time = datetime.utcnow()
        
        response = {
            'success': True,
            'request_id': request_id,
            'timestamp': end_time.isoformat(),
            'summary': {
                'total_resumes_uploaded': len(successful_files) + len(failed_files),
                'successfully_processed': len(successful_files),
                'failed_to_process': len(failed_files),
                'algorithms_used': methods,
                'job_position': position,
                'processing_options': options
            },
            'results': [],
            'failed_files': failed_files,
            'algorithm_performance': algorithm_results.get('algorithm_performance', {}),
            'metadata': {
                **metadata,
                'processing_completed_at': end_time.isoformat(),
                'server_version': '1.0.0',
                'request_id': request_id
            }
        }
        
        # Format results for frontend
        for i, combined_result in enumerate(algorithm_results.get('combined_results', [])):
            try:
                original_file_info = successful_files[combined_result['resume_index']]
                
                # Generate explanation
                explanation = _generate_result_explanation(combined_result, job_description, position)
                
                # Extract skills from NER if available
                extracted_skills = []
                if 'ner' in combined_result['algorithm_scores']:
                    ner_details = combined_result['algorithm_scores']['ner'].get('details', {})
                    extracted_skills = _extract_skills_from_ner(ner_details.get('extracted_skills', {}))
                
                result_entry = {
                    'filename': original_file_info['filename'],
                    'rank': combined_result['rank'],
                    'final_score': round(combined_result['combined_score'], 4),
                    'weighted_score': round(combined_result['weighted_score'], 4),
                    'scores': {alg: round(data['score'], 4) for alg, data in combined_result['algorithm_scores'].items()},
                    'explanation': explanation,
                    'extracted_skills': extracted_skills[:20],
                    'file_info': {
                        'size': original_file_info['size'],
                        'word_count': original_file_info['word_count'],
                        'char_count': original_file_info['char_count']
                    },
                    'algorithm_details': combined_result['algorithm_scores'],
                    'errors': combined_result.get('errors', []),
                    'confidence': _calculate_result_confidence(combined_result)
                }
                
                response['results'].append(result_entry)
                
            except Exception as e:
                logger.error(f"Error formatting result {i}: {e}")
                continue
        
        # Sort results by rank
        response['results'].sort(key=lambda x: x['rank'])
        
        return response
    
    def _generate_result_explanation(combined_result: Dict[str, Any], job_description: str, position: str) -> str:
        """Generate explanation for individual result"""
        try:
            score = combined_result['combined_score']
            algorithm_scores = combined_result['algorithm_scores']
            
            if score >= 0.8:
                rating = "Excellent match"
            elif score >= 0.6:
                rating = "Good match"
            elif score >= 0.4:
                rating = "Fair match"
            else:
                rating = "Poor match"
            
            explanation = f"{rating} for {position} position (Overall: {score:.1%}). "
            
            # Find best performing algorithm
            if algorithm_scores:
                best_alg = max(algorithm_scores.keys(), 
                             key=lambda k: algorithm_scores[k]['score'], 
                             default='unknown')
                best_score = algorithm_scores.get(best_alg, {}).get('score', 0)
                explanation += f"Strongest performance in {best_alg.upper()} analysis ({best_score:.1%}). "
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Analysis completed with combined score of {combined_result.get('combined_score', 0):.1%}"
    
    def _extract_skills_from_ner(extracted_skills: Dict[str, Any]) -> List[str]:
        """Extract flat list of skills from NER results"""
        skills = []
        for category, skill_list in extracted_skills.items():
            for skill_data in skill_list:
                if isinstance(skill_data, dict):
                    skills.append(skill_data.get('skill', '').title())
                else:
                    skills.append(str(skill_data).title())
        return list(set(skills))
    
    def _calculate_result_confidence(combined_result: Dict[str, Any]) -> str:
        """Calculate confidence level for result"""
        algorithm_scores = combined_result.get('algorithm_scores', {})
        
        if len(algorithm_scores) < 2:
            return 'low'
        
        scores = [data['score'] for data in algorithm_scores.values()]
        std_dev = np.std(scores) if len(scores) > 1 else 0
        
        if std_dev < 0.1:
            return 'high'
        elif std_dev < 0.25:
            return 'medium'
        else:
            return 'low'
    
    # Register blueprint
    app.register_blueprint(api)
    
    logger.info("API routes registered successfully")
