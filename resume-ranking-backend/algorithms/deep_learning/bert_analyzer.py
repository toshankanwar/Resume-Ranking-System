import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class BERTAnalyzer(BaseAlgorithm):
    """BERT-based semantic analysis for resume ranking"""
    
    def __init__(self, config: dict = None):
        super().__init__('bert', config)
        self.model_name = self.config.get('model_name', 'bert-base-uncased')
        self.max_length = self.config.get('max_length', 512)
        self.tokenizer = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def load_model(self):
        """Load BERT model and tokenizer"""
        try:
            logger.info(f"Loading BERT model: {self.model_name}")
            self.tokenizer = BertTokenizer.from_pretrained(self.model_name)
            self.model = BertModel.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            self.is_loaded = True
            logger.info("BERT model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load BERT model: {e}")
            raise
    
    def _get_embeddings(self, text: str) -> np.ndarray:
        """Get BERT embeddings for text"""
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
            # Use [CLS] token embedding
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            return embeddings
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with BERT"""
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
                    'max_length': self.max_length
                }
            }
            
        except Exception as e:
            logger.error(f"BERT processing failed: {e}")
            raise
