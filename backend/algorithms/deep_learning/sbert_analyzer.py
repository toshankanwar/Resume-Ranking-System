from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class SBERTAnalyzer(BaseAlgorithm):
    """Sentence-BERT based semantic analysis for resume ranking"""
    
    def __init__(self, config: dict = None):
        super().__init__('sbert', config)
        self.model_name = self.config.get('model_name', 'all-MiniLM-L6-v2')
        
    def load_model(self):
        """Load S-BERT model"""
        try:
            logger.info(f"Loading S-BERT model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.is_loaded = True
            logger.info("S-BERT model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load S-BERT model: {e}")
            raise
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with S-BERT"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Get sentence embeddings
            texts = [resume_text, job_description]
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            
            # Calculate cosine similarity
            similarity_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            # S-BERT already produces normalized embeddings, so similarity is already in reasonable range
            normalized_score = max(0, min(1, float(similarity_score)))
            
            return {
                'algorithm': self.name,
                'score': normalized_score,
                'similarity_score': float(similarity_score),
                'details': {
                    'embedding_dimension': len(embeddings[0]),
                    'model_used': self.model_name,
                    'sentence_optimized': True,
                    'max_seq_length': self.model.get_max_seq_length()
                }
            }
            
        except Exception as e:
            logger.error(f"S-BERT processing failed: {e}")
            raise
