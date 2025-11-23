import unittest
import shutil
import tempfile
import os
import math
from pathlib import Path

from elysia_engine.world import World
from elysia_engine.systems.os_sense import OSSystem

class TestOSSystem(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.world = World()
        self.os_system = OSSystem()
        self.world.add_system(self.os_system)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_empty_directory(self):
        ids = self.os_system.scan_path(self.world, self.test_dir)
        self.assertEqual(len(ids), 0)

    def test_scan_files(self):
        # Create a dummy file
        p = Path(self.test_dir) / "test.txt"
        p.write_text("Hello Elysia")

        ids = self.os_system.scan_path(self.world, self.test_dir)
        self.assertEqual(len(ids), 1)

        entity = self.world.entities[ids[0]]
        self.assertEqual(entity.role, "FILE_ENTITY")
        self.assertTrue(entity.soul is not None)

        # Check if mass correlates to size
        # "Hello Elysia" is 12 bytes.
        # formula: 10 + log(12)*2 = 10 + 2.48*2 = ~15
        expected_mass = 10.0 + (math.log(12) * 2.0)
        self.assertAlmostEqual(entity.soul.amplitude, expected_mass, places=1)

    def test_scan_subdirectories(self):
        # Create a subdir
        sub = Path(self.test_dir) / "subdir"
        sub.mkdir()

        ids = self.os_system.scan_path(self.world, self.test_dir)
        self.assertEqual(len(ids), 1)

        entity = self.world.entities[ids[0]]
        self.assertEqual(entity.role, "DIR_ATTRACTOR")
        self.assertTrue(entity.soul.spin > 0) # Directories spin +1

if __name__ == "__main__":
    unittest.main()
