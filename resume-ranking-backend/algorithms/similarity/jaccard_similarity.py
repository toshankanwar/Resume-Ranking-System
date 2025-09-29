import re
from collections import Counter
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class JaccardSimilarityAnalyzer(BaseAlgorithm):
    """Jaccard Similarity for skill-focused resume matching"""
    
    def __init__(self, config: dict = None):
        super().__init__('jaccard', config)
        self.skill_keywords = self._load_skill_keywords()
        self.stop_words = self._load_stop_words()
    
    def _load_skill_keywords(self) -> set:
        """Load comprehensive skill keywords"""
        return {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'csharp', 'c#', 'php',
            'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql',
            
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'svelte', 'nodejs', 'express',
            'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net', 'bootstrap',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'elasticsearch',
            'oracle', 'sqlite', 'dynamodb', 'neo4j', 'influxdb',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
            'ansible', 'puppet', 'chef', 'vagrant', 'git', 'gitlab', 'github',
            
            # Data Science & ML
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
            'seaborn', 'jupyter', 'spark', 'hadoop', 'tableau', 'powerbi',
            
            # Mobile Development
            'android', 'ios', 'react-native', 'flutter', 'xamarin', 'ionic',
            
            # Testing
            'selenium', 'junit', 'testng', 'cypress', 'jest', 'mocha', 'pytest',
            
            # Tools & IDEs
            'vscode', 'intellij', 'eclipse', 'xcode', 'sublime', 'vim', 'postman',
            'jira', 'confluence', 'slack', 'trello'
        }
    
    def _load_stop_words(self) -> set:
        """Load common stop words"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us'
        }
    
    def load_model(self):
        """Initialize Jaccard analyzer (no model to load)"""
        self.is_loaded = True
        logger.info("Jaccard similarity analyzer initialized")
    
    def _preprocess_text(self, text: str) -> set:
        """Preprocess text and extract meaningful terms"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep alphanumeric and common separators
        text = re.sub(r'[^\w\s\-\.\+#]', ' ', text)
        
        # Extract words
        words = set(text.split())
        
        # Remove stop words and short words
        words = {word for word in words if len(word) > 2 and word not in self.stop_words}
        
        # Extract compound skills (e.g., "machine learning", "data science")
        compound_skills = self._extract_compound_skills(text)
        words.update(compound_skills)
        
        return words
    
    def _extract_compound_skills(self, text: str) -> set:
        """Extract compound skill phrases"""
        compound_patterns = [
            'machine learning', 'data science', 'artificial intelligence', 'deep learning',
            'natural language processing', 'computer vision', 'big data', 'data analysis',
            'web development', 'mobile development', 'software engineering', 'full stack',
            'front end', 'back end', 'user experience', 'user interface', 'quality assurance',
            'project management', 'agile development', 'scrum master', 'product management',
            'business intelligence', 'cloud computing', 'cyber security', 'database design',
            'api development', 'microservices', 'responsive design', 'test automation'
        ]
        
        found_compounds = set()
        for pattern in compound_patterns:
            if pattern in text:
                # Replace spaces with underscores for compound skills
                compound_key = pattern.replace(' ', '_')
                found_compounds.add(compound_key)
        
        return found_compounds
    
    def _extract_skills_only(self, words: set) -> set:
        """Extract only technical skills from word set"""
        skills = set()
        
        # Direct skill matches
        skills.update(words & self.skill_keywords)
        
        # Partial matches for variations (e.g., "javascript" matches "js")
        word_variations = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine_learning',
            'ai': 'artificial_intelligence',
            'ui': 'user_interface',
            'ux': 'user_experience'
        }
        
        for word in words:
            if word in word_variations:
                skills.add(word_variations[word])
        
        return skills
    
    def _calculate_jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calculate Jaccard similarity coefficient"""
        if not set1 and not set2:
            return 1.0
        
        intersection = set1 & set2
        union = set1 | set2
        
        return len(intersection) / len(union) if union else 0.0
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with Jaccard similarity"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Preprocess texts
            resume_words = self._preprocess_text(resume_text)
            job_words = self._preprocess_text(job_description)
            
            # Extract skills specifically
            resume_skills = self._extract_skills_only(resume_words)
            job_skills = self._extract_skills_only(job_words)
            
            # Calculate similarities
            # 1. Overall word similarity
            overall_similarity = self._calculate_jaccard_similarity(resume_words, job_words)
            
            # 2. Skills-focused similarity (weighted more heavily)
            skills_similarity = self._calculate_jaccard_similarity(resume_skills, job_skills)
            
            # Combined score with more weight on skills
            combined_score = (overall_similarity * 0.3) + (skills_similarity * 0.7)
            
            # Find matching skills
            matching_skills = list(resume_skills & job_skills)
            missing_skills = list(job_skills - resume_skills)
            additional_skills = list(resume_skills - job_skills)
            
            return {
                'algorithm': self.name,
                'score': float(combined_score),
                'overall_similarity': float(overall_similarity),
                'skills_similarity': float(skills_similarity),
                'details': {
                    'resume_words_count': len(resume_words),
                    'job_words_count': len(job_words),
                    'resume_skills_count': len(resume_skills),
                    'job_skills_count': len(job_skills),
                    'matching_skills': matching_skills[:10],  # Top 10
                    'missing_skills': missing_skills[:10],    # Top 10
                    'additional_skills': additional_skills[:10],  # Top 10
                    'skill_match_ratio': len(matching_skills) / max(len(job_skills), 1)
                }
            }
            
        except Exception as e:
            logger.error(f"Jaccard similarity processing failed: {e}")
            raise
