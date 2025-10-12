"""Algorithms package for Resume Ranking System"""

from .base_algorithm import BaseAlgorithm

# Deep Learning Algorithms
from .deep_learning.bert_analyzer import BERTAnalyzer
from .deep_learning.distilbert_analyzer import DistilBERTAnalyzer
from .deep_learning.sbert_analyzer import SBERTAnalyzer
from .deep_learning.xlm_analyzer import XLMAnalyzer

# Traditional ML Algorithms  
from .traditional_ml.xgboost_classifier import XGBoostClassifier
from .traditional_ml.random_forest_classifier import RandomForestClassifier
from .traditional_ml.svm_classifier import SVMClassifier
from .traditional_ml.neural_network_classifier import NeuralNetworkClassifier

# Similarity Algorithms
from .similarity.cosine_similarity import CosineSimilarityAnalyzer
from .similarity.jaccard_similarity import JaccardSimilarityAnalyzer
from .similarity.ner_analyzer import NERAnalyzer

__all__ = [
    'BaseAlgorithm',
    'BERTAnalyzer',
    'DistilBERTAnalyzer', 
    'SBERTAnalyzer',
    'XLMAnalyzer',
    'XGBoostClassifier',
    'RandomForestClassifier',
    'SVMClassifier', 
    'NeuralNetworkClassifier',
    'CosineSimilarityAnalyzer',
    'JaccardSimilarityAnalyzer',
    'NERAnalyzer'
]
