from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging
import re
from collections import Counter

logger = logging.getLogger(__name__)


class CosineSimilarityAnalyzer(BaseAlgorithm):
    """Fixed TF-IDF based cosine similarity for resume ranking with proper scoring"""
    
    def __init__(self, config: dict = None):
        super().__init__('cosine', config)
        self.vectorizer = None
        self.max_features = self.config.get('max_features', 3000)
        self.ngram_range = self.config.get('ngram_range', (1, 2))
    
    def load_model(self):
        """Initialize TF-IDF vectorizer with optimal parameters"""
        try:
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words='english',
                ngram_range=self.ngram_range,
                lowercase=True,
                token_pattern=r'\b[A-Za-z0-9+#.]{2,}\b',  # Include special chars for tech terms
                min_df=1,
                max_df=1.0,
                sublinear_tf=True,
                norm='l2',
                smooth_idf=True,
                use_idf=True
            )
            self.is_loaded = True
            logger.info("Cosine similarity analyzer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize cosine similarity: {e}")
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """Enhanced preprocessing with better normalization"""
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Normalize common technical terms and abbreviations
        tech_normalizations = {
            r'\bjs\b': 'javascript',
            r'\bts\b': 'typescript',
            r'\breactjs\b': 'react',
            r'\bnodejs\b': 'nodejs',
            r'\bnode\.js\b': 'nodejs',
            r'\bvuejs\b': 'vue',
            r'\bangularjs\b': 'angular',
            r'\bml\b': 'machinelearning',
            r'\bai\b': 'artificialintelligence',
            r'\baws\b': 'amazonwebservices',
            r'\bgcp\b': 'googlecloud',
            r'\bapi\b': 'applicationprogramminginterface',
            r'\brest\b': 'restful',
            r'\bui\b': 'userinterface',
            r'\bux\b': 'userexperience',
            r'\bci/cd\b': 'cicd',
            r'\bdevops\b': 'developmentoperations',
            r'\bc\+\+': 'cplusplus',
            r'\bc#': 'csharp',
            r'\b\.net\b': 'dotnet',
            r'\bsql\b': 'structuredquerylanguage',
            r'\bhtml\b': 'html5',
            r'\bcss\b': 'css3',
            r'\bdb\b': 'database',
            r'\bfrontend\b': 'frontend',
            r'\bbackend\b': 'backend',
            r'\bfullstack\b': 'fullstack',
            r'\bfull stack\b': 'fullstack',
            r'\bfull-stack\b': 'fullstack'
        }
        
        for pattern, replacement in tech_normalizations.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Normalize experience mentions
        text = re.sub(r'(\d+)\s*\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)?', 
                     r'\1years', text)
        
        # Normalize education degrees
        text = re.sub(r'\bb\.?s\.?\b', 'bachelors', text, flags=re.IGNORECASE)
        text = re.sub(r'\bm\.?s\.?\b', 'masters', text, flags=re.IGNORECASE)
        text = re.sub(r'\bphd\b|\bph\.?d\.?\b', 'doctorate', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbtech\b|\bb\.tech\b', 'bachelors', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmba\b|\bm\.b\.a\b', 'masters', text, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with fixed cosine similarity calculation"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Validate inputs
            if not resume_text or not job_description:
                return {
                    'algorithm': self.name,
                    'score': 0.0,
                    'details': {'error': 'Empty input text'}
                }
            
            # Preprocess texts
            processed_resume = self._preprocess_text(resume_text)
            processed_job = self._preprocess_text(job_description)
            
            # Calculate multiple similarity metrics for better accuracy
            
            # 1. TF-IDF Cosine Similarity
            tfidf_score = self._calculate_tfidf_similarity(processed_resume, processed_job)
            
            # 2. Keyword Match Score
            keyword_score = self._calculate_keyword_match(processed_resume, processed_job)
            
            # 3. Jaccard Similarity (token overlap)
            jaccard_score = self._calculate_jaccard_similarity(processed_resume, processed_job)
            
            # 4. Skill Match Score
            skill_score = self._calculate_skill_match(resume_text, job_description)
            
            # Weighted combination of all metrics
            combined_score = (
                tfidf_score * 0.40 +      # TF-IDF is most important
                keyword_score * 0.30 +     # Direct keyword matching
                jaccard_score * 0.20 +     # Token overlap
                skill_score * 0.10         # Skill-specific matching
            )
            
            # Apply experience boost/penalty
            experience_factor = self._calculate_experience_match(resume_text, job_description)
            final_score = combined_score * experience_factor
            
            # Ensure score is in valid range [0.0, 1.0]
            final_score = max(0.0, min(1.0, final_score))
            
            # Get detailed matching information
            matching_details = self._get_matching_details(processed_resume, processed_job)
            
            return {
                'algorithm': self.name,
                'score': float(final_score),
                'details': {
                    'tfidf_similarity': float(tfidf_score),
                    'keyword_match': float(keyword_score),
                    'jaccard_similarity': float(jaccard_score),
                    'skill_match': float(skill_score),
                    'experience_factor': float(experience_factor),
                    'combined_raw_score': float(combined_score),
                    'top_matching_terms': matching_details['top_terms'],
                    'matching_skills': matching_details['matching_skills'],
                    'total_job_keywords': matching_details['total_job_keywords'],
                    'matched_job_keywords': matching_details['matched_keywords'],
                    'match_percentage': float(matching_details['match_percentage'])
                }
            }
            
        except Exception as e:
            logger.error(f"Cosine similarity processing failed: {e}", exc_info=True)
            return {
                'algorithm': self.name,
                'score': 0.0,
                'details': {'error': str(e)}
            }
    
    def _calculate_tfidf_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate TF-IDF based cosine similarity"""
        try:
            # Fit vectorizer on both documents
            documents = [resume_text, job_text]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = similarity_matrix[0][0]
            
            return float(similarity_score)
        except Exception as e:
            logger.warning(f"TF-IDF calculation failed: {e}")
            return 0.0
    
    def _calculate_keyword_match(self, resume_text: str, job_text: str) -> float:
        """Calculate direct keyword matching score"""
        try:
            # Tokenize both texts
            resume_tokens = set(resume_text.lower().split())
            job_tokens = set(job_text.lower().split())
            
            if not job_tokens:
                return 0.0
            
            # Calculate overlap
            common_tokens = resume_tokens.intersection(job_tokens)
            match_ratio = len(common_tokens) / len(job_tokens)
            
            # Apply sigmoid transformation for better distribution
            # This prevents too many perfect matches
            transformed_score = 2 / (1 + np.exp(-5 * (match_ratio - 0.5)))
            
            return min(1.0, transformed_score)
        except Exception as e:
            logger.warning(f"Keyword match calculation failed: {e}")
            return 0.0
    
    def _calculate_jaccard_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate Jaccard similarity (intersection over union)"""
        try:
            resume_tokens = set(resume_text.lower().split())
            job_tokens = set(job_text.lower().split())
            
            if not resume_tokens or not job_tokens:
                return 0.0
            
            intersection = resume_tokens.intersection(job_tokens)
            union = resume_tokens.union(job_tokens)
            
            jaccard_score = len(intersection) / len(union) if union else 0.0
            
            return float(jaccard_score)
        except Exception as e:
            logger.warning(f"Jaccard similarity calculation failed: {e}")
            return 0.0
    
    def _calculate_skill_match(self, resume_text: str, job_text: str) -> float:
        """Calculate skill-specific matching score"""
        try:
            # Define comprehensive skill categories
            skills = {
                'languages': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 
                             'go', 'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala'],
                'frontend': ['react', 'angular', 'vue', 'html', 'css', 'sass', 'bootstrap',
                           'tailwind', 'jquery', 'webpack', 'babel'],
                'backend': ['node', 'express', 'django', 'flask', 'spring', 'laravel',
                          'fastapi', 'nestjs', 'rails'],
                'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle',
                            'sql', 'nosql', 'dynamodb', 'cassandra', 'elasticsearch'],
                'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
                        'terraform', 'ansible', 'heroku', 'digital ocean'],
                'tools': ['git', 'jira', 'confluence', 'postman', 'swagger', 'figma',
                        'slack', 'trello']
            }
            
            resume_lower = resume_text.lower()
            job_lower = job_text.lower()
            
            # Find skills mentioned in job description
            job_skills = []
            for category, skill_list in skills.items():
                for skill in skill_list:
                    if skill in job_lower:
                        job_skills.append(skill)
            
            if not job_skills:
                return 0.5  # Neutral score if no specific skills mentioned
            
            # Count how many job skills are in resume
            matched_skills = sum(1 for skill in job_skills if skill in resume_lower)
            
            skill_match_ratio = matched_skills / len(job_skills)
            
            return float(skill_match_ratio)
        except Exception as e:
            logger.warning(f"Skill match calculation failed: {e}")
            return 0.5
    
    def _calculate_experience_match(self, resume_text: str, job_text: str) -> float:
        """Calculate experience level matching factor"""
        try:
            resume_years = self._extract_years_experience(resume_text)
            job_years = self._extract_years_experience(job_text)
            
            if job_years == 0:
                return 1.0  # No experience requirement
            
            if resume_years == 0:
                return 0.8  # Penalty if experience not mentioned in resume
            
            # Calculate match factor
            if resume_years >= job_years:
                # Meets or exceeds requirement
                return min(1.2, 1.0 + (resume_years - job_years) * 0.02)
            else:
                # Falls short of requirement
                ratio = resume_years / job_years
                if ratio >= 0.75:  # Within 25% of requirement
                    return 0.95
                elif ratio >= 0.5:  # Within 50% of requirement
                    return 0.85
                else:
                    return 0.7  # Significantly short
        except Exception as e:
            logger.warning(f"Experience match calculation failed: {e}")
            return 1.0
    
    def _extract_years_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        try:
            patterns = [
                r'(\d+)\s*\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
                r'(\d+)\s*\+?\s*(?:years?|yrs?)',
                r'over\s+(\d+)\s*(?:years?|yrs?)',
                r'more\s+than\s+(\d+)\s*(?:years?|yrs?)',
                r'(\d+)\s*\+\s*(?:years?|yrs?)'
            ]
            
            years = []
            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                years.extend([int(match) for match in matches if match.isdigit()])
            
            return max(years) if years else 0
        except Exception as e:
            logger.warning(f"Years extraction failed: {e}")
            return 0
    
    def _get_matching_details(self, resume_text: str, job_text: str) -> dict:
        """Get detailed matching information"""
        try:
            # Tokenize
            resume_tokens = resume_text.lower().split()
            job_tokens = job_text.lower().split()
            
            # Find common tokens
            resume_set = set(resume_tokens)
            job_set = set(job_tokens)
            common_tokens = resume_set.intersection(job_set)
            
            # Get frequency of common tokens
            resume_counter = Counter(resume_tokens)
            job_counter = Counter(job_tokens)
            
            # Find top matching terms by combined frequency
            term_scores = {}
            for term in common_tokens:
                if len(term) > 2:  # Ignore very short terms
                    term_scores[term] = resume_counter[term] + job_counter[term]
            
            # Sort by score
            top_terms = sorted(term_scores.items(), key=lambda x: x[1], reverse=True)[:15]
            top_terms = [(term, int(score)) for term, score in top_terms]
            
            # Calculate match percentage
            match_percentage = (len(common_tokens) / len(job_set) * 100) if job_set else 0.0
            
            # Extract specific skills that match
            skills = ['python', 'java', 'javascript', 'react', 'node', 'angular', 'vue',
                     'django', 'flask', 'spring', 'aws', 'azure', 'docker', 'kubernetes',
                     'sql', 'mongodb', 'postgresql', 'git', 'api', 'rest']
            
            matching_skills = [skill for skill in skills 
                             if skill in resume_text.lower() and skill in job_text.lower()]
            
            return {
                'top_terms': top_terms,
                'matching_skills': matching_skills,
                'total_job_keywords': len(job_set),
                'matched_keywords': len(common_tokens),
                'match_percentage': match_percentage
            }
        except Exception as e:
            logger.warning(f"Matching details extraction failed: {e}")
            return {
                'top_terms': [],
                'matching_skills': [],
                'total_job_keywords': 0,
                'matched_keywords': 0,
                'match_percentage': 0.0
            }
