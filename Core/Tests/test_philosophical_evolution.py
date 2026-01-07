import sys
import os
import unittest
import glob
from unittest.mock import MagicMock

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Evolution.Genesis.code_genesis import CodeGenesis

class TestPhilosophicalEvolution(unittest.TestCase):
    def setUp(self):
        self.genesis = CodeGenesis()
        self.test_file = "dummy_chaos.py"
        
        # Create a 'Chaos' file
        with open(self.test_file, "w") as f:
            f.write("def mess():\n    print('I am inefficient')\n    a=1+1\n")
            
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # Clean backups
        backups = glob.glob(os.path.join(self.genesis.backup_dir, "dummy_chaos.py.*.bak"))
        for b in backups:
            os.remove(b)

    def test_evolution_cycle(self):
        print("\n--- 🦋 Testing Philosophical Evolution ---")
        
        # 1. Contemplate (Mocking the thought)
        # In reality, this comes from LLM.
        contemplation = {
            "file": self.test_file,
            "intent": "Transform chaos into order",
            "reasoning": "The function does nothing useful."
        }
        
        # 2. Synthesize (Providing 'Evolved' code)
        new_code = "def order():\n    \"\"\"This is efficient.\"\"\"\n    print('I am order')\n"
        
        # 3. Evolve
        print(f"   Aiming to evolve {self.test_file}...")
        success = self.genesis.evolve_file(self.test_file, new_code)
        
        # 4. Verify
        self.assertTrue(success, "Evolution failed.")
        
        with open(self.test_file, "r") as f:
            content = f.read()
            self.assertIn("def order():", content, "File was not updated!")
            self.assertNotIn("def mess():", content, "Old chaos still exists!")
            
        print("   ✅ File updated successfully.")
        
        # 5. Verify Backup
        backups = glob.glob(os.path.join(self.genesis.backup_dir, "dummy_chaos.py.*.bak"))
        self.assertTrue(len(backups) > 0, "No backup created!")
        print(f"   ✅ Backup found: {backups[0]}")
        
if __name__ == '__main__':
    unittest.main()
