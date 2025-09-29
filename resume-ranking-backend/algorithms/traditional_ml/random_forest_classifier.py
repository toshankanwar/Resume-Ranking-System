from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import joblib
import os
from ..base_algorithm import BaseAlgorithm
import logging

logger = logging.getLogger(__name__)

class RandomForestClassifier(BaseAlgorithm):
    """Random Forest based resume classification and scoring"""
    
    def __init__(self, config: dict = None):
        super().__init__('random_forest', config)
        self.vectorizer = None
        self.scaler = None
        self.feature_names = None
        self.model_path = self.config.get('model_path', 'models/random_forest_model.joblib')
        
    def load_model(self):
        """Load or initialize Random Forest model"""
        try:
            if os.path.exists(self.model_path):
                logger.info("Loading pre-trained Random Forest model")
                model_data = joblib.load(self.model_path)
                self.model = model_data['model']
                self.vectorizer = model_data['vectorizer']
                self.scaler = model_data['scaler']
                self.feature_names = model_data['feature_names']
            else:
                logger.info("Initializing new Random Forest model")
                self._initialize_model()
            
            self.is_loaded = True
            logger.info("Random Forest model ready")
            
        except Exception as e:
            logger.error(f"Failed to load Random Forest model: {e}")
            raise
    
    def _initialize_model(self):
        """Initialize Random Forest model with default parameters"""
        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1
        )
        
        self.vectorizer = TfidfVectorizer(
            max_features=8000,
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
            "Senior Software Engineer with 5 years Python Django Flask experience web development",
            "Data Scientist PhD machine learning deep learning TensorFlow PyTorch statistics",
            "Frontend Developer React JavaScript TypeScript CSS HTML responsive design",
            "Backend Developer Node.js Express MongoDB PostgreSQL REST API microservices",
            "DevOps Engineer AWS Docker Kubernetes CI/CD Jenkins Terraform infrastructure automation",
            "Full Stack Developer MEAN MERN stack Angular Vue.js database design",
            "Mobile Developer iOS Swift Android Kotlin React Native Flutter cross-platform",
            "Machine Learning Engineer Python scikit-learn pandas numpy data preprocessing",
            "Product Manager Agile Scrum product roadmap stakeholder management analytics",
            "UI/UX Designer Figma Adobe Creative Suite user research wireframing prototyping"
        ]
        
        dummy_jobs = [
            "Python developer Django web applications backend systems",
            "Data Scientist machine learning models statistical analysis",
            "Frontend engineer React modern web applications",
            "Backend engineer Node.js scalable API development",
            "DevOps engineer cloud infrastructure automation",
            "Full stack developer end-to-end web applications",
            "Mobile developer iOS Android native applications",
            "ML engineer production machine learning systems",
            "Product manager feature development user experience",
            "Designer user interface user experience design"
        ]
        
        dummy_scores = [0.92, 0.88, 0.85, 0.90, 0.94, 0.87, 0.83, 0.91, 0.79, 0.86]
        
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
            ['length_ratio', 'keyword_match', 'skill_overlap', 'experience_score', 'education_score']
        )
        
        logger.info("Random Forest model initialized with dummy data")
    
    def _extract_additional_features(self, resumes: list, jobs: list) -> np.ndarray:
        """Extract additional features beyond TF-IDF"""
        features = []
        
        for resume, job in zip(resumes, jobs):
            # Length ratio feature
            length_ratio = len(resume) / max(len(job), 1)
            
            # Keyword matching
            resume_words = set(resume.lower().split())
            job_words = set(job.lower().split())
            keyword_match = len(resume_words & job_words) / max(len(job_words), 1)
            
            # Skill overlap
            tech_skills = {
                'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
                'node', 'django', 'flask', 'spring', 'express', 'mongodb', 'postgresql',
                'mysql', 'redis', 'aws', 'azure', 'docker', 'kubernetes', 'jenkins',
                'git', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'
            }
            resume_skills = set(word for word in resume_words if word in tech_skills)
            job_skills = set(word for word in job_words if word in tech_skills)
            skill_overlap = len(resume_skills & job_skills) / max(len(job_skills), 1)
            
            # Experience indicators
            experience_indicators = ['years', 'experience', 'senior', 'lead', 'manager', 'director']
            experience_score = sum(1 for word in experience_indicators if word in resume.lower()) / len(experience_indicators)
            
            # Education indicators
            education_indicators = ['degree', 'university', 'college', 'phd', 'masters', 'bachelor']
            education_score = sum(1 for word in education_indicators if word in resume.lower()) / len(education_indicators)
            
            features.append([length_ratio, keyword_match, skill_overlap, experience_score, education_score])
        
        return np.array(features)
    
    def process_single(self, resume_text: str, job_description: str, 
                      position: str = None) -> dict:
        """Process single resume with Random Forest"""
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
                self.feature_names[:15],  # Top 15 features
                self.model.feature_importances_[:15]
            ))
            
            return {
                'algorithm': self.name,
                'score': float(normalized_score),
                'raw_score': float(predicted_score),
                'details': {
                    'n_estimators': self.model.n_estimators,
                    'feature_count': len(self.feature_names),
                    'top_features': feature_importance,
                    'model_type': 'Random Forest Regressor',
                    'max_depth': self.model.max_depth
                }
            }
            
        except Exception as e:
            logger.error(f"Random Forest processing failed: {e}")
            raise
