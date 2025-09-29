from typing import Dict, List, Any, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)

class ScoreCombiner:
    """Combines scores from multiple algorithms using various strategies"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.default_weights = self._get_default_weights()
        self.combination_strategies = {
            'weighted_average': self._weighted_average,
            'harmonic_mean': self._harmonic_mean,
            'geometric_mean': self._geometric_mean,
            'max_score': self._max_score,
            'min_score': self._min_score,
            'median_score': self._median_score,
            'ensemble_voting': self._ensemble_voting
        }
    
    def _get_default_weights(self) -> Dict[str, float]:
        """Get default algorithm weights based on research performance"""
        return {
            # Deep Learning - Higher weights due to semantic understanding
            'bert': 0.25,
            'distilbert': 0.20,
            'sbert': 0.22,
            'xlm': 0.18,
            
            # Traditional ML - Moderate weights  
            'xgboost': 0.20,
            'random_forest': 0.18,
            'svm': 0.16,
            'neural_network': 0.15,
            
            # Similarity Methods - Lower weights, more specialized
            'cosine': 0.15,
            'jaccard': 0.12,
            'ner': 0.20  # Higher weight for skill extraction
        }
    
    def combine_scores(self, 
                      algorithm_results: Dict[str, Dict[str, Any]],
                      strategy: str = 'weighted_average',
                      custom_weights: Dict[str, float] = None) -> Dict[str, Any]:
        """
        Combine scores from multiple algorithms
        
        Args:
            algorithm_results: Dict of {algorithm_name: result_dict}
            strategy: Combination strategy to use
            custom_weights: Custom weights for algorithms
            
        Returns:
            Combined result with final score and details
        """
        
        if not algorithm_results:
            return {
                'combined_score': 0.0,
                'strategy': strategy,
                'error': 'No algorithm results provided'
            }
        
        try:
            # Extract scores from results
            scores = {}
            details = {}
            
            for alg_name, result in algorithm_results.items():
                if 'error' not in result and 'score' in result:
                    scores[alg_name] = result['score']
                    details[alg_name] = result.get('details', {})
                else:
                    logger.warning(f"Algorithm {alg_name} failed or missing score")
            
            if not scores:
                return {
                    'combined_score': 0.0,
                    'strategy': strategy,
                    'error': 'No valid scores from algorithms'
                }
            
            # Use combination strategy
            if strategy not in self.combination_strategies:
                logger.warning(f"Unknown strategy {strategy}, using weighted_average")
                strategy = 'weighted_average'
            
            combiner_func = self.combination_strategies[strategy]
            
            # Apply weights if needed
            weights = custom_weights or self.default_weights
            
            combined_result = combiner_func(scores, weights, details)
            combined_result['strategy'] = strategy
            combined_result['algorithms_used'] = list(scores.keys())
            combined_result['algorithm_count'] = len(scores)
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Score combination failed: {e}")
            return {
                'combined_score': 0.0,
                'strategy': strategy,
                'error': f'Combination failed: {str(e)}'
            }
    
    def _weighted_average(self, scores: Dict[str, float], 
                         weights: Dict[str, float],
                         details: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate weighted average score"""
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for alg_name, score in scores.items():
            weight = weights.get(alg_name, 0.1)  # Default weight
            total_weighted_score += score * weight
            total_weight += weight
        
        combined_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
        
        return {
            'combined_score': float(combined_score),
            'method': 'weighted_average',
            'total_weight': total_weight,
            'individual_scores': scores,
            'weights_used': {alg: weights.get(alg, 0.1) for alg in scores.keys()}
        }
    
    def _harmonic_mean(self, scores: Dict[str, float],
                      weights: Dict[str, float], 
                      details: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate harmonic mean (good for penalizing low scores)"""
        
        # Avoid division by zero
        valid_scores = [max(score, 0.001) for score in scores.values()]
        
        if not valid_scores:
            return {'combined_score': 0.0, 'method': 'harmonic_mean'}
        
        harmonic_mean = len(valid_scores) / sum(1/score for score in valid_scores)
        
        return {
            'combined_score': float(harmonic_mean),
            'method': 'harmonic_mean',
            'individual_scores': scores
        }
    
    def _geometric_mean(self, scores: Dict[str, float],
                       weights: Dict[str, float],
                       details: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate geometric mean"""
        
        if not scores:
            return {'combined_score': 0.0, 'method': 'geometric_mean'}
        
        # Ensure all scores are positive
        positive_scores = [max(score, 0.001) for score in scores.values()]
        
        geometric_mean = np.prod(positive_scores) ** (1.0 / len(positive_scores))
        
        return {
            'combined_score': float(geometric_mean),
            'method': 'geometric_mean',
            'individual_scores': scores
        }
    
    def _max_score(self, scores: Dict[str, float],
                   weights: Dict[str, float],
                   details: Dict[str, Dict]) -> Dict[str, Any]:
        """Take maximum score (optimistic approach)"""
        
        if not scores:
            return {'combined_score': 0.0, 'method': 'max_score'}
        
        max_score = max(scores.values())
        best_algorithm = max(scores, key=scores.get)
        
        return {
            'combined_score': float(max_score),
            'method': 'max_score',
            'best_algorithm': best_algorithm,
            'individual_scores': scores
        }
    
    def _min_score(self, scores: Dict[str, float],
                   weights: Dict[str, float],
                   details: Dict[str, Dict]) -> Dict[str, Any]:
        """Take minimum score (conservative approach)"""
        
        if not scores:
            return {'combined_score': 0.0, 'method': 'min_score'}
        
        min_score = min(scores.values())
        worst_algorithm = min(scores, key=scores.get)
        
        return {
            'combined_score': float(min_score),
            'method': 'min_score', 
            'worst_algorithm': worst_algorithm,
            'individual_scores': scores
        }
    
    def _median_score(self, scores: Dict[str, float],
                     weights: Dict[str, float],
                     details: Dict[str, Dict]) -> Dict[str, Any]:
        """Take median score (robust approach)"""
        
        if not scores:
            return {'combined_score': 0.0, 'method': 'median_score'}
        
        score_values = list(scores.values())
        median_score = np.median(score_values)
        
        return {
            'combined_score': float(median_score),
            'method': 'median_score',
            'score_distribution': {
                'min': float(np.min(score_values)),
                'max': float(np.max(score_values)),
                'std': float(np.std(score_values))
            },
            'individual_scores': scores
        }
    
    def _ensemble_voting(self, scores: Dict[str, float],
                        weights: Dict[str, float],
                        details: Dict[str, Dict]) -> Dict[str, Any]:
        """Ensemble voting based on score thresholds"""
        
        if not scores:
            return {'combined_score': 0.0, 'method': 'ensemble_voting'}
        
        # Define voting thresholds
        thresholds = {
            'excellent': 0.8,
            'good': 0.6,
            'fair': 0.4,
            'poor': 0.0
        }
        
        votes = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        
        for alg_name, score in scores.items():
            weight = weights.get(alg_name, 1.0)
            
            if score >= thresholds['excellent']:
                votes['excellent'] += weight
            elif score >= thresholds['good']:
                votes['good'] += weight  
            elif score >= thresholds['fair']:
                votes['fair'] += weight
            else:
                votes['poor'] += weight
        
        # Calculate final score based on votes
        total_votes = sum(votes.values())
        if total_votes == 0:
            combined_score = 0.0
        else:
            combined_score = (
                votes['excellent'] * 0.9 +
                votes['good'] * 0.7 +
                votes['fair'] * 0.5 + 
                votes['poor'] * 0.2
            ) / total_votes
        
        return {
            'combined_score': float(combined_score),
            'method': 'ensemble_voting',
            'votes': votes,
            'total_votes': total_votes,
            'individual_scores': scores
        }
    
    def analyze_score_agreement(self, scores: Dict[str, float]) -> Dict[str, Any]:
        """Analyze agreement between different algorithms"""
        
        if len(scores) < 2:
            return {'agreement': 'insufficient_data'}
        
        score_values = list(scores.values())
        mean_score = np.mean(score_values)
        std_score = np.std(score_values)
        min_score = np.min(score_values)
        max_score = np.max(score_values)
        
        # Calculate coefficient of variation
        cv = std_score / mean_score if mean_score > 0 else float('inf')
        
        # Determine agreement level
        if cv < 0.1:
            agreement = 'high'
        elif cv < 0.25:
            agreement = 'moderate'
        elif cv < 0.5:
            agreement = 'low'
        else:
            agreement = 'very_low'
        
        return {
            'agreement': agreement,
            'coefficient_of_variation': float(cv),
            'mean_score': float(mean_score),
            'std_deviation': float(std_score),
            'score_range': float(max_score - min_score),
            'min_score': float(min_score),
            'max_score': float(max_score)
        }
