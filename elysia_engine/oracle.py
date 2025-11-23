from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tensor import SoulTensor
    from .consciousness import GlobalConsciousness

class Oracle:
    """
    The Bridge between Quantum States and Human Language.
    Translates Wave Functions into Insights.
    """

    @staticmethod
    def interpret_superposition(soul: SoulTensor) -> str:
        if not soul.superposition_states:
            return "The mind is clear and singular."

        count = len(soul.superposition_states)
        # Just take the top 2 for description
        sorted_states = sorted(soul.superposition_states, key=lambda x: x[1], reverse=True)

        descriptions = []
        for state, prob in sorted_states[:2]:
            emo = state.decode_emotion()
            descriptions.append(f"{prob*100:.0f}% urge towards '{emo}'")

        return f"The soul is fractured into {count} possibilities. Conflict between: {', '.join(descriptions)}."

    @staticmethod
    def consult_akashic(global_sys: GlobalConsciousness) -> str:
        entropy = global_sys.global_entropy
        alignment = global_sys.alignment_score

        if entropy > 0.7:
            return f"Chaos reigns (Entropy: {entropy:.2f}). The voices are discordant."
        elif alignment > 0.8:
            return f"Harmonic convergence achieved (Alignment: {alignment:.2f}). The One sings."
        else:
            return f"The world is in flux (Entropy: {entropy:.2f}). Balance is shifting."
