import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import joblib
import json
from typing import Dict, List, Tuple, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatasetManager:
    """
    Academic ML Training System for Resume Ranking
    
    Folder Structure:
    data/
    ├── training_resumes/
    │   ├── excellent/          # Score: 0.8-1.0
    │   │   ├── fullstack/
    │   │   ├── backend/
    │   │   └── frontend/
    │   ├── good/              # Score: 0.6-0.8
    │   │   ├── fullstack/
    │   │   ├── backend/
    │   │   └── frontend/
    │   ├── fair/              # Score: 0.4-0.6
    │   │   ├── fullstack/
    │   │   ├── backend/
    │   │   └── frontend/
    │   └── poor/              # Score: 0.0-0.4
    │       ├── fullstack/
    │       ├── backend/
    │       └── frontend/
    ├── job_descriptions/
    │   ├── fullstack_jobs/
    │   ├── backend_jobs/
    │   └── frontend_jobs/
    └── models/
        ├── trained_models/
        ├── feature_extractors/
        └── scalers/
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.data_root = self.config.get('data_root', 'data')
        self.training_root = os.path.join(self.data_root, 'training_resumes')
        self.jobs_root = os.path.join(self.data_root, 'job_descriptions') 
        self.models_root = os.path.join(self.data_root, 'models')
        
        # Quality categories mapping
        self.quality_mapping = {
            'excellent': {'min': 0.8, 'max': 1.0, 'label': 3},
            'good': {'min': 0.6, 'max': 0.8, 'label': 2}, 
            'fair': {'min': 0.4, 'max': 0.6, 'label': 1},
            'poor': {'min': 0.0, 'max': 0.4, 'label': 0}
        }
        
        # Position categories
        self.positions = ['fullstack', 'backend', 'frontend', 'data_scientist', 'devops']
        
        self._create_folder_structure()
        self.feature_extractor = None
        self.scaler = None
    
    def _create_folder_structure(self):
        """Create the academic folder structure"""
        
        logger.info("Creating academic training folder structure...")
        
        # Create main directories
        os.makedirs(self.training_root, exist_ok=True)
        os.makedirs(self.jobs_root, exist_ok=True)
        os.makedirs(self.models_root, exist_ok=True)
        
        # Create quality-based folders
        for quality in self.quality_mapping.keys():
            quality_path = os.path.join(self.training_root, quality)
            os.makedirs(quality_path, exist_ok=True)
            
            # Create position subfolders
            for position in self.positions:
                position_path = os.path.join(quality_path, position)
                os.makedirs(position_path, exist_ok=True)
        
        # Create job description folders
        for position in self.positions:
            job_path = os.path.join(self.jobs_root, f"{position}_jobs")
            os.makedirs(job_path, exist_ok=True)
        
        # Create model storage folders
        for subfolder in ['trained_models', 'feature_extractors', 'scalers', 'evaluation_results']:
            model_subfolder = os.path.join(self.models_root, subfolder)
            os.makedirs(model_subfolder, exist_ok=True)
        
        # Create sample files for demonstration
        self._create_sample_training_files()
    
    def _create_sample_training_files(self):
        """Create sample training files for academic demonstration"""
        
        sample_resumes = {
            'excellent': {
                'fullstack': """
                Sarah Chen - Senior Full Stack Engineer
                
                PROFESSIONAL EXPERIENCE (7 years)
                Senior Full Stack Developer - TechCorp (2020-2024)
                • Architected and developed 12+ scalable web applications using React, Node.js, and microservices
                • Led cross-functional team of 6 engineers, implementing Agile methodologies
                • Optimized database queries reducing response time by 65%
                • Implemented CI/CD pipelines using Jenkins and Docker, decreasing deployment time by 80%
                • Mentored 4 junior developers, conducting code reviews and technical training
                
                Full Stack Developer - InnovateHub (2018-2020)
                • Built responsive web applications using Angular, Express.js, and MongoDB
                • Developed RESTful APIs serving 100k+ daily requests
                • Integrated third-party services including payment gateways and analytics
                • Collaborated with UX team to implement pixel-perfect designs
                
                TECHNICAL SKILLS
                Frontend: React, Angular, Vue.js, TypeScript, JavaScript, HTML5, CSS3, SASS, Bootstrap
                Backend: Node.js, Express.js, Django, Flask, Spring Boot
                Databases: MongoDB, PostgreSQL, MySQL, Redis, Elasticsearch
                Cloud & DevOps: AWS (EC2, S3, Lambda), Docker, Kubernetes, Jenkins, Git
                Testing: Jest, Mocha, Selenium, Unit Testing, Integration Testing
                
                EDUCATION
                Master of Science in Computer Science - Stanford University (2018)
                Bachelor of Engineering in Software Engineering - UC Berkeley (2016)
                
                CERTIFICATIONS
                • AWS Certified Solutions Architect
                • Google Cloud Professional Developer
                • Certified Kubernetes Administrator
                
                ACHIEVEMENTS
                • Led development of e-commerce platform generating $2M+ revenue
                • Open source contributor with 500+ GitHub stars
                • Technical speaker at 3 international conferences
                """,
                
                'backend': """
                Michael Rodriguez - Senior Backend Architect
                
                EXPERIENCE (8 years)
                Principal Backend Engineer - DataFlow Systems (2021-2024)
                • Designed distributed microservices architecture handling 10M+ daily transactions
                • Led backend team of 8 engineers across 3 product lines
                • Implemented event-driven architecture using Apache Kafka and RabbitMQ
                • Optimized system performance achieving 99.99% uptime
                • Built auto-scaling solutions reducing infrastructure costs by 40%
                
                Senior Backend Developer - CloudTech (2019-2021)
                • Developed high-performance APIs using Node.js and Python
                • Implemented caching strategies with Redis reducing latency by 70%
                • Built real-time data processing pipelines using Apache Spark
                • Designed database schemas for multi-tenant SaaS platform
                
                Backend Developer - StartupLab (2017-2019)
                • Built RESTful and GraphQL APIs using Express.js and Apollo
                • Implemented authentication and authorization systems
                • Developed background job processing using Queue systems
                • Optimized database queries and implemented database indexing
                
                TECHNICAL EXPERTISE
                Languages: Node.js, Python, Java, Go, TypeScript
                Frameworks: Express.js, Django, Flask, Spring Boot, Fastify
                Databases: PostgreSQL, MongoDB, MySQL, Redis, Cassandra, DynamoDB
                Message Queues: Apache Kafka, RabbitMQ, AWS SQS, Redis Queue
                Cloud: AWS, Google Cloud, Docker, Kubernetes, Terraform
                Monitoring: New Relic, DataDog, Prometheus, Grafana
                
                EDUCATION
                Master of Science in Distributed Systems - MIT (2017)
                Bachelor in Computer Science - Carnegie Mellon (2015)
                """,
            },
            
            'good': {
                'fullstack': """
                James Wilson - Full Stack Developer
                
                EXPERIENCE (4 years)
                Full Stack Developer - WebCorp (2021-2024)
                • Developed 8+ web applications using React and Node.js
                • Collaborated with design team to implement user interfaces
                • Built REST APIs and integrated with third-party services
                • Worked in Agile environment with 2-week sprints
                • Participated in code reviews and pair programming
                
                Junior Full Stack Developer - TechStart (2020-2021)
                • Built responsive websites using HTML, CSS, JavaScript
                • Learned React and Node.js through mentorship program
                • Fixed bugs and added new features to existing applications
                • Wrote unit tests using Jest framework
                
                SKILLS
                Frontend: React, JavaScript, HTML5, CSS3, Bootstrap
                Backend: Node.js, Express.js, Python
                Database: MongoDB, MySQL
                Tools: Git, npm, webpack, VS Code
                
                EDUCATION
                Bachelor of Science in Computer Science - State University (2020)
                """,
                
                'backend': """
                David Kumar - Backend Developer
                
                EXPERIENCE (3 years)
                Backend Developer - APITech (2022-2024)
                • Developed REST APIs using Node.js and Express
                • Worked with PostgreSQL and MongoDB databases
                • Implemented user authentication and authorization
                • Deployed applications on AWS EC2 instances
                • Collaborated with frontend team for API integration
                
                Junior Backend Developer - CodeCorp (2021-2022)
                • Built simple CRUD applications using Express.js
                • Learned database design and SQL optimization
                • Participated in daily standups and sprint planning
                • Fixed bugs in existing backend services
                
                TECHNICAL SKILLS
                Languages: Node.js, Python, JavaScript
                Databases: PostgreSQL, MongoDB, MySQL
                Cloud: AWS EC2, S3
                Tools: Git, Postman, Docker (basic)
                
                EDUCATION
                Bachelor in Information Technology (2021)
                """,
            },
            
            'fair': {
                'fullstack': """
                Lisa Park - Junior Developer
                
                EXPERIENCE (1.5 years)
                Junior Full Stack Developer - SmallTech (2023-2024)
                • Worked on small web projects using basic HTML, CSS, JavaScript
                • Learning React through online courses and tutorials
                • Made minor bug fixes in existing applications  
                • Attended team meetings and daily standups
                
                Intern - WebStudio (2023)
                • Built simple static websites
                • Learned version control with Git
                • Participated in code reviews as observer
                
                SKILLS
                Basic: HTML, CSS, JavaScript, Git
                Learning: React, Node.js
                
                EDUCATION
                Computer Science Degree (Expected 2024)
                """,
                
                'backend': """
                Tom Chen - Entry Level Backend Developer
                
                EXPERIENCE (1 year)
                Junior Backend Developer - StartCorp (2023-2024)
                • Built simple APIs using Express.js
                • Working with MySQL database
                • Learning about REST API best practices
                • Fixed minor bugs in existing code
                
                SKILLS
                Node.js (basic), Express.js, MySQL, Git
                
                EDUCATION
                Bachelor in Computer Science (2023)
                """,
            },
            
            'poor': {
                'fullstack': """
                Alex Johnson - Recent Graduate
                
                EDUCATION
                Bachelor of Science in Computer Science (2024)
                
                PROJECTS
                • Built a simple calculator using HTML, CSS, JavaScript
                • Created a basic portfolio website
                • Completed online tutorials for React
                
                SKILLS
                HTML, CSS, JavaScript (basic level)
                
                Looking to start career in web development
                """,
                
                'backend': """
                Maria Lopez - Computer Science Student
                
                EDUCATION
                Currently pursuing Bachelor in Computer Science (Final Year)
                
                ACADEMIC PROJECTS
                • Built simple web applications for coursework
                • Basic knowledge of programming concepts
                • Completed courses in data structures and algorithms
                
                SKILLS
                Python (academic level), SQL (basic), HTML/CSS
                
                Seeking internship or entry-level position
                """,
            }
        }
        
        # Create sample job descriptions
        job_descriptions = {
            'fullstack': """
            Senior Full Stack Developer Position
            
            REQUIREMENTS:
            • 4+ years of experience in full stack web development
            • Proficiency in React, Node.js, and modern JavaScript
            • Experience with databases (PostgreSQL, MongoDB)
            • Knowledge of cloud platforms (AWS preferred)
            • Strong understanding of RESTful APIs and microservices
            • Experience with version control (Git) and Agile methodologies
            • Bachelor's degree in Computer Science or related field
            
            RESPONSIBILITIES:
            • Design and develop scalable web applications
            • Lead technical decisions and architecture choices
            • Collaborate with cross-functional teams
            • Mentor junior developers and conduct code reviews
            • Ensure application performance, quality, and responsiveness
            • Stay updated with emerging technologies and best practices
            
            PREFERRED:
            • Experience with cloud services (AWS, Docker, Kubernetes)
            • Knowledge of testing frameworks and CI/CD pipelines
            • Leadership or team management experience
            • Open source contributions
            """,
            
            'backend': """
            Senior Backend Engineer Position
            
            REQUIREMENTS:
            • 5+ years of backend development experience
            • Expert knowledge of server-side languages (Node.js, Python, Java)
            • Strong experience with databases and data modeling
            • Experience with microservices architecture
            • Knowledge of cloud platforms and DevOps practices
            • Understanding of scalability, performance optimization
            • Experience with message queues and distributed systems
            
            RESPONSIBILITIES:
            • Design and implement robust backend systems
            • Build and maintain APIs serving millions of requests
            • Optimize database performance and queries
            • Implement monitoring and alerting systems
            • Lead technical architecture discussions
            • Mentor team members and establish best practices
            """,
        }
        
        # Save sample files
        for quality, positions_data in sample_resumes.items():
            for position, resume_content in positions_data.items():
                file_path = os.path.join(self.training_root, quality, position, f"sample_{quality}_{position}.txt")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(resume_content)
        
        # Save job descriptions
        for position, job_content in job_descriptions.items():
            job_path = os.path.join(self.jobs_root, f"{position}_jobs", f"{position}_senior.txt")
            with open(job_path, 'w', encoding='utf-8') as f:
                f.write(job_content)
        
        logger.info("Sample training files created successfully!")
    
    def load_training_dataset(self, position: str = None) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        Load complete training dataset from folder structure
        
        Returns:
            DataFrame with features and metadata
            Array with target scores
        """
        
        logger.info(f"Loading training dataset for position: {position or 'all'}")
        
        training_data = []
        
        # Load job descriptions for the position
        job_descriptions = self._load_job_descriptions(position)
        
        # Load resumes from each quality folder
        for quality, quality_info in self.quality_mapping.items():
            quality_path = os.path.join(self.training_root, quality)
            
            if position:
                position_folders = [position]
            else:
                position_folders = self.positions
            
            for pos in position_folders:
                position_path = os.path.join(quality_path, pos)
                
                if not os.path.exists(position_path):
                    continue
                
                # Load all resume files in this folder
                for filename in os.listdir(position_path):
                    if filename.endswith(('.txt', '.pdf', '.docx')):
                        file_path = os.path.join(position_path, filename)
                        
                        try:
                            resume_content = self._read_file(file_path)
                            
                            # Generate training examples by pairing with job descriptions
                            for job_desc in job_descriptions.get(pos, []):
                                # Generate score within quality range with some noise
                                base_score = (quality_info['min'] + quality_info['max']) / 2
                                noise = np.random.normal(0, 0.05)  # Small noise
                                target_score = np.clip(base_score + noise, 
                                                     quality_info['min'], 
                                                     quality_info['max'])
                                
                                training_data.append({
                                    'resume_text': resume_content,
                                    'job_description': job_desc,
                                    'target_score': target_score,
                                    'quality_label': quality_info['label'],
                                    'position': pos,
                                    'filename': filename,
                                    'quality_category': quality
                                })
                                
                        except Exception as e:
                            logger.error(f"Error reading file {file_path}: {e}")
                            continue
        
        if not training_data:
            raise ValueError("No training data found! Please add resume files to the training folders.")
        
        df = pd.DataFrame(training_data)
        target_scores = df['target_score'].values
        
        logger.info(f"Loaded {len(df)} training samples from {len(df.groupby(['quality_category', 'position']))} categories")
        
        return df, target_scores
    
    def _load_job_descriptions(self, position: str = None) -> Dict[str, List[str]]:
        """Load job descriptions for specified position(s)"""
        
        job_descriptions = {}
        
        if position:
            positions_to_load = [position]
        else:
            positions_to_load = self.positions
        
        for pos in positions_to_load:
            job_folder = os.path.join(self.jobs_root, f"{pos}_jobs")
            jobs = []
            
            if os.path.exists(job_folder):
                for filename in os.listdir(job_folder):
                    if filename.endswith(('.txt', '.pdf', '.docx')):
                        file_path = os.path.join(job_folder, filename)
                        try:
                            job_content = self._read_file(file_path)
                            jobs.append(job_content)
                        except Exception as e:
                            logger.error(f"Error reading job file {file_path}: {e}")
            
            job_descriptions[pos] = jobs
        
        return job_descriptions
    
    def _read_file(self, file_path: str) -> str:
        """Read content from various file formats"""
        
        if file_path.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_path.endswith('.pdf'):
            # Use your existing PDF processing
            from utils.file_processor import FileProcessor
            processor = FileProcessor()
            with open(file_path, 'rb') as f:
                return processor.extract_text_from_pdf(f)
        
        elif file_path.endswith(('.docx', '.doc')):
            # Use your existing DOCX processing
            from utils.file_processor import FileProcessor  
            processor = FileProcessor()
            with open(file_path, 'rb') as f:
                return processor.extract_text_from_docx(f)
        
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
    
    def extract_features(self, df: pd.DataFrame, fit_transform: bool = True) -> np.ndarray:
        """
        Extract comprehensive features from resume-job pairs for ML training
        
        This is the key academic component - feature engineering
        """
        
        logger.info("Extracting comprehensive feature set for ML training...")
        
        features_list = []
        
        # 1. TF-IDF Features (Traditional NLP approach)
        tfidf_features = self._extract_tfidf_features(df, fit_transform)
        
        # 2. Statistical Features (Academic approach)
        statistical_features = self._extract_statistical_features(df)
        
        # 3. Semantic Features (Advanced approach)
        semantic_features = self._extract_semantic_features(df)
        
        # 4. Pattern Matching Features (Rule-based approach)
        pattern_features = self._extract_pattern_features(df)
        
        # 5. Experience & Education Features (Domain-specific)
        domain_features = self._extract_domain_features(df)
        
        # Combine all features
        all_features = np.hstack([
            tfidf_features,
            statistical_features,
            semantic_features, 
            pattern_features,
            domain_features
        ])
        
        # Scale features for ML algorithms
        if fit_transform:
            self.scaler = StandardScaler()
            scaled_features = self.scaler.fit_transform(all_features)
        else:
            scaled_features = self.scaler.transform(all_features)
        
        # Save feature names for academic explanation
        feature_names = (
            [f"tfidf_{i}" for i in range(tfidf_features.shape[1])] +
            self._get_statistical_feature_names() +
            self._get_semantic_feature_names() +
            self._get_pattern_feature_names() +
            self._get_domain_feature_names()
        )
        
        self._save_feature_metadata(feature_names, scaled_features.shape)
        
        logger.info(f"Extracted {scaled_features.shape[1]} features from {scaled_features.shape[0]} samples")
        
        return scaled_features
    
    def _extract_tfidf_features(self, df: pd.DataFrame, fit_transform: bool) -> np.ndarray:
        """Extract TF-IDF features (Term Frequency-Inverse Document Frequency)"""
        
        # Combine resume and job description for context
        combined_texts = [
            f"{resume} {job}" 
            for resume, job in zip(df['resume_text'], df['job_description'])
        ]
        
        if fit_transform:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=2000,  # Limit features for academic explanation
                ngram_range=(1, 2),  # Unigrams and bigrams
                stop_words='english',
                min_df=2,  # Must appear in at least 2 documents
                max_df=0.8,  # Exclude very common terms
                sublinear_tf=True  # Apply log scaling
            )
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(combined_texts)
        else:
            tfidf_matrix = self.tfidf_vectorizer.transform(combined_texts)
        
        return tfidf_matrix.toarray()
    
    def _extract_statistical_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract statistical features from text"""
        
        features = []
        
        for _, row in df.iterrows():
            resume = row['resume_text']
            job = row['job_description']
            
            # Length-based features
            resume_word_count = len(resume.split())
            job_word_count = len(job.split())
            length_ratio = resume_word_count / max(job_word_count, 1)
            
            # Character-level features
            resume_char_count = len(resume)
            job_char_count = len(job)
            char_ratio = resume_char_count / max(job_char_count, 1)
            
            # Vocabulary features
            resume_words = set(resume.lower().split())
            job_words = set(job.lower().split())
            vocabulary_overlap = len(resume_words & job_words) / max(len(job_words), 1)
            vocabulary_coverage = len(resume_words & job_words) / max(len(resume_words), 1)
            
            # Sentence complexity
            resume_sentences = resume.count('.') + resume.count('!') + resume.count('?')
            avg_sentence_length = resume_word_count / max(resume_sentences, 1)
            
            features.append([
                resume_word_count, job_word_count, length_ratio,
                resume_char_count, job_char_count, char_ratio,
                vocabulary_overlap, vocabulary_coverage,
                resume_sentences, avg_sentence_length
            ])
        
        return np.array(features)
    
    def _extract_semantic_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract semantic similarity features"""
        
        features = []
        
        # Define semantic categories for matching
        tech_skills = {
            'languages': ['python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++'],
            'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform'],
            'tools': ['git', 'jira', 'confluence', 'postman', 'webpack', 'npm', 'yarn']
        }
        
        for _, row in df.iterrows():
            resume_lower = row['resume_text'].lower()
            job_lower = row['job_description'].lower()
            
            category_scores = []
            
            # Calculate match score for each category
            for category, skills in tech_skills.items():
                resume_skills = sum(1 for skill in skills if skill in resume_lower)
                job_skills = sum(1 for skill in skills if skill in job_lower)
                
                if job_skills > 0:
                    category_score = resume_skills / job_skills
                else:
                    category_score = 0.0
                
                category_scores.append(min(category_score, 1.0))  # Cap at 1.0
            
            # Overall semantic similarity (average)
            overall_semantic = np.mean(category_scores) if category_scores else 0.0
            
            features.append(category_scores + [overall_semantic])
        
        return np.array(features)
    
    def _extract_pattern_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract pattern-based features using regex"""
        
        import re
        features = []
        
        for _, row in df.iterrows():
            resume = row['resume_text']
            job = row['job_description']
            
            # Experience pattern matching
            resume_exp = self._extract_years_experience(resume)
            job_exp = self._extract_years_experience(job)
            experience_match = 1.0 if resume_exp >= job_exp else max(0.0, resume_exp / max(job_exp, 1))
            
            # Education level matching
            resume_education = self._extract_education_level(resume)
            job_education = self._extract_education_level(job)
            education_match = 1.0 if resume_education >= job_education else 0.5
            
            # Contact information completeness
            has_email = 1.0 if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', resume) else 0.0
            has_phone = 1.0 if re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', resume) else 0.0
            
            # Section completeness
            has_experience = 1.0 if re.search(r'\b(experience|work|employment)\b', resume, re.I) else 0.0
            has_education = 1.0 if re.search(r'\b(education|degree|university|college)\b', resume, re.I) else 0.0
            has_skills = 1.0 if re.search(r'\b(skills|technologies|technical)\b', resume, re.I) else 0.0
            
            features.append([
                experience_match, education_match,
                has_email, has_phone, 
                has_experience, has_education, has_skills
            ])
        
        return np.array(features)
    
    def _extract_domain_features(self, df: pd.DataFrame) -> np.ndarray:
        """Extract domain-specific features for each position type"""
        
        features = []
        
        # Position-specific skill requirements
        position_skills = {
            'fullstack': ['react', 'node', 'javascript', 'html', 'css', 'mongodb', 'express'],
            'backend': ['api', 'database', 'server', 'microservices', 'python', 'java', 'node'],
            'frontend': ['react', 'angular', 'vue', 'html', 'css', 'javascript', 'ui', 'ux'],
            'data_scientist': ['python', 'machine learning', 'pandas', 'numpy', 'tensorflow', 'sql'],
            'devops': ['docker', 'kubernetes', 'aws', 'jenkins', 'terraform', 'monitoring']
        }
        
        for _, row in df.iterrows():
            resume_lower = row['resume_text'].lower()
            position = row['position']
            
            # Calculate position-specific skill match
            required_skills = position_skills.get(position, [])
            matched_skills = sum(1 for skill in required_skills if skill in resume_lower)
            skill_match_ratio = matched_skills / max(len(required_skills), 1)
            
            # Leadership indicators
            leadership_terms = ['led', 'managed', 'supervised', 'mentored', 'team lead', 'senior', 'principal']
            leadership_score = sum(1 for term in leadership_terms if term in resume_lower) / len(leadership_terms)
            
            # Project complexity indicators
            complexity_terms = ['scalable', 'distributed', 'microservices', 'architecture', 'optimization']
            complexity_score = sum(1 for term in complexity_terms if term in resume_lower) / len(complexity_terms)
            
            # Industry experience relevance
            industry_terms = ['startup', 'enterprise', 'saas', 'fintech', 'healthcare', 'ecommerce']
            industry_score = sum(1 for term in industry_terms if term in resume_lower) / len(industry_terms)
            
            features.append([
                skill_match_ratio, leadership_score, 
                complexity_score, industry_score
            ])
        
        return np.array(features)
    
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
    
    def _extract_education_level(self, text: str) -> int:
        """Extract education level (0=None, 1=Bachelor, 2=Master, 3=PhD)"""
        text_lower = text.lower()
        
        if any(term in text_lower for term in ['phd', 'ph.d', 'doctorate', 'doctoral']):
            return 3
        elif any(term in text_lower for term in ['master', 'msc', 'ms', 'mba', 'ma']):
            return 2
        elif any(term in text_lower for term in ['bachelor', 'bsc', 'bs', 'ba', 'be', 'btech']):
            return 1
        else:
            return 0
    
    def _get_statistical_feature_names(self) -> List[str]:
        return [
            'resume_word_count', 'job_word_count', 'length_ratio',
            'resume_char_count', 'job_char_count', 'char_ratio',
            'vocabulary_overlap', 'vocabulary_coverage',
            'resume_sentences', 'avg_sentence_length'
        ]
    
    def _get_semantic_feature_names(self) -> List[str]:
        return [
            'languages_match', 'frameworks_match', 'databases_match',
            'cloud_match', 'tools_match', 'overall_semantic'
        ]
    
    def _get_pattern_feature_names(self) -> List[str]:
        return [
            'experience_match', 'education_match',
            'has_email', 'has_phone',
            'has_experience_section', 'has_education_section', 'has_skills_section'
        ]
    
    def _get_domain_feature_names(self) -> List[str]:
        return [
            'position_skill_match', 'leadership_score',
            'complexity_score', 'industry_score'
        ]
    
    def _save_feature_metadata(self, feature_names: List[str], shape: Tuple[int, int]):
        """Save feature metadata for academic analysis"""
        
        metadata = {
            'feature_names': feature_names,
            'total_features': len(feature_names),
            'feature_shape': shape,
            'feature_categories': {
                'tfidf_features': 2000,
                'statistical_features': 10,
                'semantic_features': 6,
                'pattern_features': 7,
                'domain_features': 4
            },
            'created_at': datetime.now().isoformat()
        }
        
        metadata_file = os.path.join(self.models_root, 'feature_extractors', 'feature_metadata.json')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Save feature extractor components
        if hasattr(self, 'tfidf_vectorizer'):
            joblib.dump(self.tfidf_vectorizer, 
                       os.path.join(self.models_root, 'feature_extractors', 'tfidf_vectorizer.joblib'))
        
        if hasattr(self, 'scaler'):
            joblib.dump(self.scaler,
                       os.path.join(self.models_root, 'scalers', 'feature_scaler.joblib'))
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get comprehensive dataset statistics for academic reporting"""
        
        try:
            df, target_scores = self.load_training_dataset()
            
            stats = {
                'dataset_overview': {
                    'total_samples': len(df),
                    'positions': df['position'].value_counts().to_dict(),
                    'quality_distribution': df['quality_category'].value_counts().to_dict(),
                    'avg_target_score': float(np.mean(target_scores)),
                    'score_std': float(np.std(target_scores)),
                    'score_range': [float(np.min(target_scores)), float(np.max(target_scores))]
                },
                
                'text_statistics': {
                    'avg_resume_length': float(df['resume_text'].str.len().mean()),
                    'avg_job_length': float(df['job_description'].str.len().mean()),
                    'avg_resume_words': float(df['resume_text'].str.split().str.len().mean()),
                    'avg_job_words': float(df['job_description'].str.split().str.len().mean())
                },
                
                'quality_analysis': self._analyze_quality_distribution(df, target_scores),
                'position_analysis': self._analyze_position_distribution(df),
                'data_quality_score': self._calculate_data_quality_score(df)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating dataset statistics: {e}")
            return {'error': str(e)}
    
    def _analyze_quality_distribution(self, df: pd.DataFrame, target_scores: np.ndarray) -> Dict[str, Any]:
        """Analyze quality distribution for academic insight"""
        
        quality_stats = {}
        
        for quality in self.quality_mapping.keys():
            quality_data = df[df['quality_category'] == quality]
            quality_scores = quality_data.index.map(lambda i: target_scores[i])
            
            if len(quality_data) > 0:
                quality_stats[quality] = {
                    'sample_count': len(quality_data),
                    'avg_score': float(np.mean(quality_scores)),
                    'score_range': [float(np.min(quality_scores)), float(np.max(quality_scores))],
                    'positions': quality_data['position'].value_counts().to_dict()
                }
        
        return quality_stats
    
    def _analyze_position_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze position-specific data distribution"""
        
        position_stats = {}
        
        for position in df['position'].unique():
            position_data = df[df['position'] == position]
            
            position_stats[position] = {
                'total_samples': len(position_data),
                'quality_distribution': position_data['quality_category'].value_counts().to_dict(),
                'avg_resume_length': float(position_data['resume_text'].str.len().mean()),
                'files_count': position_data['filename'].nunique()
            }
        
        return position_stats
    
    def _calculate_data_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate overall data quality score for academic assessment"""
        
        quality_factors = []
        
        # 1. Sample diversity (0-1)
        position_diversity = len(df['position'].unique()) / len(self.positions)
        quality_factors.append(position_diversity * 0.2)
        
        # 2. Quality balance (0-1)  
        quality_counts = df['quality_category'].value_counts()
        quality_balance = 1.0 - (quality_counts.std() / quality_counts.mean()) if len(quality_counts) > 1 else 0.5
        quality_factors.append(max(0, min(1, quality_balance)) * 0.3)
        
        # 3. Sample size adequacy (0-1)
        sample_adequacy = min(1.0, len(df) / 100)  # Target: 100+ samples
        quality_factors.append(sample_adequacy * 0.3)
        
        # 4. Content quality (0-1)
        avg_resume_length = df['resume_text'].str.len().mean()
        content_quality = min(1.0, avg_resume_length / 2000)  # Target: 2000+ chars
        quality_factors.append(content_quality * 0.2)
        
        overall_quality = sum(quality_factors)
        return float(overall_quality)
