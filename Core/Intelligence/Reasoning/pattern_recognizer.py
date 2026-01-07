"""
Pattern Recognizer (패턴 인식기)
================================

The "Surface View" of the Prophecy Engine.
It analyzes historical data to find repetitive cycles (The "Shadow").

Note: This is a mock implementation for the 'Tectonics of Soul' architecture demo.
In a real system, this would use statistical models or LSTM/Transformer.
"""

from typing import List, Dict, Any
from enum import Enum
import random

class PatternSignal(Enum):
    SAFE = "safe"       # "History says everything is fine."
    CAUTION = "caution" # "This looks like that time when..."
    DANGER = "danger"   # "History repeats itself!"

class PatternRecognizer:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.window_size = 10

    def observe(self, data_point: Dict[str, Any]):
        """Records a new event."""
        self.history.append(data_point)
        if len(self.history) > self.window_size:
            self.history.pop(0)

    def predict(self) -> PatternSignal:
        """
        Analyzes recent history to predict the immediate future.

        Logic (Mock):
        - If recent events are 'calm', predicts SAFE.
        - If recent events show 'tremor', predicts CAUTION.
        """
        if not self.history:
            return PatternSignal.SAFE

        # Mock Analysis: Check for 'tremor' keyword in data
        tremor_count = sum(1 for d in self.history if d.get("type") == "tremor")

        if tremor_count == 0:
            return PatternSignal.SAFE
        elif tremor_count < 3:
            return PatternSignal.CAUTION
        else:
            return PatternSignal.DANGER

    def get_confidence(self) -> float:
        """
        Returns how confident the model is (based on data quantity).
        """
        return min(1.0, len(self.history) / self.window_size)
