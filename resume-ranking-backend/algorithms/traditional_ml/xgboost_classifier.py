import xgboost as xgb
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class XGBoostClassifier(BaseAlgorithm):
    """XGBoost-based resume classification and scoring"""
    
    def __init__(self, config: dict = None):
        super().__init__('xgboost', config)
        self.vectorizer = None
        self.scaler = None
        self.feature_names = None
        self.model_path = self.config.get('model_path', 'models/xgboost_model.joblib')
        
    def load_model(self):
        """Load or initialize XGBoost model"""
        try:
            if os.path.exists(self.model_path):
                logger.info("Loading pre-trained XGBoost model")
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.vectorizer = model_data['vectorizer']
                self.scaler = model_data['scaler']
                self.feature_names = model_data['feature_names']
            else:
                logger.info("Initializing new XGBoost model")
                self._initialize_model()
            
            self.is_loaded = True
            logger.info("XGBoost model ready")
            
        except Exception as e:
            logger.error(f"Failed to load XGBoost model: {e}")
            raise
    
    def _initialize_model(self):
        """Initialize XGBoost model with default parameters"""
        self.model = xgb.XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.scaler = StandardScaler()
        
        # Create dummy training data for initialization
        self._create_dummy_training_data()
    
    def _create_dummy_training_data(self):
        """Create dummy training data for model initialization"""
        # This would be replaced with actual training data in production
        dummy_resumes = [
            "Software Engineer with Python Django Flask experience",
            "Data Scientist with machine learning deep learning skills", 
            "Frontend Developer React JavaScript TypeScript experience",
            "Backend Developer Node.js Express MongoDB database",
            "DevOps Engineer AWS Docker Kubernetes infrastructure"
        ]
        
        dummy_jobs = [
            "Looking for Python developer with Django experience",
            "Seeking Data Scientist with ML expertise",
            "Frontend position requiring React skills",
            "Backend role using Node.js and databases", 
            "DevOps position with cloud experience"
        ]
        
        dummy_scores = [0.9, 0.85, 0.8, 0.88, 0.92]
        
        # Create features
        combined_texts = [f"{resume} {job}" for resume, job in zip(dummy_resumes, dummy_jobs)]
        tfidf_features = self.vectorizer.fit_transform(combined_texts)
        
        # Additional features
        additional_features = self._extract_additional_features(dummy_resumes, dummy_jobs)
        
        # Combine features
        features = np.hstack([tfidf_features.toarray(), additional_features])
        features_scaled = self.scaler.fit_transform(features)
        
        # Train model
        self.model.fit(features_scaled, dummy_scores)
        
        self.feature_names = (
            list(self.vectorizer.get_feature_names_out()) + 
            ['length_ratio', 'keyword_match', 'skill_overlap']
        )
        
        logger.info("XGBoost model initialized with dummy data")
    
    def _extract_additional_features(self, resumes: list, jobs: list) -> np.ndarray:
        """Extract additional features beyond TF-IDF"""
        features = []
        
        for resume, job in zip(resumes, jobs):
            # Length ratio feature
            length_ratio = len(resume) / max(len(job), 1)
            
            # Simple keyword matching
            resume_words = set(resume.lower().split())
            job_words = set(job.lower().split())
            keyword_match = len(resume_words & job_words) / max(len(job_words), 1)
            
            # Skill overlap (simplified)
            common_skills = ['python', 'java', 'javascript', 'react', 'node', 'aws', 'docker']
            resume_skills = set(skill for skill in common_skills if skill in resume.lower())
            job_skills = set(skill for skill in common_skills if skill in job.lower())
            skill_overlap = len(resume_skills & job_skills) / max(len(job_skills), 1)
            
            features.append([length_ratio, keyword_match, skill_overlap])
        
        return np.array(features)
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with XGBoost"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Create combined text for TF-IDF
            combined_text = f"{resume_text} {job_description}"
            tfidf_features = self.vectorizer.transform([combined_text])
            
            # Extract additional features
            additional_features = self._extract_additional_features([resume_text], [job_description])
            
            # Combine features
            features = np.hstack([tfidf_features.toarray(), additional_features])
            features_scaled = self.scaler.transform(features)
            
            # Predict score
            predicted_score = self.model.predict(features_scaled)[0]
            
            # Normalize to 0-1 range
            normalized_score = max(0, min(1, predicted_score))
            
            # Get feature importance
            feature_importance = dict(zip(
                self.feature_names[:10],  # Top 10 features
                self.model.feature_importances_[:10]
            ))
            
            return {
                'algorithm': self.name,
                'score': float(normalized_score),
                'raw_score': float(predicted_score),
                'details': {
                    'feature_count': len(self.feature_names),
                    'top_features': feature_importance,
                    'model_type': 'XGBoost Regressor'
                }
            }
            
        except Exception as e:
            logger.error(f"XGBoost processing failed: {e}")
            raise
