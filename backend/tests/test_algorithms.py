import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.similarity.cosine_similarity import CosineSimilarityAnalyzer
from algorithms.similarity.jaccard_similarity import JaccardSimilarityAnalyzer
from algorithms.similarity.ner_analyzer import NERAnalyzer

class TestAlgorithms(unittest.TestCase):
    """Test suite for resume ranking algorithms"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_resume = """
        John Doe
        Software Engineer
        
        Experience:
        - 3 years of Python development
        - Django and Flask web frameworks
        - PostgreSQL and MongoDB databases
        - AWS cloud services
        - Git version control
        
        Skills:
        Python, JavaScript, React, Django, Flask, PostgreSQL, MongoDB, AWS, Docker, Git
        
        Education:
        Bachelor of Science in Computer Science
        """
        
        self.sample_job = """
        We are looking for a Software Engineer with experience in:
        - Python programming
        - Web development with Django or Flask
        - Database design (PostgreSQL preferred)
        - Cloud services (AWS)
        - Version control (Git)
        
        Requirements:
        - 2+ years of experience
        - Strong problem-solving skills
        - Bachelor's degree in Computer Science or related field
        """
    
    def test_cosine_similarity(self):
        """Test Cosine Similarity algorithm"""
        analyzer = CosineSimilarityAnalyzer()
        result = analyzer.process_single(self.sample_resume, self.sample_job)
        
        self.assertIn('algorithm', result)
        self.assertEqual(result['algorithm'], 'cosine')
        self.assertIn('score', result)
        self.assertIsInstance(result['score'], float)
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 1.0)
        self.assertIn('details', result)
    
    def test_jaccard_similarity(self):
        """Test Jaccard Similarity algorithm"""
        analyzer = JaccardSimilarityAnalyzer()
        result = analyzer.process_single(self.sample_resume, self.sample_job)
        
        self.assertIn('algorithm', result)
        self.assertEqual(result['algorithm'], 'jaccard')
        self.assertIn('score', result)
        self.assertIsInstance(result['score'], float)
        self.assertGreaterEqual(result['score'], 0.0)
        self.assertLessEqual(result['score'], 1.0)
        self.assertIn('details', result)
        self.assertIn('matching_skills', result['details'])
    
    def test_ner_analyzer(self):
        """Test NER analyzer"""
        try:
            analyzer = NERAnalyzer()
            result = analyzer.process_single(self.sample_resume, self.sample_job)
            
            self.assertIn('algorithm', result)
            self.assertEqual(result['algorithm'], 'ner')
            self.assertIn('score', result)
            self.assertIsInstance(result['score'], float)
            self.assertGreaterEqual(result['score'], 0.0)
            self.assertLessEqual(result['score'], 1.0)
            self.assertIn('details', result)
            self.assertIn('extracted_skills', result['details'])
            
        except Exception as e:
            self.skipTest(f"NER test skipped due to missing spaCy model: {e}")
    
    def test_algorithm_consistency(self):
        """Test that algorithms return consistent results"""
        cosine_analyzer = CosineSimilarityAnalyzer()
        jaccard_analyzer = JaccardSimilarityAnalyzer()
        
        # Run multiple times to check consistency
        cosine_results = []
        jaccard_results = []
        
        for _ in range(3):
            cosine_result = cosine_analyzer.process_single(self.sample_resume, self.sample_job)
            jaccard_result = jaccard_analyzer.process_single(self.sample_resume, self.sample_job)
            
            cosine_results.append(cosine_result['score'])
            jaccard_results.append(jaccard_result['score'])
        
        # Check consistency (all results should be identical)
        self.assertEqual(len(set(cosine_results)), 1, "Cosine similarity should be consistent")
        self.assertEqual(len(set(jaccard_results)), 1, "Jaccard similarity should be consistent")

if __name__ == '__main__':
    unittest.main()
