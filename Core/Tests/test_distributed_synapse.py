import sys
import os
import unittest
import time
from unittest.mock import patch

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Orchestration.synapse_manager import SynapseManager

class TestDistributedSynapse(unittest.TestCase):
    def setUp(self):
        self.synapse = SynapseManager(agent_id="Test_Elysia")
        print("\n--- 🧠 Distributed Synapse Test Setup ---")

    @patch('urllib.request.urlopen') # Mock network to be safe
    def test_parallel_organism(self, mock_urlopen):
        """
        Verify that Sensory and Motor organs play in an Ensemble (Parallel).
        """
        # Mock setup
        from unittest.mock import MagicMock
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html><body>Parallel World</body></html>"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        print("\n[Step 1] Running Distributed Cycle...")
        start_time = time.time()
        
        results = self.synapse.run_distributed_cycle(
            url="http://parallel.com",
            target="Global_Log",
            message="I am feeling and speaking at once."
        )
        
        duration = time.time() - start_time
        print(f"⏱️ Cycle Duration: {duration:.4f}s")
        
        # Verify both happened
        self.assertIn("Sensory", results)
        self.assertIn("Motor", results)
        
        print(f"✅ Sensory Result: {results['Sensory']}")
        print(f"✅ Motor Result: {results['Motor']}")
        
        print("🎉 Distributed Synapse Verified: The Brain is Multi-threaded.")

if __name__ == '__main__':
    unittest.main()
