from sklearn.neural_network import MLPRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
import os
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class NeuralNetworkClassifier(BaseAlgorithm):
    """Multi-layer Perceptron Neural Network for resume scoring"""
    
    def __init__(self, config: dict = None):
        super().__init__('neural_network', config)
        self.vectorizer = None
        self.scaler = None
        self.model_path = self.config.get('model_path', 'models/neural_network_model.joblib')
        
    def load_model(self):
        """Load or initialize Neural Network model"""
        try:
            if os.path.exists(self.model_path):
                logger.info("Loading pre-trained Neural Network model")
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.vectorizer = model_data['vectorizer']
                self.scaler = model_data['scaler']
            else:
                logger.info("Initializing new Neural Network model")
                self._initialize_model()
            
            self.is_loaded = True
            logger.info("Neural Network model ready")
            
        except Exception as e:
            logger.error(f"Failed to load Neural Network model: {e}")
            raise
    
    def _initialize_model(self):
        """Initialize Neural Network model"""
        self.model = MLPRegressor(
            hidden_layer_sizes=(256, 128, 64),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='constant',
            learning_rate_init=0.001,
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=10
        )
        
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words='english',
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.95
        )
        
        self.scaler = StandardScaler()
        
        # Create dummy training data
        self._create_dummy_training_data()
    
    def _create_dummy_training_data(self):
        """Create dummy training data for model initialization"""
        dummy_resumes = [
            "Senior Software Engineer 7 years experience Python Django Flask REST API PostgreSQL Redis AWS",
            "Data Scientist PhD machine learning deep learning TensorFlow PyTorch scikit-learn pandas numpy",
            "Frontend Developer 4 years React JavaScript TypeScript HTML5 CSS3 responsive design webpack",
            "Backend Developer Node.js Express.js MongoDB MySQL microservices Docker Kubernetes",
            "DevOps Engineer infrastructure automation AWS EC2 S3 Lambda Jenkins CI/CD Terraform Ansible",
            "Full Stack Developer MERN stack React Node.js MongoDB Express Angular Vue.js",
            "iOS Developer Swift Objective-C Xcode Core Data UIKit SwiftUI App Store",
            "Android Developer Kotlin Java Android Studio Room Retrofit Dagger MVVM",
            "Machine Learning Engineer Python R scikit-learn TensorFlow model deployment MLOps",
            "Product Manager 5 years Agile Scrum product roadmap stakeholder management analytics KPIs",
            "UI/UX Designer Figma Sketch Adobe XD user research wireframing prototyping usability testing",
            "QA Engineer automation testing Selenium WebDriver TestNG JUnit Python Java",
            "Security Engineer cybersecurity penetration testing OWASP vulnerability assessment compliance",
            "Database Administrator MySQL PostgreSQL Oracle performance tuning backup recovery optimization"
        ]
        
        dummy_jobs = [
            "Python developer web applications Django Flask",
            "Data Scientist machine learning Python R",
            "Frontend React JavaScript modern web apps",
            "Backend Node.js scalable API development",
            "DevOps cloud infrastructure AWS automation",
            "Full stack web application development",
            "iOS mobile app development Swift",
            "Android app development Kotlin Java",
            "ML engineer production machine learning",
            "Product manager feature development",
            "Designer user experience interface design",
            "QA automation testing frameworks",
            "Security engineer cybersecurity testing",
            "Database administrator performance optimization"
        ]
        
        dummy_scores = [0.93, 0.90, 0.87, 0.89, 0.92, 0.85, 0.88, 0.86, 0.91, 0.81, 0.83, 0.84, 0.87, 0.89]
        
        # Create features
        combined_texts = [f"{resume} {job}" for resume, job in zip(dummy_resumes, dummy_jobs)]
        tfidf_features = self.vectorizer.fit_transform(combined_texts)
        
        # Scale features
        features_scaled = self.scaler.fit_transform(tfidf_features.toarray())
        
        # Train model
        self.model.fit(features_scaled, dummy_scores)
        
        logger.info(f"Neural Network model initialized - Loss: {self.model.loss_:.4f}")
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with Neural Network"""
        if not self.is_loaded:
            self.load_model()
        
        try:
            # Create combined text for TF-IDF
            combined_text = f"{resume_text} {job_description}"
            tfidf_features = self.vectorizer.transform([combined_text])
            
            # Scale features
            features_scaled = self.scaler.transform(tfidf_features.toarray())
            
            # Predict score
            predicted_score = self.model.predict(features_scaled)[0]
            
            # Normalize to 0-1 range
            normalized_score = max(0, min(1, predicted_score))
            
            return {
                'algorithm': self.name,
                'score': float(normalized_score),
                'raw_score': float(predicted_score),
                'details': {
                    'hidden_layers': self.model.hidden_layer_sizes,
                    'n_features': tfidf_features.shape[1],
                    'activation': self.model.activation,
                    'solver': self.model.solver,
                    'n_iter': getattr(self.model, 'n_iter_', 0),
                    'loss': getattr(self.model, 'loss_', 0),
                    'model_type': 'Multi-layer Perceptron'
                }
            }
            
        except Exception as e:
            logger.error(f"Neural Network processing failed: {e}")
            raise
