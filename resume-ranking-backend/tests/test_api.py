import unittest
import json
import tempfile
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

class TestAPI(unittest.TestCase):
    """Test suite for API endpoints"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up"""
        self.app_context.pop()
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_get_algorithms(self):
        """Test algorithms endpoint"""
        response = self.client.get('/api/algorithms')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('available_algorithms', data)
        self.assertIsInstance(data['available_algorithms'], list)
    
    def test_get_positions(self):
        """Test positions endpoint"""
        response = self.client.get('/api/positions')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        
        # Check structure of first position
        position = data[0]
        self.assertIn('value', position)
        self.assertIn('label', position)
        self.assertIn('icon', position)
    
    def test_get_supported_formats(self):
        """Test supported formats endpoint"""
        response = self.client.get('/api/supported-formats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('formats', data)
        self.assertIn('max_file_size', data)
        self.assertIn('max_files', data)
    
    def test_process_resumes_missing_data(self):
        """Test process resumes with missing data"""
        response = self.client.post('/api/process-resumes')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_process_resumes_missing_job_description(self):
        """Test process resumes with missing job description"""
        # Create a dummy file
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b"Test resume content")
            tmp_file_path = tmp_file.name
        
        try:
            with open(tmp_file_path, 'rb') as test_file:
                response = self.client.post('/api/process-resumes', data={
                    'resumes': (test_file, 'test_resume.txt'),
                    'methods': ['cosine']
                })
            
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            
        finally:
            os.unlink(tmp_file_path)
    
    def test_validate_files_empty(self):
        """Test file validation with no files"""
        response = self.client.post('/api/validate-files')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
