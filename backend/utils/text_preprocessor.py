import re
import string
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """Advanced text preprocessing for resume analysis"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.remove_emails = self.config.get('remove_emails', True)
        self.remove_phones = self.config.get('remove_phones', True)
        self.remove_urls = self.config.get('remove_urls', True)
        self.normalize_whitespace = self.config.get('normalize_whitespace', True)
        
    def clean_resume_text(self, text: str) -> str:
        """Comprehensive resume text cleaning"""
        if not text:
            return ""
        
        try:
            # Remove personal information
            text = self._remove_personal_info(text)
            
            # Clean formatting
            text = self._clean_formatting(text)
            
            # Normalize text
            text = self._normalize_text(text)
            
            # Remove excessive whitespace
            if self.normalize_whitespace:
                text = self._normalize_whitespace(text)
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Text cleaning failed: {e}")
            return text  # Return original text if cleaning fails
    
    def _remove_personal_info(self, text: str) -> str:
        """Remove personal information like emails, phones, addresses"""
        
        if self.remove_emails:
            # Remove email addresses
            text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        if self.remove_phones:
            # Remove phone numbers (various formats)
            phone_patterns = [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # 123-456-7890
                r'\(\d{3}\)\s?\d{3}[-.]?\d{4}',    # (123) 456-7890
                r'\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}',  # International
            ]
            for pattern in phone_patterns:
                text = re.sub(pattern, '', text)
        
        if self.remove_urls:
            # Remove URLs
            text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
            text = re.sub(r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove common address patterns
        address_patterns = [
            r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)',
            r'\b[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}(-\d{4})?\b',  # City, ST 12345
        ]
        for pattern in address_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text
    
    def _clean_formatting(self, text: str) -> str:
        """Clean formatting artifacts from PDF/DOCX extraction"""
        
        # Remove bullet points and list markers
        text = re.sub(r'^[\s]*[•·▪▫‣⁃]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*[-*]\s*', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*\d+[.)]\s*', '', text, flags=re.MULTILINE)
        
        # Remove excessive punctuation
        text = re.sub(r'[.]{2,}', '.', text)
        text = re.sub(r'[-]{2,}', '-', text)
        text = re.sub(r'[_]{2,}', '_', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'^\s*Page\s+\d+\s*$', '', text, flags=re.MULTILINE | re.IGNORECASE)
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better processing"""
        
        # Fix common OCR errors
        ocr_fixes = {
            'experienee': 'experience',
            'skilIs': 'skills',
            'programmlng': 'programming',
            'managemenl': 'management',
            'developmenl': 'development',
            'analylics': 'analytics',
            'responslble': 'responsible'
        }
        
        for wrong, right in ocr_fixes.items():
            text = text.replace(wrong, right)
        
        # Normalize degree abbreviations
        degree_normalizations = {
            r'\bB\.?S\.?\b': 'Bachelor of Science',
            r'\bM\.?S\.?\b': 'Master of Science',
            r'\bB\.?A\.?\b': 'Bachelor of Arts',
            r'\bM\.?A\.?\b': 'Master of Arts',
            r'\bPh\.?D\.?\b': 'Doctor of Philosophy',
            r'\bMBA\b': 'Master of Business Administration'
        }
        
        for pattern, replacement in degree_normalizations.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Normalize technology terms
        tech_normalizations = {
            r'\bJS\b': 'JavaScript',
            r'\bTS\b': 'TypeScript',
            r'\bML\b': 'Machine Learning',
            r'\bAI\b': 'Artificial Intelligence',
            r'\bAPI\b': 'Application Programming Interface',
            r'\bSQL\b': 'Structured Query Language',
            r'\bHTML\b': 'HyperText Markup Language',
            r'\bCSS\b': 'Cascading Style Sheets'
        }
        
        for pattern, replacement in tech_normalizations.items():
            text = re.sub(pattern, replacement, text)
        
        return text
    
    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace characters"""
        
        # Replace multiple spaces with single space
        text = re.sub(r' {2,}', ' ', text)
        
        # Replace tabs with spaces
        text = text.replace('\t', ' ')
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in text.split('\n')]
        text = '\n'.join(lines)
        
        return text
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract different sections from resume"""
        
        sections = {
            'summary': '',
            'experience': '',
            'education': '',
            'skills': '',
            'projects': '',
            'certifications': ''
        }
        
        # Section header patterns
        section_patterns = {
            'summary': r'(?:professional\s+)?summary|objective|profile',
            'experience': r'(?:work\s+)?experience|employment|career|professional\s+background',
            'education': r'education|academic\s+background|qualifications',
            'skills': r'(?:technical\s+)?skills|competencies|expertise',
            'projects': r'projects|portfolio',
            'certifications': r'certifications?|certificates|licenses'
        }
        
        try:
            # Split text into lines
            lines = text.split('\n')
            current_section = None
            
            for line in lines:
                line_lower = line.lower().strip()
                
                # Check if line is a section header
                section_found = False
                for section, pattern in section_patterns.items():
                    if re.search(f'^{pattern}', line_lower):
                        current_section = section
                        section_found = True
                        break
                
                # If not a section header and we have a current section, add to that section
                if not section_found and current_section and line.strip():
                    sections[current_section] += line + '\n'
            
        except Exception as e:
            logger.error(f"Section extraction failed: {e}")
        
        return sections
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        
        skill_categories = {
            'programming': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php',
                'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala'
            ],
            'web': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring boot', 'laravel'
            ],
            'database': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sql server', 'sqlite'
            ],
            'cloud': [
                'aws', 'azure', 'google cloud', 'docker', 'kubernetes',
                'terraform', 'ansible'
            ],
            'data': [
                'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn',
                'tableau', 'power bi', 'spark'
            ]
        }
        
        found_skills = []
        text_lower = text.lower()
        
        for category, skills in skill_categories.items():
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
