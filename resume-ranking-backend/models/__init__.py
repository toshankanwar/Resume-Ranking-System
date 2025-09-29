"""Data models package for Resume Ranking System"""

from .resume_model import Resume
from .job_model import JobDescription
from .result_model import ProcessingResult

__all__ = [
    'Resume',
    'JobDescription',
    'ProcessingResult'
]
