"""Similarity algorithms package"""

from .cosine_similarity import CosineSimilarityAnalyzer
from .jaccard_similarity import JaccardSimilarityAnalyzer
from .ner_analyzer import NERAnalyzer

__all__ = [
    'CosineSimilarityAnalyzer',
    'JaccardSimilarityAnalyzer',
    'NERAnalyzer'
]
