from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class JobDescription:
    """Job description data model"""
    
    text: str
    position: str
    created_at: datetime
    
    # Extracted information
    required_skills: List[str] = None
    experience_level: str = None
    education_requirements: List[str] = None
    responsibilities: List[str] = None
    
    # Metadata
    word_count: int = 0
    char_count: int = 0
    processed: bool = False
    
    def __post_init__(self):
        if self.required_skills is None:
            self.required_skills = []
        if self.education_requirements is None:
            self.education_requirements = []
        if self.responsibilities is None:
            self.responsibilities = []
        
        # Calculate counts
        self.word_count = len(self.text.split())
        self.char_count = len(self.text)
    
    def extract_requirements(self):
        """Extract structured information from job description"""
        import re
        
        text_lower = self.text.lower()
        
        # Extract experience level
        exp_patterns = [
            (r'(\d+)\+?\s*years?\s*(?:of\s*)?experience', lambda m: f"{m.group(1)}+ years"),
            (r'entry[- ]?level', lambda m: "Entry Level"),
            (r'junior', lambda m: "Junior Level"),
            (r'senior', lambda m: "Senior Level"),
            (r'lead', lambda m: "Lead Level"),
            (r'principal', lambda m: "Principal Level")
        ]
        
        for pattern, formatter in exp_patterns:
            match = re.search(pattern, text_lower)
            if match:
                self.experience_level = formatter(match)
                break
        
        # Extract common skills
        skill_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node.js', 'django', 'flask', 'spring', 'sql', 'nosql',
            'aws', 'azure', 'docker', 'kubernetes', 'git'
        ]
        
        for skill in skill_keywords:
            if skill in text_lower:
                self.required_skills.append(skill)
        
        # Extract education requirements
        edu_patterns = [
            r'bachelor(?:\'?s)?\s*(?:degree)?',
            r'master(?:\'?s)?\s*(?:degree)?',
            r'phd|ph\.d|doctorate',
            r'mba',
            r'computer science|cs\b',
            r'engineering'
        ]
        
        for pattern in edu_patterns:
            if re.search(pattern, text_lower):
                self.education_requirements.append(pattern.replace(r'\b', '').replace('\\', ''))
        
        self.processed = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'text': self.text,
            'position': self.position,
            'created_at': self.created_at.isoformat(),
            'required_skills': self.required_skills,
            'experience_level': self.experience_level,
            'education_requirements': self.education_requirements,
            'word_count': self.word_count,
            'char_count': self.char_count,
            'processed': self.processed
        }
