from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging
import re

logger = logging.getLogger(__name__)

class CosineSimilarityAnalyzer(BaseAlgorithm):
    """Enhanced TF-IDF based cosine similarity for resume ranking"""
    
    def __init__(self, config: dict = None):
        super().__init__('cosine', config)
        self.vectorizer = None
        self.max_features = self.config.get('max_features', 5000)
        self.ngram_range = self.config.get('ngram_range', (1, 3))  # Increased to trigrams
    
    def load_model(self):
        """Initialize enhanced TF-IDF vectorizer"""
        try:
            # Custom stop words - remove fewer words to preserve important terms
            custom_stop_words = [
                'the', 'is', 'at', 'which', 'on', 'and', 'or', 'but', 'in', 'with', 'to'
            ]
            
            self.vectorizer = TfidfVectorizer(
                max_features=self.max_features,
                stop_words=custom_stop_words,  # Reduced stop words
                ngram_range=self.ngram_range,  # Include trigrams
                lowercase=True,
                token_pattern=r'\b[A-Za-z]{2,}\b',
                min_df=1,  # Include terms that appear at least once
                max_df=0.9,  # Exclude terms that appear in >90% of documents
                sublinear_tf=True,  # Apply sublinear tf scaling
                norm='l2'  # L2 normalization
            )
            self.is_loaded = True
            logger.info("Enhanced Cosine similarity analyzer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize cosine similarity: {e}")
            raise
    
    def _preprocess_text(self, text: str) -> str:
        """Enhanced text preprocessing"""
        # Convert to lowercase
        text = text.lower()
        
        # Normalize common technical terms
        tech_normalizations = {
            r'\bjs\b': 'javascript',
            r'\bts\b': 'typescript', 
            r'\bml\b': 'machine learning',
            r'\bai\b': 'artificial intelligence',
            r'\bapi\b': 'application programming interface',
            r'\bsql\b': 'structured query language',
            r'\bhtml\b': 'hypertext markup language',
            r'\bcss\b': 'cascading style sheets',
            r'\baws\b': 'amazon web services',
            r'\bgcp\b': 'google cloud platform',
            r'\bui\b': 'user interface',
            r'\bux\b': 'user experience',
            r'\brest\b': 'representational state transfer',
            r'\bci/cd\b': 'continuous integration continuous deployment',
            r'\bdevops\b': 'development operations',
            r'\breactjs\b': 'react',
            r'\bnodejs\b': 'node.js',
            r'\bvuejs\b': 'vue.js',
            r'\bangularjs\b': 'angular'
        }
        
        for pattern, replacement in tech_normalizations.items():
            text = re.sub(pattern, replacement, text)
        
        # Normalize years of experience
        text = re.sub(r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)', 
                     r'\1 years experience', text)
        
        # Normalize degree mentions
        text = re.sub(r'\bb\.?s\.?\b', 'bachelor degree', text)
        text = re.sub(r'\bm\.?s\.?\b', 'master degree', text)
        text = re.sub(r'\bphd\b|\bph\.d\b', 'doctor philosophy', text)
        
        return text
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with enhanced cosine similarity"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Enhanced preprocessing
            processed_resume = self._preprocess_text(resume_text)
            processed_job = self._preprocess_text(job_description)
            
            # Create TF-IDF vectors
            documents = [processed_resume, processed_job]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            
            # Calculate cosine similarity
            similarity_matrix = cosine_similarity(tfidf_matrix)
            similarity_score = similarity_matrix[0][1]
            
            # Apply boost factors for better scoring
            boost_factor = self._calculate_boost_factor(processed_resume, processed_job)
            boosted_score = min(1.0, similarity_score * boost_factor)
            
            # Get matching term analysis
            feature_names = self.vectorizer.get_feature_names_out()
            resume_vector = tfidf_matrix[0].toarray()[0]
            job_vector = tfidf_matrix[1].toarray()[0]
            
            # Find top contributing terms
            term_contributions = resume_vector * job_vector
            top_indices = np.argsort(term_contributions)[-15:][::-1]
            top_terms = [(feature_names[i], float(term_contributions[i])) 
                        for i in top_indices if term_contributions[i] > 0]
            
            return {
                'algorithm': self.name,
                'score': max(0.1, float(boosted_score)),  # Minimum score of 0.1
                'raw_similarity': float(similarity_score),
                'boost_factor': float(boost_factor),
                'details': {
                    'total_features': len(feature_names),
                    'resume_terms': int(np.sum(resume_vector > 0)),
                    'job_terms': int(np.sum(job_vector > 0)),
                    'matching_terms': len(top_terms),
                    'top_matching_terms': top_terms,
                    'ngram_range': self.ngram_range,
                    'preprocessing_applied': True
                }
            }
            
        except Exception as e:
            logger.error(f"Enhanced cosine similarity processing failed: {e}")
            raise
    
    def _calculate_boost_factor(self, resume_text: str, job_text: str) -> float:
        """Calculate boost factor based on keyword density and matching"""
        
        # Key technical skills that should boost score
        high_value_terms = [
            'python', 'java', 'javascript', 'react', 'node.js', 'angular', 'vue',
            'django', 'flask', 'spring', 'express', 'mongodb', 'mysql', 'postgresql',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'jenkins', 'tensorflow',
            'machine learning', 'data science', 'artificial intelligence',
            'full stack', 'backend', 'frontend', 'api', 'microservices'
        ]
        
        resume_words = set(resume_text.lower().split())
        job_words = set(job_text.lower().split())
        
        # Calculate high-value term matches
        resume_high_value = sum(1 for term in high_value_terms 
                               if any(word in resume_text.lower() for word in term.split()))
        job_high_value = sum(1 for term in high_value_terms 
                            if any(word in job_text.lower() for word in term.split()))
        
        # Calculate boost based on high-value matches
        if job_high_value > 0:
            high_value_ratio = resume_high_value / job_high_value
            boost = 1.0 + (high_value_ratio * 0.5)  # Up to 50% boost
        else:
            boost = 1.0
        
        # Additional boost for exact phrase matches
        job_phrases = [phrase.strip() for phrase in job_text.split(',')]
        phrase_matches = sum(1 for phrase in job_phrases[:10] 
                           if len(phrase) > 3 and phrase.lower() in resume_text.lower())
        
        if len(job_phrases[:10]) > 0:
            phrase_boost = 1.0 + (phrase_matches / len(job_phrases[:10]) * 0.3)
        else:
            phrase_boost = 1.0
        
        # Experience level matching
        experience_boost = self._calculate_experience_boost(resume_text, job_text)
        
        final_boost = boost * phrase_boost * experience_boost
        return min(2.0, final_boost)  # Cap at 2x boost
    
    def _calculate_experience_boost(self, resume_text: str, job_text: str) -> float:
        """Calculate boost based on experience level matching"""
        
        # Extract years of experience from both texts
        resume_years = self._extract_years_experience(resume_text)
        job_years = self._extract_years_experience(job_text)
        
        if resume_years > 0 and job_years > 0:
            if resume_years >= job_years:
                return 1.2  # 20% boost for meeting experience requirement
            elif resume_years >= job_years * 0.8:
                return 1.1  # 10% boost for close to requirement
            else:
                return 0.9  # Slight penalty for insufficient experience
        
        return 1.0  # No change if experience not clearly stated
    
    def _extract_years_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        import re
        
        patterns = [
            r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\s*(?:\+)?\s*(?:years?|yrs?)',
            r'over\s*(\d+)\s*(?:years?|yrs?)',
            r'more\s*than\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(match) for match in matches])
        
        return max(years) if years else 0
