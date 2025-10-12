import re
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging
from collections import Counter
import math

logger = logging.getLogger(__name__)


class JaccardSimilarityAnalyzer(BaseAlgorithm):
    """
    BM25 (Best Matching 25) Ranking Algorithm
    
    COMPLETELY DIFFERENT from TF-IDF and Jaccard:
    - TF-IDF: Linear term frequency
    - Jaccard: Set-based intersection/union
    - BM25: Probabilistic ranking with saturation
    
    Used by: Elasticsearch, Lucene, search engines
    Better handles: term saturation, document length normalization
    """
    
    def __init__(self, config: dict = None):
        super().__init__('jaccard', config)  # Keep name for compatibility
        # BM25 parameters
        self.k1 = 1.5  # Term saturation parameter (1.2-2.0)
        self.b = 0.75  # Document length normalization (0-1)
        self.tech_skills = self._load_tech_skills()
    
    def _load_tech_skills(self) -> set:
        """Load technical skills for boosting"""
        return {
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'nodejs', 'django', 'flask', 'spring', 'aws', 'azure', 'docker',
            'kubernetes', 'mongodb', 'postgresql', 'mysql', 'redis', 'git'
        }
    
    def load_model(self):
        self.is_loaded = True
        logger.info("BM25 ranking algorithm initialized")
    
    def _tokenize(self, text: str) -> list:
        """Tokenize text into terms"""
        # Convert to lowercase and extract words
        text = text.lower()
        # Keep alphanumeric and common tech separators
        text = re.sub(r'[^\w\s\-\+\.]', ' ', text)
        tokens = text.split()
        
        # Remove very short tokens
        tokens = [t for t in tokens if len(t) > 2]
        
        return tokens
    
    def _compute_idf(self, term: str, doc_count: int, term_doc_freq: int) -> float:
        """
        Compute IDF (Inverse Document Frequency) for BM25
        Different from TF-IDF's IDF formula
        """
        # BM25 IDF formula
        idf = math.log((doc_count - term_doc_freq + 0.5) / (term_doc_freq + 0.5) + 1.0)
        return max(0.0, idf)  # Ensure non-negative
    
    def _compute_bm25_score(self, term_freq: int, doc_length: int, 
                           avg_doc_length: float, idf: float) -> float:
        """
        Compute BM25 score for a term
        
        BM25 formula:
        score = IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_len / avg_doc_len)))
        """
        # Term frequency saturation
        numerator = term_freq * (self.k1 + 1)
        
        # Document length normalization
        denominator = term_freq + self.k1 * (1 - self.b + self.b * (doc_length / avg_doc_length))
        
        # Final BM25 score
        score = idf * (numerator / denominator)
        
        return score
    
    def _extract_n_grams(self, tokens: list, n: int = 2) -> list:
        """Extract n-grams for phrase matching"""
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngram = ' '.join(tokens[i:i+n])
            ngrams.append(ngram)
        return ngrams
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Rank resume using BM25 algorithm"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Tokenize both documents
            resume_tokens = self._tokenize(resume_text)
            job_tokens = self._tokenize(job_description)
            
            # Extract bigrams (2-word phrases)
            resume_bigrams = self._extract_n_grams(resume_tokens, 2)
            job_bigrams = self._extract_n_grams(job_tokens, 2)
            
            # Combine unigrams and bigrams
            resume_terms = resume_tokens + resume_bigrams
            job_terms = job_tokens + job_bigrams
            
            # Calculate document lengths
            resume_length = len(resume_terms)
            job_length = len(job_terms)
            avg_length = (resume_length + job_length) / 2
            
            # Count term frequencies in resume
            resume_term_freq = Counter(resume_terms)
            job_term_freq = Counter(job_terms)
            
            # Get unique query terms from job description
            query_terms = set(job_terms)
            
            # Calculate BM25 scores for each query term
            total_bm25_score = 0.0
            term_scores = {}
            matched_terms = []
            
            # For IDF calculation, treat resume and job as corpus of 2 docs
            doc_count = 2
            
            for term in query_terms:
                # Check if term appears in resume
                if term in resume_term_freq:
                    # Term document frequency (in how many docs does term appear)
                    term_doc_freq = 1  # Appears in at least job description
                    if term in resume_term_freq:
                        term_doc_freq = 2  # Appears in both
                    
                    # Compute IDF
                    idf = self._compute_idf(term, doc_count, term_doc_freq)
                    
                    # Compute BM25 score for this term
                    tf = resume_term_freq[term]
                    bm25_term_score = self._compute_bm25_score(
                        tf, resume_length, avg_length, idf
                    )
                    
                    # Apply skill boosting (technical terms get higher weight)
                    if term in self.tech_skills:
                        bm25_term_score *= 1.5  # 50% boost for tech skills
                    
                    total_bm25_score += bm25_term_score
                    term_scores[term] = bm25_term_score
                    
                    matched_terms.append(term)
            
            # Normalize BM25 score to 0-1 range
            # BM25 scores can theoretically be unbounded, but typically 0-100
            # We'll use a sigmoid-like transformation
            max_possible_score = len(query_terms) * 10  # Rough estimate
            normalized_score = total_bm25_score / max_possible_score if max_possible_score > 0 else 0
            
            # Apply additional factors for better differentiation
            
            # 1. Coverage factor (what % of job terms are in resume)
            coverage = len(matched_terms) / len(query_terms) if query_terms else 0
            
            # 2. Term importance factor (rare terms matter more)
            rare_term_bonus = 0.0
            for term in matched_terms:
                if len(term) > 8:  # Long terms are usually more specific
                    rare_term_bonus += 0.01
            
            # 3. Exact phrase matching bonus
            exact_phrases = set(job_bigrams) & set(resume_bigrams)
            phrase_bonus = min(0.15, len(exact_phrases) * 0.02)
            
            # Combined final score
            base_score = normalized_score * 0.60 + coverage * 0.40
            final_score = base_score + rare_term_bonus + phrase_bonus
            
            # Ensure score is in valid range
            final_score = max(0.10, min(0.95, final_score))
            
            # Sort terms by BM25 score to show most important matches
            top_terms = sorted(term_scores.items(), key=lambda x: x[1], reverse=True)[:10]
            
            logger.info(f"BM25 - Raw:{total_bm25_score:.2f}, Normalized:{normalized_score:.2f}, "
                       f"Coverage:{coverage:.2f}, Phrases:{len(exact_phrases)}, "
                       f"Final:{final_score:.2f}")
            
            return {
                'algorithm': self.name,
                'score': float(final_score),
                'details': {
                    'algorithm_type': 'BM25 (Best Matching 25)',
                    'raw_bm25_score': total_bm25_score,
                    'normalized_bm25': normalized_score,
                    'coverage_ratio': coverage,
                    'parameters': {
                        'k1': self.k1,
                        'b': self.b,
                        'doc_count': doc_count
                    },
                    'statistics': {
                        'resume_length': resume_length,
                        'job_length': job_length,
                        'avg_length': avg_length,
                        'unique_query_terms': len(query_terms),
                        'matched_terms': len(matched_terms),
                        'exact_phrase_matches': len(exact_phrases)
                    },
                    'top_matching_terms': [
                        {'term': term, 'bm25_score': float(score)} 
                        for term, score in top_terms
                    ],
                    'bonuses': {
                        'rare_term_bonus': rare_term_bonus,
                        'phrase_bonus': phrase_bonus
                    },
                    'scoring_breakdown': {
                        'bm25_component': normalized_score * 0.60,
                        'coverage_component': coverage * 0.40,
                        'bonuses': rare_term_bonus + phrase_bonus
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"BM25 ranking failed: {e}", exc_info=True)
            return {'algorithm': self.name, 'score': 0.0, 'details': {'error': str(e)}}
