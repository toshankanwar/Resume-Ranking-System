import torch
from transformers import XLMTokenizer, XLMModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class XLMAnalyzer(BaseAlgorithm):
    """XLM Cross-lingual model for multilingual resume analysis"""
    
    def __init__(self, config: dict = None):
        super().__init__('xlm', config)
        self.model_name = self.config.get('model_name', 'xlm-mlm-en-2048')
        self.max_length = self.config.get('max_length', 512)
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def load_model(self):
        """Load XLM model and tokenizer"""
        try:
            logger.info(f"Loading XLM model: {self.model_name}")
            self.tokenizer = XLMTokenizer.from_pretrained(self.model_name)
            self.model = XLMModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            self.is_loaded = True
            logger.info("XLM model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load XLM model: {e}")
            raise
    
    def _get_embeddings(self, text: str, lang: str = 'en') -> np.ndarray:
        """Get XLM embeddings for text"""
        with torch.no_grad():
            inputs = self.tokenizer(
                text,
                return_tensors='pt',
                max_length=self.max_length,
                truncation=True,
                padding=True
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            outputs = self.model(**inputs)
            # Use mean pooling of last hidden states
            embeddings = outputs.last_hidden_state.mean(dim=1).cpu().numpy()
            return embeddings
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with XLM"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Get embeddings
            resume_embedding = self._get_embeddings(resume_text)
            job_embedding = self._get_embeddings(job_description)
            
            # Calculate similarity
            similarity_score = cosine_similarity(resume_embedding, job_embedding)[0][0]
            
            # Normalize score to 0-1 range
            normalized_score = max(0, min(1, (similarity_score + 1) / 2))
            
            return {
                'algorithm': self.name,
                'score': float(normalized_score),
                'similarity_score': float(similarity_score),
                'details': {
                    'embedding_dimension': resume_embedding.shape[1],
                    'model_used': self.model_name,
                    'max_length': self.max_length,
                    'multilingual': True,
                    'pooling_strategy': 'mean'
                }
            }
            
        except Exception as e:
            logger.error(f"XLM processing failed: {e}")
            raise
