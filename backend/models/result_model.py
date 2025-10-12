from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from .resume_model import Resume
from .job_model import JobDescription

@dataclass
class ProcessingResult:
    """Complete processing result model"""
    
    job_description: JobDescription
    resumes: List[Resume]
    algorithms_used: List[str]
    processing_started_at: datetime
    processing_completed_at: Optional[datetime] = None
    
    # Summary statistics
    total_processing_time: float = 0.0
    successful_resumes: int = 0
    failed_resumes: int = 0
    
    # Algorithm performance
    algorithm_performance: Dict[str, Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.algorithm_performance is None:
            self.algorithm_performance = {}
        
        # Calculate summary stats
        self.successful_resumes = len([r for r in self.resumes if not r.errors])
        self.failed_resumes = len([r for r in self.resumes if r.errors])
    
    def mark_completed(self):
        """Mark processing as completed"""
        self.processing_completed_at = datetime.utcnow()
        if self.processing_started_at:
            self.total_processing_time = (
                self.processing_completed_at - self.processing_started_at
            ).total_seconds()
    
    def get_top_resumes(self, n: int = 10) -> List[Resume]:
        """Get top N resumes by combined score"""
        sorted_resumes = sorted(
            self.resumes, 
            key=lambda r: r.combined_score, 
            reverse=True
        )
        return sorted_resumes[:n]
    
    def get_algorithm_summary(self) -> Dict[str, Any]:
        """Get summary of algorithm performance"""
        summary = {}
        
        for algorithm in self.algorithms_used:
            scores = []
            processing_times = []
            
            for resume in self.resumes:
                if algorithm in resume.scores:
                    score_data = resume.scores[algorithm]
                    score = score_data['score'] if isinstance(score_data, dict) else score_data
                    scores.append(score)
            
            if scores:
                summary[algorithm] = {
                    'average_score': sum(scores) / len(scores),
                    'max_score': max(scores),
                    'min_score': min(scores),
                    'processed_resumes': len(scores)
                }
        
        return summary
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'job_description': self.job_description.to_dict(),
            'resumes': [resume.to_dict() for resume in self.resumes],
            'algorithms_used': self.algorithms_used,
            'processing_started_at': self.processing_started_at.isoformat(),
            'processing_completed_at': self.processing_completed_at.isoformat() if self.processing_completed_at else None,
            'total_processing_time': self.total_processing_time,
            'successful_resumes': self.successful_resumes,
            'failed_resumes': self.failed_resumes,
            'algorithm_performance': self.algorithm_performance,
            'algorithm_summary': self.get_algorithm_summary()
        }
