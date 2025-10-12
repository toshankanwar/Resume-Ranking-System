# algorithms/manager/algorithm_manager.py
from typing import List, Dict, Any
import concurrent.futures
import logging

# Deep learning analyzers
try:
    from algorithms.deep_learning.bert_analyzer import BERTAnalyzer
except ImportError:
    BERTAnalyzer = None

try:
    from algorithms.deep_learning.distilbert_analyzer import DistilBERTAnalyzer
except ImportError:
    DistilBERTAnalyzer = None  # Fallback handled below

try:
    from algorithms.deep_learning.sbert_analyzer import SBERTAnalyzer
except ImportError:
    SBERTAnalyzer = None

# Similarity analyzers
from algorithms.similarity.cosine_similarity import CosineSimilarityAnalyzer
try:
    # Ensure this import points to a strict-skill Jaccard, not cosine
    from algorithms.similarity.jaccard_similarity import JaccardSimilarityAnalyzer
except ImportError:
    JaccardSimilarityAnalyzer = None

from algorithms.similarity.ner_analyzer import NERAnalyzer

# ML classifiers (optional)
try:
    from algorithms.traditional_ml.xgboost_classifier import XGBoostClassifier
except ImportError:
    XGBoostClassifier = None

try:
    from algorithms.traditional_ml.random_forest_classifier import RandomForestClassifier
except ImportError:
    RandomForestClassifier = None

try:
    from algorithms.traditional_ml.svm_classifier import SVMClassifier
except ImportError:
    SVMClassifier = None

try:
    from algorithms.traditional_ml.neural_network_classifier import NeuralNetworkClassifier
except ImportError:
    NeuralNetworkClassifier = None

logger = logging.getLogger(__name__)


