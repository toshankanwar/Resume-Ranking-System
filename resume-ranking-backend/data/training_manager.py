import pandas as pd
import json
import os
import logging
from typing import List, Dict, Any, Tuple
from datetime import datetime
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

logger = logging.getLogger(__name__)

class TrainingDataManager:
    """Manages real resume training data for academic evaluation"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.data_dir = self.config.get('data_dir', 'data')
        self.training_file = os.path.join(self.data_dir, 'training_data.json')
        self.models_dir = self.config.get('models_dir', 'models')
        
        # Create directories
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        self.training_data = self._load_training_data()
    
    def add_resume_data(self, resume_text: str, job_description: str, 
                       manual_score: float, position: str, 
                       evaluator: str = "human") -> str:
        """Add manually scored resume data for training"""
        
        data_entry = {
            'id': f"entry_{len(self.training_data) + 1}_{int(datetime.now().timestamp())}",
            'resume_text': resume_text,
            'job_description': job_description,
            'position': position,
            'manual_score': float(manual_score),  # Ground truth score (0-1)
            'evaluator': evaluator,
            'added_at': datetime.now().isoformat(),
            'word_count': len(resume_text.split()),
            'char_count': len(resume_text)
        }
        
        self.training_data.append(data_entry)
        self._save_training_data()
        
        logger.info(f"Added training entry {data_entry['id']} with score {manual_score}")
        return data_entry['id']
    
    def bulk_import_csv(self, csv_path: str) -> int:
        """Import training data from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            required_columns = ['resume_text', 'job_description', 'manual_score', 'position']
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"CSV must contain columns: {required_columns}")
            
            imported_count = 0
            for _, row in df.iterrows():
                try:
                    self.add_resume_data(
                        resume_text=row['resume_text'],
                        job_description=row['job_description'],
                        manual_score=float(row['manual_score']),
                        position=row['position'],
                        evaluator=row.get('evaluator', 'csv_import')
                    )
                    imported_count += 1
                except Exception as e:
                    logger.error(f"Failed to import row: {e}")
                    continue
            
            return imported_count
            
        except Exception as e:
            logger.error(f"CSV import failed: {e}")
            raise
    
    def get_training_dataset(self, position: str = None, 
                           min_samples: int = 10) -> Tuple[List[str], List[str], List[float]]:
        """Get training dataset for specified position"""
        
        filtered_data = self.training_data
        if position:
            filtered_data = [d for d in self.training_data if d['position'] == position]
        
        if len(filtered_data) < min_samples:
            logger.warning(f"Insufficient training data: {len(filtered_data)} < {min_samples}")
            # Return default enhanced training data
            return self._get_enhanced_default_training_data(position)
        
        resumes = [d['resume_text'] for d in filtered_data]
        jobs = [d['job_description'] for d in filtered_data]
        scores = [d['manual_score'] for d in filtered_data]
        
        return resumes, jobs, scores
    
    def _get_enhanced_default_training_data(self, position: str = None) -> Tuple[List[str], List[str], List[float]]:
        """Enhanced default training data with realistic resume examples"""
        
        training_examples = [
            {
                'resume': """
                John Smith - Senior Full Stack Developer
                
                PROFESSIONAL EXPERIENCE:
                Senior Full Stack Developer - TechCorp Inc. (2019-2024)
                • Developed and maintained 15+ web applications using React, Node.js, and MongoDB
                • Led a team of 4 junior developers in Agile development environment
                • Implemented microservices architecture reducing system downtime by 40%
                • Deployed applications on AWS using Docker and Kubernetes
                • Collaborated with product managers and designers to deliver user-centric solutions
                
                Full Stack Developer - StartupXYZ (2017-2019)
                • Built responsive web applications using Vue.js and Express.js
                • Designed and optimized PostgreSQL databases for high-performance queries
                • Integrated third-party APIs and payment gateways
                • Implemented automated testing reducing bugs by 60%
                
                TECHNICAL SKILLS:
                Frontend: React, Vue.js, Angular, JavaScript, TypeScript, HTML5, CSS3, SASS
                Backend: Node.js, Express.js, Django, Flask, Spring Boot
                Databases: MongoDB, PostgreSQL, MySQL, Redis
                Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Git
                Testing: Jest, Mocha, Selenium, Unit Testing, Integration Testing
                
                EDUCATION:
                Bachelor of Science in Computer Science - University of Technology (2017)
                
                PROJECTS:
                • E-commerce Platform: Built scalable platform handling 10k+ concurrent users
                • Real-time Chat Application: Implemented WebSocket-based chat with file sharing
                • Task Management System: Created project management tool with advanced analytics
                """,
                'job': """
                Senior Full Stack Developer Position
                
                We are seeking an experienced Full Stack Developer to join our growing team.
                
                REQUIRED QUALIFICATIONS:
                • 4+ years of experience in full stack web development
                • Strong proficiency in JavaScript, React, and Node.js
                • Experience with modern databases (MongoDB, PostgreSQL)
                • Knowledge of cloud platforms (AWS, Azure)
                • Experience with version control (Git) and Agile methodologies
                • Bachelor's degree in Computer Science or related field
                
                RESPONSIBILITIES:
                • Design and develop scalable web applications
                • Collaborate with cross-functional teams
                • Implement best practices for code quality and testing
                • Deploy and maintain applications in cloud environments
                • Mentor junior developers
                
                PREFERRED QUALIFICATIONS:
                • Experience with microservices architecture
                • Knowledge of Docker and Kubernetes
                • Experience with automated testing and CI/CD
                • Leadership experience
                """,
                'score': 0.92,
                'position': 'fullstack'
            },
            {
                'resume': """
                Sarah Johnson - Frontend Developer
                
                EXPERIENCE:
                Frontend Developer - WebSolutions Ltd (2021-2024)
                • Developed responsive user interfaces using React and TypeScript
                • Collaborated with UX/UI designers to implement pixel-perfect designs
                • Optimized applications for performance and accessibility
                • Maintained component library used across 5+ projects
                
                Junior Web Developer - DigitalAgency (2020-2021)
                • Created landing pages and marketing websites using HTML, CSS, JavaScript
                • Worked with WordPress and custom CMS solutions
                • Assisted in mobile-first responsive design implementation
                
                SKILLS:
                HTML5, CSS3, JavaScript, TypeScript, React, Vue.js, SASS, Webpack, Git
                
                EDUCATION:
                Associate Degree in Web Development (2020)
                """,
                'job': """
                Senior Full Stack Developer Position
                
                REQUIRED:
                • 4+ years full stack development experience
                • Backend development with Node.js, Python, or Java
                • Database design and optimization
                • Cloud platform experience
                • Team leadership experience
                """,
                'score': 0.45,  # Low score - missing backend and senior experience
                'position': 'fullstack'
            },
            {
                'resume': """
                Michael Chen - Data Scientist
                
                EXPERIENCE:
                Senior Data Scientist - DataTech Corp (2020-2024)
                • Developed machine learning models for predictive analytics
                • Implemented deep learning solutions using TensorFlow and PyTorch
                • Built data pipelines processing 1M+ records daily
                • Led data science team of 6 members
                
                TECHNICAL SKILLS:
                Python, R, SQL, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy
                AWS, Docker, Jupyter, Git, Statistical Analysis, Deep Learning
                
                EDUCATION:
                PhD in Data Science - Stanford University (2020)
                Master's in Statistics - MIT (2017)
                """,
                'job': """
                Senior Full Stack Developer Position
                
                REQUIRED:
                • 4+ years full stack web development
                • JavaScript, React, Node.js
                • Database and cloud experience
                """,
                'score': 0.25,  # Very low - completely different field
                'position': 'fullstack'
            },
            {
                'resume': """
                Alex Rodriguez - Junior Full Stack Developer
                
                EXPERIENCE:
                Junior Full Stack Developer - TechStart (2023-2024)
                • Developed web applications using React and Node.js
                • Worked with MongoDB and Express.js
                • Participated in Agile development processes
                • Created RESTful APIs and integrated third-party services
                
                Intern - CodeCamp (2023)
                • Built personal projects using HTML, CSS, JavaScript
                • Learned React, Node.js through intensive bootcamp
                • Completed full stack web development certification
                
                SKILLS:
                JavaScript, React, Node.js, Express, MongoDB, HTML, CSS, Git
                
                EDUCATION:
                Full Stack Web Development Bootcamp (2023)
                Bachelor's in Business Administration (2022)
                """,
                'job': """
                Senior Full Stack Developer Position
                
                REQUIRED:
                • 4+ years full stack development experience
                • Leadership and mentoring experience
                • Advanced knowledge of system architecture
                • Experience with multiple technology stacks
                """,
                'score': 0.35,  # Low due to lack of senior experience
                'position': 'fullstack'
            }
        ]
        
        # Add more examples for different positions
        if position == 'data_scientist':
            training_examples.extend([
                {
                    'resume': """
                    Dr. Emily Watson - Senior Data Scientist
                    
                    EXPERIENCE:
                    Senior Data Scientist - AI Research Lab (2019-2024)
                    • Led machine learning projects with $2M+ budget
                    • Published 15+ research papers in top-tier journals
                    • Developed recommendation systems serving 100M+ users
                    • Built end-to-end ML pipelines on AWS and GCP
                    
                    SKILLS:
                    Python, R, TensorFlow, PyTorch, Scikit-learn, Pandas, NumPy, SQL
                    AWS, GCP, Docker, Kubernetes, MLflow, Apache Spark
                    
                    EDUCATION:
                    PhD in Machine Learning - Carnegie Mellon (2019)
                    """,
                    'job': """
                    Senior Data Scientist Position
                    • PhD in ML/AI or 5+ years experience
                    • Deep learning expertise
                    • Production ML systems experience
                    """,
                    'score': 0.95,
                    'position': 'data_scientist'
                }
            ])
        
        resumes = [ex['resume'] for ex in training_examples]
        jobs = [ex['job'] for ex in training_examples]
        scores = [ex['score'] for ex in training_examples]
        
        return resumes, jobs, scores
    
    def _load_training_data(self) -> List[Dict]:
        """Load training data from file"""
        if os.path.exists(self.training_file):
            try:
                with open(self.training_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load training data: {e}")
                return []
        return []
    
    def _save_training_data(self):
        """Save training data to file"""
        try:
            with open(self.training_file, 'w') as f:
                json.dump(self.training_data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save training data: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get training data statistics"""
        if not self.training_data:
            return {'total_samples': 0, 'positions': {}}
        
        positions = {}
        for entry in self.training_data:
            pos = entry['position']
            if pos not in positions:
                positions[pos] = {'count': 0, 'scores': []}
            positions[pos]['count'] += 1
            positions[pos]['scores'].append(entry['manual_score'])
        
        # Calculate statistics for each position
        for pos, data in positions.items():
            scores = data['scores']
            data.update({
                'avg_score': np.mean(scores),
                'std_score': np.std(scores),
                'min_score': np.min(scores),
                'max_score': np.max(scores)
            })
        
        return {
            'total_samples': len(self.training_data),
            'positions': positions,
            'data_quality': self._assess_data_quality()
        }
    
    def _assess_data_quality(self) -> Dict[str, Any]:
        """Assess the quality of training data"""
        if not self.training_data:
            return {'quality_score': 0, 'issues': ['No training data available']}
        
        issues = []
        quality_score = 1.0
        
        # Check for score distribution
        scores = [d['manual_score'] for d in self.training_data]
        if np.std(scores) < 0.1:
            issues.append('Low score variance - may indicate biased labeling')
            quality_score -= 0.2
        
        # Check for sufficient samples per position
        positions = {}
        for entry in self.training_data:
            pos = entry['position']
            positions[pos] = positions.get(pos, 0) + 1
        
        insufficient_positions = [pos for pos, count in positions.items() if count < 20]
        if insufficient_positions:
            issues.append(f'Insufficient samples for positions: {insufficient_positions}')
            quality_score -= 0.3
        
        return {
            'quality_score': max(0, quality_score),
            'issues': issues,
            'recommendations': self._get_quality_recommendations(issues)
        }
    
    def _get_quality_recommendations(self, issues: List[str]) -> List[str]:
        """Get recommendations for improving data quality"""
        recommendations = []
        
        if any('variance' in issue for issue in issues):
            recommendations.append('Add more diverse score examples (both high and low quality matches)')
        
        if any('Insufficient samples' in issue for issue in issues):
            recommendations.append('Collect at least 20-30 examples per job position')
            
        if len(self.training_data) < 50:
            recommendations.append('Collect more training data (target: 100+ examples)')
        
        return recommendations
