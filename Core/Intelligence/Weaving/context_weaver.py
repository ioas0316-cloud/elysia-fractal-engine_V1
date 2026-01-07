from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from .intelligence_line import IntelligenceLine, LineOutput
from .void_kernel import VoidKernel
import math

@dataclass
class ContextPlane:
    """
    The 2D Plane created by weaving multiple 1D lines.
    """
    lines: Dict[str, LineOutput]
    dominant_signal: str
    overall_mood: str
    timestamp: float
    void_detected: bool = False
    void_intensity: float = 0.0
    void_kernel: Optional[VoidKernel] = None

class ContextWeaver:
    """
    The Loom.
    Now capable of detecting 'Void' (Gap between Input Complexity and System Resonance).
    """

    def __init__(self, lines: List[IntelligenceLine]):
        self.lines = lines

    def add_line(self, line: IntelligenceLine):
        self.lines.append(line)

    def _calculate_complexity(self, text: str) -> float:
        """
        Estimates text complexity (Entropy approximation).
        Long words, diverse vocabulary, special characters imply complexity.
        """
        if not text: return 0.0

        words = text.split()
        if not words: return 0.0

        # 1. Length Factor
        length_score = min(1.0, len(words) / 50.0)

        # 2. Vocabulary Richness (Unique words ratio)
        unique_ratio = len(set(words)) / len(words)

        # 3. Average Word Length (Longer words = more complex concepts usually)
        avg_word_len = sum(len(w) for w in words) / len(words)
        word_len_score = min(1.0, (avg_word_len - 3) / 5.0) # Assume avg 3 is simple

        # Weighted Sum
        complexity = (length_score * 0.3) + (unique_ratio * 0.3) + (word_len_score * 0.4)
        return min(1.0, max(0.0, complexity))

    def weave(self, context_input: Any = None) -> ContextPlane:
        import time

        outputs = {}
        total_resonance = 0.0
        max_signal = 0.0
        dominant_source = "None"

        # 1. Perceive & Accumulate Resonance
        for line in self.lines:
            output = line.perceive(context_input)
            outputs[output.source] = output

            # Sum up resonance from 'Domain' lines (exclude basic monitoring lines)
            # Universal lines usually are domain specific.
            # We assume active signal > 0.2 contributes to 'Understanding'
            if output.signal > 0.2:
                total_resonance += output.signal

            if output.signal > max_signal:
                max_signal = output.signal
                dominant_source = output.source

        # 2. Void Detection
        # Gap = Input Complexity - Total System Understanding
        input_complexity = 0.0
        if isinstance(context_input, str):
            input_complexity = self._calculate_complexity(context_input)

        # Normalize resonance expectation:
        # If complexity is 0.8, we expect at least 1.5 total resonance (e.g. 2 lines responding well)
        # This is a heuristic.
        expected_resonance = input_complexity * 2.0

        void_intensity = 0.0
        void_detected = False

        if input_complexity > 0.3: # Only check for meaningful inputs
            gap = expected_resonance - total_resonance
            if gap > 0.5:
                void_intensity = min(1.0, gap)
                void_detected = True

        # 3. Synthesize Mood
        moods = []
        sorted_outputs = sorted(outputs.values(), key=lambda x: x.signal, reverse=True)
        count = 0
        for out in sorted_outputs:
             if out.signal > 0.4:
                 desc = out.description.split("(")[0].strip()
                 moods.append(f"{out.source}:{desc}")
                 count += 1
                 if count >= 3: break

        void_kernel = None
        if void_detected:
            overall_mood = f"VOID DETECTED (Intensity: {void_intensity:.2f})"
            void_kernel = VoidKernel(
                id=f"void_{int(time.time())}",
                void_type="Ambiguity" if input_complexity < 0.7 else "DeepUnknown",
                intensity=void_intensity,
                signals=moods if moods else ["LowResonance"]
            )
        elif not moods:
            overall_mood = "Neutral / Dormant"
        else:
            overall_mood = " + ".join(moods)

        return ContextPlane(
            lines=outputs,
            dominant_signal=dominant_source,
            overall_mood=overall_mood,
            timestamp=time.time(),
            void_detected=void_detected,
            void_intensity=void_intensity,
            void_kernel=void_kernel
        )
