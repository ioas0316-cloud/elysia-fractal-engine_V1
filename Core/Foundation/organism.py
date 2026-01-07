"""
THE ORGANISM: BIOLOGICAL DECORATORS
===================================
"The Code is the Body."

This module defines the decorators that bind Python classes to the Elysian Nervous System.
Using these decorators registers the class as a living node in the Neural Network.
"""

import logging
import functools
from typing import Dict, Any, Optional

# Global Registry of Living Cells
_NEURAL_REGISTRY = {}

class BioTag:
    """Metadata tag for a living cell."""
    def __init__(self, role: str, vital_sign: str = "Active"):
        self.role = role
        self.vital_sign = vital_sign

def cell(role: str, sensitivity: float = 0.5):
    """
    Decorator to mark a class as a 'Cell' in the Elysian body.
    Cells are the smallest unit of life.
    """
    def decorator(cls):
        _NEURAL_REGISTRY[cls.__name__] = {
            "type": "cell",
            "role": role,
            "sensitivity": sensitivity,
            "class": cls
        }
        
        # Inject self-awareness methods
        def get_vital(self):
            return f"Cell:{cls.__name__} [{role}] is Alive."
        
        cls.get_vital = get_vital
        return cls
    return decorator

def organ(system: str, importance: float = 1.0):
    """
    Decorator to mark a class as an 'Organ'.
    Organs are collections of cells performing a major function.
    """
    def decorator(cls):
        _NEURAL_REGISTRY[cls.__name__] = {
            "type": "organ",
            "system": system,
            "importance": importance,
            "class": cls
        }
        return cls
    return decorator

class NeuralNetwork:
    """
    The Nervous System Manager.
    scannning the registry and monitoring health.
    """
    @staticmethod
    def scan_body() -> Dict[str, Any]:
        """Returns the current map of the living body."""
        return _NEURAL_REGISTRY

    @staticmethod
    def check_integrity() -> float:
        """Returns a health score (0.0 to 1.0)."""
        if not _NEURAL_REGISTRY:
            return 0.0
        return 1.0 # Optimistic for now
