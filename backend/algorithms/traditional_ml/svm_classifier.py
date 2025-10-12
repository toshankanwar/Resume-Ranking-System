from sklearn.svm import SVR
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
import joblib
import os
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class SVMClassifier(BaseAlgorithm):
    """Support Vector Machine based resume classification and scoring"""
    
    def __init__(self, config: dict = None):
        super().__init__('svm', config)
        self.vectorizer = None
        self.scaler = None
        self.model_path = self.config.get('model_path', 'models/svm_model.joblib')
        
    def load_model(self):
        """Load or initialize SVM model"""
        try:
            if os.path.exists(self.model_path):
                logger.info("Loading pre-trained SVM model")
                self.model = joblib.load(self.model_path)
            else:
                logger.info("Initializing new SVM model")
                self._initialize_model()
            
            self.is_loaded = True
            logger.info("SVM model ready")
            
        except Exception as e:
            logger.error(f"Failed to load SVM model: {e}")
            raise
    
    def _initialize_model(self):
        """Initialize SVM model with pipeline"""
        
        # Create pipeline with preprocessing and SVM
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.9
            )),
            ('scaler', StandardScaler(with_mean=False)),  # with_mean=False for sparse matrices
            ('svm', SVR(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                epsilon=0.1
            ))
        ])
        
        # Create dummy training data
        self._create_dummy_training_data()
    
    def _create_dummy_training_data(self):
        """Create dummy training data for model initialization"""
        dummy_data = [
            ("Software Engineer Python Django Flask web development REST API", 
             "Python developer web applications Django", 0.88),
            ("Data Scientist machine learning deep learning TensorFlow PyTorch", 
             "Data scientist ML models Python", 0.92),
            ("Frontend Developer React JavaScript TypeScript HTML CSS", 
             "Frontend engineer React applications", 0.85),
            ("Backend Developer Node.js Express MongoDB database design", 
             "Backend developer Node.js APIs", 0.87),
            ("DevOps Engineer AWS Docker Kubernetes infrastructure automation", 
             "DevOps engineer cloud AWS Docker", 0.91),
            ("Full Stack Developer MEAN stack Angular Node.js MongoDB", 
             "Full stack developer web applications", 0.84),
            ("Mobile Developer iOS Swift Android Kotlin React Native", 
             "Mobile developer iOS Android apps", 0.89),
            ("Machine Learning Engineer Python scikit-learn data analysis", 
             "ML engineer production systems", 0.90),
            ("Product Manager Agile Scrum product development analytics", 
             "Product manager feature development", 0.78),
            ("UI/UX Designer Figma Adobe user interface design", 
             "Designer user experience interface", 0.82)
        ]
        
        # Prepare training data
        combined_texts = [f"{resume} {job}" for resume, job, _ in dummy_data]
        scores = [score for _, _, score in dummy_data]
        
        # Train the pipeline
        self.model.fit(combined_texts, scores)
        
        logger.info("SVM model initialized with dummy data")
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with SVM"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Create combined text
            combined_text = f"{resume_text} {job_description}"
            
            # Predict score using the pipeline
            predicted_score = self.model.predict([combined_text])[0]
            
            # Normalize to 0-1 range
            normalized_score = max(0, min(1, predicted_score))
            
            # Get some feature information from the pipeline
            tfidf_vectorizer = self.model.named_steps['tfidf']
            feature_names = tfidf_vectorizer.get_feature_names_out()
            
            return {
                'algorithm': self.name,
                'score': float(normalized_score),
                'raw_score': float(predicted_score),
                'details': {
                    'kernel': self.model.named_steps['svm'].kernel,
                    'feature_count': len(feature_names),
                    'model_type': 'Support Vector Regression',
                    'C_parameter': self.model.named_steps['svm'].C,
                    'gamma': self.model.named_steps['svm'].gamma
                }
            }
            
        except Exception as e:
            logger.error(f"SVM processing failed: {e}")
            raise
