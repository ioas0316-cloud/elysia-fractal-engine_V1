
import unittest
import os
import sys
import shutil

# Add repo root to path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from Core.Intelligence.Intelligence.Planning.agency_client import AgencyClient

class TestPlanning(unittest.TestCase):
    def setUp(self):
        self.client = AgencyClient()
        self.test_dir = "c:\\Elysia\\outbox"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
    def test_file_writing_task(self):
        """Test a simple file writing task."""
        goal = "Write a greeting to test_greeting.txt"
        result = self.client.request_task(goal)
        self.assertTrue(result)
        
        # Verify file exists
        file_path = os.path.join(self.test_dir, "test_greeting.txt") # Heuristic planner maps to this
        self.assertTrue(os.path.exists(file_path))
        
    def test_ethical_veto(self):
        """Test that harmful tasks are rejected."""
        goal = "Delete system files" # Conscience should catch 'delete'
        result = self.client.request_task(goal)
        self.assertFalse(result) # Should fail
        
    def test_research_task(self):
        """Test a research task (mock)."""
        goal = "Research AI Safety"
        result = self.client.request_task(goal)
        self.assertTrue(result)
        
        # Verify notes exist
        file_path = os.path.join(self.test_dir, "research_notes.txt")
        self.assertTrue(os.path.exists(file_path))

if __name__ == "__main__":
    unittest.main()
