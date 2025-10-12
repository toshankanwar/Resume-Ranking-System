"""Test package for Resume Ranking System"""

# Test configuration and utilities
import unittest
import tempfile
import os

def create_test_file(content: str, suffix: str = '.txt') -> str:
    """Create a temporary test file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
        f.write(content)
        return f.name

def cleanup_test_file(filepath: str):
    """Clean up test file"""
    try:
        os.unlink(filepath)
    except OSError:
        pass

# Sample test data
SAMPLE_RESUME_TEXT = """
John Doe
Software Engineer

EXPERIENCE:
Senior Python Developer - TechCorp (2020-2023)
- Developed web applications using Django and Flask
- Worked with PostgreSQL and MongoDB databases  
- Deployed applications on AWS cloud platform
- Used Git for version control and collaboration

SKILLS:
Python, JavaScript, React, Django, Flask, PostgreSQL, MongoDB, AWS, Docker, Git, Linux

EDUCATION:
Bachelor of Science in Computer Science
University of Technology (2016-2020)
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Software Engineer Position

We are seeking a talented Senior Software Engineer to join our growing team.

REQUIREMENTS:
- 3+ years of experience with Python development
- Strong experience with web frameworks (Django, Flask)
- Database experience (PostgreSQL, MongoDB) 
- Cloud platform experience (AWS preferred)
- Version control with Git
- Bachelor's degree in Computer Science or related field

RESPONSIBILITIES:
- Design and develop scalable web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews
- Deploy and maintain applications in cloud environment

We offer competitive salary, excellent benefits, and opportunity for growth.
"""

__all__ = [
    'create_test_file',
    'cleanup_test_file', 
    'SAMPLE_RESUME_TEXT',
    'SAMPLE_JOB_DESCRIPTION'
]