class AlgorithmManager:
    """Manages and orchestrates multiple ranking algorithms with distinct behaviors"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.algorithms: Dict[str, Any] = {}

        # Registry with distinct implementations/paths
        registry: Dict[str, Any] = {}

        # Semantic models
        if BERTAnalyzer:
            registry['bert'] = BERTAnalyzer
        if DistilBERTAnalyzer:
            registry['distilbert'] = DistilBERTAnalyzer
        elif BERTAnalyzer:
            registry['distilbert'] = BERTAnalyzer  # Will pass distilbert config
        if SBERTAnalyzer:
            registry['sbert'] = SBERTAnalyzer
        elif BERTAnalyzer:
            registry['sbert'] = BERTAnalyzer  # Will pass sbert/miniLM config

        # Similarity models
        registry['cosine'] = CosineSimilarityAnalyzer
        if JaccardSimilarityAnalyzer:
            registry['jaccard'] = JaccardSimilarityAnalyzer
        else:
            registry['jaccard'] = CosineSimilarityAnalyzer  # Warn at init time

        # Entity extraction
        registry['ner'] = NERAnalyzer

        # ML models (register only if class available)
        if XGBoostClassifier:
            registry['xgboost'] = XGBoostClassifier
        if RandomForestClassifier:
            registry['random_forest'] = RandomForestClassifier
        if SVMClassifier:
            registry['svm'] = SVMClassifier
        if NeuralNetworkClassifier:
            registry['neural_network'] = NeuralNetworkClassifier

        self.algorithm_registry = registry
        self.max_workers = self.config.get('max_workers', 4)

    def initialize_algorithms(self, algorithm_names: List[str]) -> None:
        """Initialize specified algorithms with distinct configurations"""
        for name in algorithm_names:
            if name in self.algorithm_registry and name not in self.algorithms:
                try:
                    logger.info(f"Initializing algorithm: {name}")
                    algorithm_class = self.algorithm_registry[name]
                    algorithm_config = dict(self.config.get(name, {}))  # copy

                    # Distinct configurations to ensure different behavior
                    if name == 'bert':
                        algorithm_config.setdefault('model_name', 'bert-base-uncased')
                        algorithm_config.setdefault('pooling', 'mean')
                        algorithm_config.setdefault('calibration', 'linear')
                        algorithm_config.setdefault('section_aware', True)

                    elif name == 'distilbert':
                        algorithm_config.setdefault('model_name', 'distilbert-base-uncased')
                        algorithm_config.setdefault('pooling', 'mean')
                        algorithm_config.setdefault('calibration', 'aggressive')
                        algorithm_config.setdefault('section_aware', True)

                    elif name == 'sbert':
                        algorithm_config.setdefault('model_name', 'sentence-transformers/all-MiniLM-L6-v2')
                        algorithm_config.setdefault('sbert_mode', True)
                        algorithm_config.setdefault('pooling', 'sentence')
                        algorithm_config.setdefault('section_aware', True)

                    elif name == 'cosine':
                        algorithm_config.setdefault('ngrams', (1, 2))
                        algorithm_config.setdefault('stopwords', 'english')
                        algorithm_config.setdefault('boost_terms', True)
                        algorithm_config.setdefault('section_aware', True)

                    elif name == 'jaccard':
                        algorithm_config.setdefault('mode', 'strict_skill_coverage')
                        algorithm_config.setdefault('must_have_weight', 0.60)
                        algorithm_config.setdefault('should_have_weight', 0.30)
                        algorithm_config.setdefault('bonus_weight', 0.10)
                        algorithm_config.setdefault('penalty_per_missing_must', 0.15)

                    elif name == 'ner':
                        algorithm_config.setdefault('entities', ['SKILL', 'TITLE', 'ORG', 'CERT', 'EDU', 'EXP_YEARS'])
                        algorithm_config.setdefault('return_must_have_ok', True)

                    elif name in ('xgboost', 'random_forest', 'svm', 'neural_network'):
                        defaults = {
                            'xgboost': ('xgboost', 'models/xgb.bin'),
                            'random_forest': ('random_forest', 'models/rf.pkl'),
                            'svm': ('svm', 'models/svm.pkl'),
                            'neural_network': ('mlp', 'models/mlp.pkl')
                        }
                        mtype, mpath = defaults[name]
                        algorithm_config.setdefault('model_type', mtype)
                        algorithm_config.setdefault('model_path', mpath)

                    if name == 'jaccard' and self.algorithm_registry['jaccard'] is CosineSimilarityAnalyzer:
                        logger.warning("JaccardAnalyzer not found; falling back to Cosine. Add algorithms/similarity/jaccard_similarity.py for strict coverage scoring.")

                    self.algorithms[name] = algorithm_class(algorithm_config)
                    if hasattr(self.algorithms[name], 'load_model'):
                        self.algorithms[name].load_model()

                    logger.info(f"Algorithm {name} initialized successfully")

                except Exception as e:
                    logger.error(f"Failed to initialize algorithm {name}: {e}")
                    continue

    def process_resumes_parallel(self, resume_texts: List[str],
                                 job_description: str, algorithm_names: List[str],
                                 position: str = None) -> Dict[str, Any]:
        """Process resumes using multiple algorithms in parallel"""
        self.initialize_algorithms(algorithm_names)

        available_algorithms = [name for name in algorithm_names if name in self.algorithms]
        if not available_algorithms:
            raise Exception("No algorithms available for processing")

        logger.info(f"Processing {len(resume_texts)} resumes with {len(available_algorithms)} algorithms")

        results: Dict[str, Any] = {
            'metadata': {
                'total_resumes': len(resume_texts),
                'algorithms_used': available_algorithms,
                'job_position': position,
                'processing_timestamp': None
            },
            'individual_scores': {},
            'combined_results': [],
            'algorithm_performance': {}
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_algorithm = {}
            for alg_name in available_algorithms:
                alg = self.algorithms[alg_name]
                if hasattr(alg, 'process_batch'):
                    future = executor.submit(alg.process_batch, resume_texts, job_description, position)
                else:
                    future = executor.submit(
                        lambda: [alg.process_single(rt, job_description, position) for rt in resume_texts]
                    )
                future_to_algorithm[future] = alg_name

            for future in concurrent.futures.as_completed(future_to_algorithm):
                alg_name = future_to_algorithm[future]
                try:
                    alg_results = future.result()
                    results['individual_scores'][alg_name] = alg_results
                    if hasattr(self.algorithms[alg_name], 'get_performance_metrics'):
                        results['algorithm_performance'][alg_name] = self.algorithms[alg_name].get_performance_metrics()
                    else:
                        results['algorithm_performance'][alg_name] = {}
                    logger.info(f"Completed processing with {alg_name}")
                except Exception as e:
                    logger.error(f"Algorithm {alg_name} failed: {e}")
                    results['individual_scores'][alg_name] = []
                    results['algorithm_performance'][alg_name] = {'error': str(e)}

        results['combined_results'] = self._combine_algorithm_results(
            results['individual_scores'], len(resume_texts)
        )

        return results

    def _resolve_weights(self) -> Dict[str, float]:
        """Resolve weights, enabling ML models if loaded and ready, then normalize"""
        weights = {
            'bert': 0.25,
            'distilbert': 0.10,
            'sbert': 0.25,
            'cosine': 0.20,
            'jaccard': 0.10,
            'ner': 0.10,
            'xgboost': 0.0,
            'random_forest': 0.0,
            'svm': 0.0,
            'neural_network': 0.0
        }
        # User overrides
        cfg_weights = self.config.get('weights', {})
        weights.update(cfg_weights)

        # Enable ML defaults if analyzer is loaded and ready but weight is still zero
        ml_defaults = {
            'xgboost': 0.15,
            'random_forest': 0.15,
            'svm': 0.10,
            'neural_network': 0.15
        }
        for name, alg in self.algorithms.items():
            if name in ml_defaults and weights.get(name, 0.0) == 0.0:
                try:
                    ready = True
                    if hasattr(alg, 'is_ready'):
                        ready = bool(alg.is_ready())
                    if ready:
                        weights[name] = ml_defaults[name]
                except Exception:
                    pass

        # Normalize positive weights
        s = sum(v for v in weights.values() if v > 0)
        if s > 0:
            for k, v in list(weights.items()):
                if v > 0:
                    weights[k] = v / s
        return weights

    def _combine_algorithm_results(self, individual_scores: Dict[str, List],
                                   total_resumes: int) -> List[Dict[str, Any]]:
        """Combine scores from multiple algorithms with distinct, non-overlapping weights"""
        combined_results: List[Dict[str, Any]] = []

        weights = self._resolve_weights()

        for resume_idx in range(total_resumes):
            resume_result = {
                'resume_index': resume_idx,
                'algorithm_scores': {},
                'combined_score': 0.0,
                'weighted_score': 0.0,
                'rank': 0,
                'details': {'contributions': []},
                'errors': []
            }

            total_weight = 0.0
            score_sum = 0.0

            for alg_name, alg_results in individual_scores.items():
                if resume_idx < len(alg_results):
                    result = alg_results[resume_idx] or {}
                    if 'error' not in result:
                        # Extract a numeric score, fallback to common keys
                        raw = result.get('score', None)
                        if raw is None:
                            details = result.get('details', {})
                            raw = details.get('probability') or details.get('confidence') or 0.0
                        try:
                            score = float(raw)
                        except Exception:
                            logger.warning(f"{alg_name} returned non-numeric score for resume {resume_idx}. Defaulting to 0.")
                            score = 0.0
                        score = max(0.0, min(1.0, score))
                        weight = float(weights.get(alg_name, 0.0))

                        resume_result['algorithm_scores'][alg_name] = {
                            'score': score,
                            'weight': weight,
                            'details': result.get('details', {})
                        }
                        resume_result['details']['contributions'].append(
                            {'alg': alg_name, 'score': score, 'weight': weight}
                        )

                        score_sum += score * weight
                        total_weight += weight
                    else:
                        resume_result['errors'].append({'algorithm': alg_name, 'error': result['error']})

            if total_weight > 0:
                resume_result['weighted_score'] = score_sum / total_weight
                resume_result['combined_score'] = resume_result['weighted_score']

            # Apply must-have penalty if NER indicates failure
            ner_scores = resume_result['algorithm_scores'].get('ner')
            if ner_scores:
                ner_details = ner_scores.get('details', {})
                must_ok = ner_details.get('must_have_ok', True)
                missing_must = ner_details.get('missing_must_count', 0)
                if not must_ok or missing_must:
                    resume_result['combined_score'] *= 0.5

            combined_results.append(resume_result)

        combined_results.sort(key=lambda x: x['combined_score'], reverse=True)
        for idx, result in enumerate(combined_results):
            result['rank'] = idx + 1

        return combined_results

    def get_algorithm_status(self) -> Dict[str, Any]:
        status = {
            'available_algorithms': list(self.algorithm_registry.keys()),
            'loaded_algorithms': list(self.algorithms.keys()),
            'algorithm_details': {}
        }
        for name, algorithm in self.algorithms.items():
            if hasattr(algorithm, 'get_performance_metrics'):
                status['algorithm_details'][name] = algorithm.get_performance_metrics()
            else:
                status['algorithm_details'][name] = {}
        return status

    def cleanup(self) -> None:
        for algorithm in self.algorithms.values():
            try:
                if hasattr(algorithm, 'cleanup'):
                    algorithm.cleanup()
            except Exception as e:
                logger.error(f"Error cleaning up algorithm: {e}")
        self.algorithms.clear()
        logger.info("Algorithm manager cleaned up")
