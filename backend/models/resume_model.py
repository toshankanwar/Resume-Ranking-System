from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Resume:
    """Resume data model"""
    
    filename: str
    text: str
    file_size: int
    word_count: int
    char_count: int
    extracted_at: datetime
    
    # Processing results
    scores: Dict[str, float] = None
    combined_score: float = 0.0
    rank: int = 0
    
    # Extracted information
    extracted_skills: List[str] = None
    extracted_experience: Dict[str, Any] = None
    sections: Dict[str, str] = None
    
    # Metadata
    processing_time: float = 0.0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.scores is None:
            self.scores = {}
        if self.extracted_skills is None:
            self.extracted_skills = []
        if self.extracted_experience is None:
            self.extracted_experience = {}
        if self.sections is None:
            self.sections = {}
        if self.errors is None:
            self.errors = []
    
    def add_algorithm_score(self, algorithm: str, score: float, details: Dict[str, Any] = None):
        """Add score from an algorithm"""
        self.scores[algorithm] = {
            'score': score,
            'details': details or {}
        }
    
    def calculate_combined_score(self, weights: Dict[str, float] = None):
        """Calculate weighted combined score"""
        if not self.scores:
            return 0.0
        
        if weights is None:
            # Default equal weights
            weights = {alg: 1.0 for alg in self.scores.keys()}
        
        total_weight = 0
        weighted_sum = 0
        
        for algorithm, score_data in self.scores.items():
            weight = weights.get(algorithm, 1.0)
            score = score_data['score'] if isinstance(score_data, dict) else score_data
            
            weighted_sum += score * weight
            total_weight += weight
        
        self.combined_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        return self.combined_score
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'filename': self.filename,
            'file_size': self.file_size,
            'word_count': self.word_count,
            'char_count': self.char_count,
            'extracted_at': self.extracted_at.isoformat(),
            'scores': self.scores,
            'combined_score': self.combined_score,
            'rank': self.rank,
            'extracted_skills': self.extracted_skills,
            'extracted_experience': self.extracted_experience,
            'processing_time': self.processing_time,
            'errors': self.errors
        }
