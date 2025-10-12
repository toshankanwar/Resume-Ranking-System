import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import cross_val_score, KFold
from scipy.stats import pearsonr, spearmanr
from typing import Dict, List, Any, Tuple
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import time

logger = logging.getLogger(__name__)

class AccuracyEvaluator:
    """Comprehensive accuracy evaluation for resume ranking algorithms"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.results_dir = self.config.get('results_dir', 'evaluation_results')
        os.makedirs(self.results_dir, exist_ok=True)
    
    def evaluate_algorithm(self, algorithm, test_resumes: List[str], 
                          test_jobs: List[str], ground_truth_scores: List[float],
                          algorithm_name: str) -> Dict[str, Any]:
        """Comprehensive evaluation of a single algorithm"""
        
        logger.info(f"Evaluating {algorithm_name} with {len(test_resumes)} test samples")
        
        # Get algorithm predictions
        predicted_scores = []
        processing_times = []
        
        for i, (resume, job) in enumerate(zip(test_resumes, test_jobs)):
            try:
                start_time = time.time()
                result = algorithm.process_single(resume, job)
                end_time = time.time()
                
                predicted_scores.append(result['score'])
                processing_times.append(end_time - start_time)
                
            except Exception as e:
                logger.error(f"Error processing sample {i} with {algorithm_name}: {e}")
                predicted_scores.append(0.0)  # Default score for failed predictions
                processing_times.append(0.0)
        
        # Calculate comprehensive metrics
        evaluation_results = {
            'algorithm': algorithm_name,
            'timestamp': datetime.now().isoformat(),
            'test_samples': len(test_resumes),
            'successful_predictions': sum(1 for score in predicted_scores if score > 0),
            'failed_predictions': sum(1 for score in predicted_scores if score == 0),
            
            # Regression Metrics
            'regression_metrics': self._calculate_regression_metrics(
                ground_truth_scores, predicted_scores
            ),
            
            # Ranking Metrics
            'ranking_metrics': self._calculate_ranking_metrics(
                ground_truth_scores, predicted_scores
            ),
            
            # Classification Metrics (if we convert to classes)
            'classification_metrics': self._calculate_classification_metrics(
                ground_truth_scores, predicted_scores
            ),
            
            # Performance Metrics
            'performance_metrics': {
                'avg_processing_time': np.mean(processing_times),
                'std_processing_time': np.std(processing_times),
                'min_processing_time': np.min(processing_times),
                'max_processing_time': np.max(processing_times),
                'total_processing_time': np.sum(processing_times)
            },
            
            # Statistical Analysis
            'statistical_analysis': self._calculate_statistical_analysis(
                ground_truth_scores, predicted_scores
            ),
            
            # Error Analysis
            'error_analysis': self._analyze_errors(
                ground_truth_scores, predicted_scores, test_resumes, test_jobs
            )
        }
        
        # Generate detailed report
        self._generate_algorithm_report(evaluation_results)
        
        return evaluation_results
    
    def _calculate_regression_metrics(self, y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
        """Calculate regression metrics for continuous score prediction"""
        
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        return {
            'mean_squared_error': float(mean_squared_error(y_true, y_pred)),
            'root_mean_squared_error': float(np.sqrt(mean_squared_error(y_true, y_pred))),
            'mean_absolute_error': float(mean_absolute_error(y_true, y_pred)),
            'r2_score': float(r2_score(y_true, y_pred)),
            'explained_variance': float(1 - np.var(y_true - y_pred) / np.var(y_true)),
            'max_error': float(np.max(np.abs(y_true - y_pred))),
            'mean_error': float(np.mean(y_true - y_pred))
        }
    
    def _calculate_ranking_metrics(self, y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
        """Calculate ranking-specific metrics"""
        
        # Convert to rankings
        true_rankings = np.argsort(np.argsort(-np.array(y_true)))
        pred_rankings = np.argsort(np.argsort(-np.array(y_pred)))
        
        # Spearman correlation (rank correlation)
        spearman_corr, spearman_p = spearmanr(y_true, y_pred)
        
        # Kendall's tau (another rank correlation)
        from scipy.stats import kendalltau
        kendall_corr, kendall_p = kendalltau(y_true, y_pred)
        
        # NDCG (Normalized Discounted Cumulative Gain)
        ndcg_score = self._calculate_ndcg(y_true, y_pred)
        
        # Top-k accuracy (how many of top-k predictions are actually in top-k)
        top_k_accuracies = {}
        for k in [1, 3, 5, 10]:
            if len(y_true) >= k:
                top_k_accuracies[f'top_{k}_accuracy'] = self._calculate_top_k_accuracy(
                    y_true, y_pred, k
                )
        
        return {
            'spearman_correlation': float(spearman_corr) if not np.isnan(spearman_corr) else 0.0,
            'spearman_p_value': float(spearman_p) if not np.isnan(spearman_p) else 1.0,
            'kendall_correlation': float(kendall_corr) if not np.isnan(kendall_corr) else 0.0,
            'kendall_p_value': float(kendall_p) if not np.isnan(kendall_p) else 1.0,
            'ndcg_score': float(ndcg_score),
            'ranking_accuracy': float(np.mean(true_rankings == pred_rankings)),
            **top_k_accuracies
        }
    
    def _calculate_classification_metrics(self, y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
        """Convert to classification problem and calculate metrics"""
        
        # Convert continuous scores to classes (Poor: 0-0.4, Good: 0.4-0.7, Excellent: 0.7-1.0)
        def score_to_class(score):
            if score < 0.4:
                return 0  # Poor
            elif score < 0.7:
                return 1  # Good
            else:
                return 2  # Excellent
        
        y_true_classes = [score_to_class(score) for score in y_true]
        y_pred_classes = [score_to_class(score) for score in y_pred]
        
        # Calculate classification metrics
        accuracy = accuracy_score(y_true_classes, y_pred_classes)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true_classes, y_pred_classes, average='weighted', zero_division=0
        )
        
        return {
            'classification_accuracy': float(accuracy),
            'weighted_precision': float(precision),
            'weighted_recall': float(recall),
            'weighted_f1_score': float(f1),
            'class_distribution_true': {
                'poor': sum(1 for c in y_true_classes if c == 0),
                'good': sum(1 for c in y_true_classes if c == 1),
                'excellent': sum(1 for c in y_true_classes if c == 2)
            },
            'class_distribution_pred': {
                'poor': sum(1 for c in y_pred_classes if c == 0),
                'good': sum(1 for c in y_pred_classes if c == 1),
                'excellent': sum(1 for c in y_pred_classes if c == 2)
            }
        }
    
    def _calculate_statistical_analysis(self, y_true: List[float], y_pred: List[float]) -> Dict[str, float]:
        """Calculate statistical analysis metrics"""
        
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Pearson correlation
        pearson_corr, pearson_p = pearsonr(y_true, y_pred)
        
        # Distribution statistics
        pred_stats = {
            'mean': float(np.mean(y_pred)),
            'std': float(np.std(y_pred)),
            'min': float(np.min(y_pred)),
            'max': float(np.max(y_pred)),
            'median': float(np.median(y_pred)),
            'q25': float(np.percentile(y_pred, 25)),
            'q75': float(np.percentile(y_pred, 75))
        }
        
        true_stats = {
            'mean': float(np.mean(y_true)),
            'std': float(np.std(y_true)),
            'min': float(np.min(y_true)),
            'max': float(np.max(y_true)),
            'median': float(np.median(y_true)),
            'q25': float(np.percentile(y_true, 25)),
            'q75': float(np.percentile(y_true, 75))
        }
        
        return {
            'pearson_correlation': float(pearson_corr) if not np.isnan(pearson_corr) else 0.0,
            'pearson_p_value': float(pearson_p) if not np.isnan(pearson_p) else 1.0,
            'prediction_stats': pred_stats,
            'ground_truth_stats': true_stats,
            'score_range_coverage': float((np.max(y_pred) - np.min(y_pred)) / (np.max(y_true) - np.min(y_true)))
        }
    
    def _analyze_errors(self, y_true: List[float], y_pred: List[float], 
                       resumes: List[str], jobs: List[str]) -> Dict[str, Any]:
        """Analyze prediction errors in detail"""
        
        errors = np.array(y_pred) - np.array(y_true)
        abs_errors = np.abs(errors)
        
        # Find worst predictions
        worst_indices = np.argsort(abs_errors)[-5:]  # Top 5 worst predictions
        best_indices = np.argsort(abs_errors)[:5]    # Top 5 best predictions
        
        worst_cases = []
        for idx in worst_indices:
            worst_cases.append({
                'index': int(idx),
                'true_score': float(y_true[idx]),
                'predicted_score': float(y_pred[idx]),
                'absolute_error': float(abs_errors[idx]),
                'resume_snippet': resumes[idx][:200] + "..." if len(resumes[idx]) > 200 else resumes[idx],
                'job_snippet': jobs[idx][:200] + "..." if len(jobs[idx]) > 200 else jobs[idx]
            })
        
        best_cases = []
        for idx in best_indices:
            best_cases.append({
                'index': int(idx),
                'true_score': float(y_true[idx]),
                'predicted_score': float(y_pred[idx]),
                'absolute_error': float(abs_errors[idx])
            })
        
        return {
            'error_distribution': {
                'mean_absolute_error': float(np.mean(abs_errors)),
                'std_absolute_error': float(np.std(abs_errors)),
                'max_absolute_error': float(np.max(abs_errors)),
                'min_absolute_error': float(np.min(abs_errors))
            },
            'bias_analysis': {
                'mean_error': float(np.mean(errors)),  # Positive = overestimation
                'overestimations': int(np.sum(errors > 0)),
                'underestimations': int(np.sum(errors < 0)),
                'perfect_predictions': int(np.sum(abs_errors < 0.05))  # Within 5% error
            },
            'worst_predictions': worst_cases,
            'best_predictions': best_cases,
            'error_patterns': self._identify_error_patterns(errors, resumes, jobs)
        }
    
    def _calculate_ndcg(self, y_true: List[float], y_pred: List[float], k: int = 10) -> float:
        """Calculate Normalized Discounted Cumulative Gain"""
        
        def dcg_at_k(scores, k):
            k = min(k, len(scores))
            return np.sum(scores[:k] / np.log2(np.arange(2, k + 2)))
        
        # Sort by predictions and calculate DCG
        pred_order = np.argsort(y_pred)[::-1]  # Descending order
        true_scores_sorted = [y_true[i] for i in pred_order]
        
        dcg = dcg_at_k(true_scores_sorted, k)
        
        # Calculate IDCG (Ideal DCG)
        ideal_scores_sorted = sorted(y_true, reverse=True)
        idcg = dcg_at_k(ideal_scores_sorted, k)
        
        return dcg / idcg if idcg > 0 else 0.0
    
    def _calculate_top_k_accuracy(self, y_true: List[float], y_pred: List[float], k: int) -> float:
        """Calculate top-k accuracy"""
        
        true_top_k = set(np.argsort(y_true)[-k:])
        pred_top_k = set(np.argsort(y_pred)[-k:])
        
        return len(true_top_k.intersection(pred_top_k)) / k
    
    def _identify_error_patterns(self, errors: np.ndarray, resumes: List[str], jobs: List[str]) -> Dict[str, Any]:
        """Identify patterns in prediction errors"""
        
        patterns = {
            'high_error_keywords': [],
            'low_error_keywords': [],
            'error_by_resume_length': {},
            'error_by_job_complexity': {}
        }
        
        # Analyze error by resume length
        resume_lengths = [len(resume.split()) for resume in resumes]
        length_categories = ['short (<150)', 'medium (150-300)', 'long (>300)']
        length_errors = [[], [], []]
        
        for i, length in enumerate(resume_lengths):
            error = abs(errors[i])
            if length < 150:
                length_errors[0].append(error)
            elif length < 300:
                length_errors[1].append(error)
            else:
                length_errors[2].append(error)
        
        for i, category in enumerate(length_categories):
            if length_errors[i]:
                patterns['error_by_resume_length'][category] = {
                    'mean_error': float(np.mean(length_errors[i])),
                    'count': len(length_errors[i])
                }
        
        return patterns
    
    def compare_algorithms(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compare multiple algorithms and generate comprehensive comparison"""
        
        comparison = {
            'timestamp': datetime.now().isoformat(),
            'algorithms_compared': [result['algorithm'] for result in evaluation_results],
            'best_performers': {},
            'rankings': {},
            'statistical_significance': {},
            'recommendations': []
        }
        
        # Compare each metric
        metrics_to_compare = [
            'r2_score', 'mean_absolute_error', 'spearman_correlation',
            'classification_accuracy', 'ndcg_score', 'avg_processing_time'
        ]
        
        for metric in metrics_to_compare:
            values = []
            algorithms = []
            
            for result in evaluation_results:
                try:
                    if metric == 'avg_processing_time':
                        value = result['performance_metrics'][metric]
                    elif metric in ['r2_score', 'mean_absolute_error']:
                        value = result['regression_metrics'][metric]
                    elif metric == 'spearman_correlation':
                        value = result['ranking_metrics'][metric]
                    elif metric == 'classification_accuracy':
                        value = result['classification_metrics'][metric]
                    elif metric == 'ndcg_score':
                        value = result['ranking_metrics'][metric]
                    else:
                        continue
                    
                    values.append(value)
                    algorithms.append(result['algorithm'])
                except KeyError:
                    continue
            
            if values:
                # For error metrics, lower is better
                reverse = metric in ['mean_absolute_error', 'avg_processing_time']
                best_idx = np.argmin(values) if reverse else np.argmax(values)
                
                comparison['best_performers'][metric] = {
                    'algorithm': algorithms[best_idx],
                    'value': values[best_idx],
                    'all_values': dict(zip(algorithms, values))
                }
        
        # Generate overall ranking
        comparison['rankings'] = self._calculate_overall_ranking(evaluation_results)
        
        # Generate recommendations
        comparison['recommendations'] = self._generate_recommendations(evaluation_results, comparison)
        
        return comparison
    
    def _calculate_overall_ranking(self, evaluation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate overall algorithm ranking based on multiple criteria"""
        
        scores = {}
        
        for result in evaluation_results:
            algorithm = result['algorithm']
            score = 0
            
            # Weight different aspects
            weights = {
                'accuracy': 0.4,    # 40% - Most important
                'ranking': 0.3,     # 30% - Important for ranking tasks  
                'performance': 0.2, # 20% - Processing speed
                'reliability': 0.1  # 10% - Consistent performance
            }
            
            # Accuracy component (higher is better)
            try:
                r2 = result['regression_metrics']['r2_score']
                mae = result['regression_metrics']['mean_absolute_error']
                accuracy_score = max(0, r2) * 0.7 + max(0, (1 - mae)) * 0.3
                score += accuracy_score * weights['accuracy']
            except KeyError:
                pass
            
            # Ranking component (higher is better)  
            try:
                spearman = result['ranking_metrics']['spearman_correlation']
                ndcg = result['ranking_metrics']['ndcg_score']
                ranking_score = max(0, spearman) * 0.6 + max(0, ndcg) * 0.4
                score += ranking_score * weights['ranking']
            except KeyError:
                pass
            
            # Performance component (faster is better, normalized)
            try:
                avg_time = result['performance_metrics']['avg_processing_time']
                # Assume 10 seconds is very slow, 0.1 seconds is very fast
                performance_score = max(0, 1 - min(avg_time / 10.0, 1))
                score += performance_score * weights['performance']
            except KeyError:
                pass
            
            # Reliability component (lower error variance is better)
            try:
                std_error = result['error_analysis']['error_distribution']['std_absolute_error']
                reliability_score = max(0, 1 - min(std_error, 1))
                score += reliability_score * weights['reliability']
            except KeyError:
                pass
            
            scores[algorithm] = score
        
        # Rank algorithms
        ranked_algorithms = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'overall_scores': scores,
            'ranking_order': [alg for alg, score in ranked_algorithms],
            'top_performer': ranked_algorithms[0] if ranked_algorithms else None,
            'scoring_weights': weights
        }
    
    def _generate_recommendations(self, evaluation_results: List[Dict[str, Any]], 
                                comparison: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on evaluation results"""
        
        recommendations = []
        
        # Check for data quality issues
        avg_r2 = np.mean([r['regression_metrics']['r2_score'] 
                         for r in evaluation_results 
                         if 'regression_metrics' in r])
        
        if avg_r2 < 0.5:
            recommendations.append(
                "LOW ACCURACY DETECTED: Average R² score is below 0.5. "
                "Consider collecting more diverse training data or using different algorithms."
            )
        
        # Check for processing time issues
        slow_algorithms = []
        for result in evaluation_results:
            if result['performance_metrics']['avg_processing_time'] > 5.0:
                slow_algorithms.append(result['algorithm'])
        
        if slow_algorithms:
            recommendations.append(
                f"PERFORMANCE ISSUE: {', '.join(slow_algorithms)} are slow (>5s per resume). "
                "Consider optimization or using faster algorithms for real-time applications."
            )
        
        # Check for bias issues
        for result in evaluation_results:
            mean_error = result['error_analysis']['bias_analysis']['mean_error']
            if abs(mean_error) > 0.1:
                bias_type = "overestimation" if mean_error > 0 else "underestimation"
                recommendations.append(
                    f"BIAS DETECTED: {result['algorithm']} shows {bias_type} bias "
                    f"(mean error: {mean_error:.3f}). Review training data balance."
                )
        
        # Recommend best algorithm combination
        top_3 = comparison['rankings']['ranking_order'][:3]
        if len(top_3) >= 2:
            recommendations.append(
                f"ENSEMBLE RECOMMENDATION: Consider combining {', '.join(top_3[:2])} "
                "for improved accuracy through ensemble methods."
            )
        
        return recommendations
    
    def generate_final_report(self, evaluation_results: List[Dict[str, Any]]) -> str:
        """Generate comprehensive final evaluation report"""
        
        comparison = self.compare_algorithms(evaluation_results)
        
        report = f"""
# Resume Ranking Algorithm Evaluation Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
This report presents a comprehensive evaluation of {len(evaluation_results)} resume ranking algorithms 
using multiple accuracy metrics and performance indicators.

## Algorithms Evaluated
{chr(10).join([f"- {result['algorithm']}" for result in evaluation_results])}

## Key Findings

### Overall Performance Ranking
"""
        
        for i, (algorithm, score) in enumerate(zip(
            comparison['rankings']['ranking_order'],
            [comparison['rankings']['overall_scores'][alg] 
             for alg in comparison['rankings']['ranking_order']]
        )):
            report += f"{i+1}. **{algorithm}** (Score: {score:.3f})\n"
        
        report += "\n### Metric Analysis\n"
        
        for metric, data in comparison['best_performers'].items():
            report += f"- **{metric}**: {data['algorithm']} ({data['value']:.3f})\n"
        
        report += f"\n### Recommendations\n"
        for i, rec in enumerate(comparison['recommendations'], 1):
            report += f"{i}. {rec}\n"
        
        # Save report
        report_file = os.path.join(self.results_dir, 
                                 f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        with open(report_file, 'w') as f:
            f.write(report)
        
        return report
