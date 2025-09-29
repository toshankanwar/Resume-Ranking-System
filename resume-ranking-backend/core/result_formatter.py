from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import logging
import numpy as np

logger = logging.getLogger(__name__)

class ResultFormatter:
    """Formats processing results for different output formats"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.include_debug_info = self.config.get('include_debug_info', False)
        self.max_skills_display = self.config.get('max_skills_display', 20)
        self.max_explanation_length = self.config.get('max_explanation_length', 500)
    
    def format_for_frontend(self, processing_results: Dict[str, Any], include_detailed_breakdown: bool = True) -> Dict[str, Any]:
        """Format results for frontend consumption"""
        try:
            formatted_results = {
                'success': True,
                'timestamp': datetime.utcnow().isoformat(),
                'summary': self._format_summary(processing_results),
                'results': self._format_resume_results(processing_results),
                'metadata': self._format_metadata(processing_results)
            }
            
            if include_detailed_breakdown:
                formatted_results['algorithm_performance'] = self._format_algorithm_performance(processing_results)
                formatted_results['score_analysis'] = self._format_score_analysis(processing_results)
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Result formatting failed: {e}")
            return {
                'success': False,
                'error': f'Result formatting failed: {str(e)}',
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def _format_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format summary statistics"""
        combined_results = results.get('combined_results', [])
        metadata = results.get('metadata', {})
        
        return {
            'total_resumes': len(combined_results),
            'algorithms_used': metadata.get('algorithms_used', []),
            'processing_time': metadata.get('total_processing_time', 0),
            'average_score': self._calculate_average_score(combined_results),
            'top_score': self._get_top_score(combined_results),
            'score_distribution': self._get_score_distribution(combined_results)
        }
    
    def _format_resume_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Format individual resume results"""
        combined_results = results.get('combined_results', [])
        formatted_resumes = []
        
        for resume_result in combined_results:
            try:
                formatted_resume = {
                    'rank': resume_result.get('rank', 0),
                    'filename': resume_result.get('filename', 'Unknown'),
                    'final_score': round(resume_result.get('combined_score', 0.0), 3),
                    'scores': self._format_individual_scores(resume_result.get('algorithm_scores', {})),
                    'explanation': self._generate_explanation(resume_result),
                    'extracted_skills': self._format_skills(resume_result),
                    'strengths': self._identify_strengths(resume_result),
                    'areas_for_improvement': self._identify_improvements(resume_result),
                    'confidence_level': self._calculate_confidence(resume_result)
                }
                
                if self.include_debug_info:
                    formatted_resume['debug'] = {
                        'processing_errors': resume_result.get('errors', []),
                        'raw_algorithm_data': resume_result.get('algorithm_scores', {}),
                        'processing_time': resume_result.get('processing_time', 0)
                    }
                
                formatted_resumes.append(formatted_resume)
                
            except Exception as e:
                logger.error(f"Error formatting resume result: {e}")
                continue
        
        return formatted_resumes
    
    def _format_individual_scores(self, algorithm_scores: Dict[str, Any]) -> Dict[str, Any]:
        """Format individual algorithm scores"""
        formatted_scores = {}
        
        for algorithm, score_data in algorithm_scores.items():
            try:
                if isinstance(score_data, dict):
                    score = score_data.get('score', 0.0)
                    details = score_data.get('details', {})
                else:
                    score = float(score_data)
                    details = {}
                
                formatted_scores[algorithm] = {
                    'score': round(score, 3),
                    'percentage': f"{score * 100:.1f}%",
                    'category': self._categorize_score(score),
                    'details': self._extract_relevant_details(details)
                }
                
            except Exception as e:
                logger.error(f"Error formatting score for {algorithm}: {e}")
                formatted_scores[algorithm] = {
                    'score': 0.0,
                    'percentage': "0.0%",
                    'category': 'poor',
                    'details': {}
                }
        
        return formatted_scores
    
    def _calculate_average_score(self, combined_results: List[Dict]) -> float:
        """Calculate average combined score"""
        if not combined_results:
            return 0.0
        scores = [r.get('combined_score', 0.0) for r in combined_results]
        return round(sum(scores) / len(scores), 3)
    
    def _get_top_score(self, combined_results: List[Dict]) -> float:
        """Get highest combined score"""
        if not combined_results:
            return 0.0
        scores = [r.get('combined_score', 0.0) for r in combined_results]
        return round(max(scores), 3)
    
    def _get_score_distribution(self, combined_results: List[Dict]) -> Dict[str, int]:
        """Get score distribution by categories"""
        distribution = {'excellent': 0, 'good': 0, 'fair': 0, 'poor': 0}
        
        for result in combined_results:
            score = result.get('combined_score', 0.0)
            category = self._categorize_score(score)
            distribution[category] += 1
        
        return distribution
    
    def _categorize_score(self, score: float) -> str:
        """Categorize score into performance levels"""
        if score >= 0.8:
            return 'excellent'
        elif score >= 0.6:
            return 'good'
        elif score >= 0.4:
            return 'fair'
        else:
            return 'poor'
    
    def _generate_explanation(self, resume_result: Dict[str, Any]) -> str:
        """Generate human-readable explanation"""
        try:
            score = resume_result.get('combined_score', 0.0)
            algorithm_scores = resume_result.get('algorithm_scores', {})
            
            category = self._categorize_score(score)
            category_descriptions = {
                'excellent': 'Excellent match for this position',
                'good': 'Good match with strong qualifications', 
                'fair': 'Fair match with some relevant experience',
                'poor': 'Limited match for this position'
            }
            
            explanation = f"{category_descriptions[category]} (Overall: {score:.1%}). "
            
            # Find best performing algorithm
            if algorithm_scores:
                best_alg = max(algorithm_scores.keys(), 
                             key=lambda k: algorithm_scores[k].get('score', 0), 
                             default='unknown')
                best_score = algorithm_scores.get(best_alg, {}).get('score', 0)
                explanation += f"Strongest performance in {best_alg.upper()} analysis ({best_score:.1%}). "
            
            # Add specific insights
            insights = []
            for alg_name, alg_data in algorithm_scores.items():
                details = alg_data.get('details', {})
                if alg_name == 'ner' and 'extracted_skills' in details:
                    skill_count = len(details.get('extracted_skills', {}))
                    if skill_count > 0:
                        insights.append(f"Identified {skill_count} skill categories")
                
                elif alg_name == 'cosine' and 'top_matching_terms' in details:
                    term_count = len(details.get('top_matching_terms', []))
                    if term_count > 0:
                        insights.append(f"Found {term_count} key matching terms")
            
            if insights:
                explanation += ". ".join(insights) + "."
            
            return explanation[:self.max_explanation_length]
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Analysis completed with combined score of {resume_result.get('combined_score', 0):.1%}"
    
    def _format_skills(self, resume_result: Dict[str, Any]) -> List[str]:
        """Format extracted skills"""
        skills = set()
        algorithm_scores = resume_result.get('algorithm_scores', {})
        
        # Extract skills from NER results
        if 'ner' in algorithm_scores:
            ner_details = algorithm_scores['ner'].get('details', {})
            extracted_skills = ner_details.get('extracted_skills', {})
            for category, skill_list in extracted_skills.items():
                for skill_data in skill_list:
                    if isinstance(skill_data, dict):
                        skills.add(skill_data.get('skill', '').title())
                    else:
                        skills.add(str(skill_data).title())
        
        return sorted(list(skills))[:self.max_skills_display]
    
    def _identify_strengths(self, resume_result: Dict[str, Any]) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        algorithm_scores = resume_result.get('algorithm_scores', {})
        
        for alg_name, alg_data in algorithm_scores.items():
            score = alg_data.get('score', 0.0)
            if score >= 0.7:  # Strong performance threshold
                if alg_name == 'bert':
                    strengths.append("Strong semantic match with job requirements")
                elif alg_name == 'ner':
                    strengths.append("Excellent skill and experience extraction")
                elif alg_name == 'cosine':
                    strengths.append("High keyword and terminology match")
                elif alg_name in ['xgboost', 'random_forest']:
                    strengths.append("Strong overall profile match")
        
        return strengths
    
    def _identify_improvements(self, resume_result: Dict[str, Any]) -> List[str]:
        """Identify areas for improvement"""
        improvements = []
        algorithm_scores = resume_result.get('algorithm_scores', {})
        
        for alg_name, alg_data in algorithm_scores.items():
            score = alg_data.get('score', 0.0)
            if score < 0.5:  # Low performance threshold
                if alg_name == 'ner':
                    improvements.append("Limited relevant skills or experience mentioned")
                elif alg_name == 'cosine':
                    improvements.append("Few matching keywords with job description")
                elif alg_name == 'bert':
                    improvements.append("Weak semantic alignment with job requirements")
        
        return improvements
    
    def _calculate_confidence(self, resume_result: Dict[str, Any]) -> str:
        """Calculate confidence level in the ranking"""
        algorithm_scores = resume_result.get('algorithm_scores', {})
        
        if len(algorithm_scores) < 2:
            return 'low'
        
        scores = [alg_data.get('score', 0.0) for alg_data in algorithm_scores.values()]
        std_dev = np.std(scores)
        
        if std_dev < 0.1:
            return 'high'
        elif std_dev < 0.25:
            return 'medium'
        else:
            return 'low'
    
    def _format_metadata(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format metadata information"""
        return {
            'processing_timestamp': datetime.utcnow().isoformat(),
            'total_algorithms': len(results.get('algorithm_performance', {})),
            'successful_processing': True,
            'version': '1.0.0'
        }
    
    def _format_algorithm_performance(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format algorithm performance data"""
        return results.get('algorithm_performance', {})
    
    def _format_score_analysis(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Format score analysis"""
        combined_results = results.get('combined_results', [])
        
        if not combined_results:
            return {}
        
        all_scores = []
        for result in combined_results:
            all_scores.append(result.get('combined_score', 0.0))
        
        return {
            'mean_score': float(np.mean(all_scores)),
            'median_score': float(np.median(all_scores)),
            'std_deviation': float(np.std(all_scores)),
            'min_score': float(np.min(all_scores)),
            'max_score': float(np.max(all_scores)),
            'score_range': float(np.max(all_scores) - np.min(all_scores))
        }
    
    def _extract_relevant_details(self, details: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant details for frontend display"""
        relevant_details = {}
        
        # Common relevant fields
        relevant_fields = [
            'model_used', 'embedding_dimension', 'feature_count', 
            'matching_terms', 'skill_match_ratio', 'experience_score',
            'top_features', 'kernel', 'n_estimators'
        ]
        
        for field in relevant_fields:
            if field in details:
                relevant_details[field] = details[field]
        
        return relevant_details
