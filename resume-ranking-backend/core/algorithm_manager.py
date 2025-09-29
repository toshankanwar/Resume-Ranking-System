from typing import List, Dict, Any, Optional
import asyncio
import concurrent.futures
from algorithms.deep_learning.bert_analyzer import BERTAnalyzer
from algorithms.traditional_ml.xgboost_classifier import XGBoostClassifier
from algorithms.similarity.cosine_similarity import CosineSimilarityAnalyzer
from algorithms.similarity.ner_analyzer import NERAnalyzer
import logging

logger = logging.getLogger(__name__)

class AlgorithmManager:
    """Manages and orchestrates multiple ranking algorithms"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.algorithms = {}
        self.algorithm_registry = {
            'bert': BERTAnalyzer,
            'distilbert': BERTAnalyzer,  # Can be extended with separate class
            'sbert': BERTAnalyzer,       # Can be extended with separate class
            'xgboost': XGBoostClassifier,
            'random_forest': XGBoostClassifier,  # Can be extended
            'svm': XGBoostClassifier,           # Can be extended
            'neural_network': XGBoostClassifier, # Can be extended
            'cosine': CosineSimilarityAnalyzer,
            'jaccard': CosineSimilarityAnalyzer, # Can be extended
            'ner': NERAnalyzer
        }
        self.max_workers = self.config.get('max_workers', 4)
    
    def initialize_algorithms(self, algorithm_names: List[str]) -> None:
        """Initialize specified algorithms"""
        for name in algorithm_names:
            if name in self.algorithm_registry and name not in self.algorithms:
                try:
                    logger.info(f"Initializing algorithm: {name}")
                    algorithm_class = self.algorithm_registry[name]
                    algorithm_config = self.config.get(name, {})
                    
                    # Special configuration for different variants
                    if name == 'distilbert':
                        algorithm_config['model_name'] = 'distilbert-base-uncased'
                    elif name == 'sbert':
                        algorithm_config['model_name'] = 'sentence-transformers/all-MiniLM-L6-v2'
                    
                    self.algorithms[name] = algorithm_class(algorithm_config)
                    self.algorithms[name].load_model()
                    
                    logger.info(f"Algorithm {name} initialized successfully")
                    
                except Exception as e:
                    logger.error(f"Failed to initialize algorithm {name}: {e}")
                    # Continue with other algorithms
                    continue
    
    def process_resumes_parallel(self, resume_texts: List[str], 
                                job_description: str, algorithm_names: List[str],
                                position: str = None) -> Dict[str, Any]:
        """Process resumes using multiple algorithms in parallel"""
        
        # Initialize required algorithms
        self.initialize_algorithms(algorithm_names)
        
        # Filter to only available algorithms
        available_algorithms = [name for name in algorithm_names if name in self.algorithms]
        
        if not available_algorithms:
            raise Exception("No algorithms available for processing")
        
        logger.info(f"Processing {len(resume_texts)} resumes with {len(available_algorithms)} algorithms")
        
        results = {
            'metadata': {
                'total_resumes': len(resume_texts),
                'algorithms_used': available_algorithms,
                'job_position': position,
                'processing_timestamp': None
            },
            'individual_scores': {},
            'combined_results': [],
            'algorithm_performance': {}
        }
        
        # Process with each algorithm
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_algorithm = {}
            
            for alg_name in available_algorithms:
                future = executor.submit(
                    self.algorithms[alg_name].process_batch,
                    resume_texts, job_description, position
                )
                future_to_algorithm[future] = alg_name
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_algorithm):
                alg_name = future_to_algorithm[future]
                try:
                    alg_results = future.result()
                    results['individual_scores'][alg_name] = alg_results
                    results['algorithm_performance'][alg_name] = self.algorithms[alg_name].get_performance_metrics()
                    logger.info(f"Completed processing with {alg_name}")
                    
                except Exception as e:
                    logger.error(f"Algorithm {alg_name} failed: {e}")
                    results['individual_scores'][alg_name] = []
                    results['algorithm_performance'][alg_name] = {'error': str(e)}
        
        # Combine results
        results['combined_results'] = self._combine_algorithm_results(
            results['individual_scores'], len(resume_texts)
        )
        
        return results
    
    def _combine_algorithm_results(self, individual_scores: Dict[str, List], 
                                  total_resumes: int) -> List[Dict[str, Any]]:
        """Combine scores from multiple algorithms"""
        combined_results = []
        
        for resume_idx in range(total_resumes):
            resume_result = {
                'resume_index': resume_idx,
                'algorithm_scores': {},
                'combined_score': 0.0,
                'weighted_score': 0.0,
                'rank': 0,
                'details': {},
                'errors': []
            }
            
            total_weight = 0
            score_sum = 0
            
            # Algorithm weights (can be configured)
            weights = {
                'bert': 0.3,
                'distilbert': 0.25,
                'sbert': 0.25,
                'xgboost': 0.2,
                'random_forest': 0.15,
                'svm': 0.15,
                'neural_network': 0.15,
                'cosine': 0.2,
                'jaccard': 0.15,
                'ner': 0.25
            }
            
            for alg_name, alg_results in individual_scores.items():
                if resume_idx < len(alg_results):
                    result = alg_results[resume_idx]
                    
                    if 'error' not in result:
                        score = result.get('score', 0.0)
                        weight = weights.get(alg_name, 0.1)
                        
                        resume_result['algorithm_scores'][alg_name] = {
                            'score': score,
                            'weight': weight,
                            'details': result.get('details', {})
                        }
                        
                        score_sum += score * weight
                        total_weight += weight
                    else:
                        resume_result['errors'].append({
                            'algorithm': alg_name,
                            'error': result['error']
                        })
            
            # Calculate final scores
            if total_weight > 0:
                resume_result['weighted_score'] = score_sum / total_weight
                resume_result['combined_score'] = score_sum / total_weight
            
            combined_results.append(resume_result)
        
        # Sort by combined score and assign ranks
        combined_results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        for idx, result in enumerate(combined_results):
            result['rank'] = idx + 1
        
        return combined_results
    
    def get_algorithm_status(self) -> Dict[str, Any]:
        """Get status of all algorithms"""
        status = {
            'available_algorithms': list(self.algorithm_registry.keys()),
            'loaded_algorithms': list(self.algorithms.keys()),
            'algorithm_details': {}
        }
        
        for name, algorithm in self.algorithms.items():
            status['algorithm_details'][name] = algorithm.get_performance_metrics()
        
        return status
    
    def cleanup(self) -> None:
        """Clean up all algorithm resources"""
        for algorithm in self.algorithms.values():
            try:
                algorithm.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up algorithm: {e}")
        
        self.algorithms.clear()
        logger.info("Algorithm manager cleaned up")
