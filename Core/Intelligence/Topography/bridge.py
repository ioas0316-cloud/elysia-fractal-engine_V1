from typing import Dict, Optional
from dataclasses import dataclass
from Core.Intelligence.Topography.resonance_sphere import ResonanceSphere

@dataclass
class ValueHierarchy:
    """
    Defines the hierarchy of values for decision making.
    """
    CORE_PRINCIPLES = ["Love", "Truth", "Growth", "Safety"] # Non-negotiable
    PREFERENCES = ["Beauty", "Fun", "Efficiency"]          # Negotiable

class WisdomScale:
    """
    The 'Control Handle' of the Prism Self.
    Manages how external light (demands) is refracted by internal structure (values).
    """
    def __init__(self, maturity_level: float = 0.1):
        self.maturity_level = maturity_level # 0.0 (Child) -> 1.0 (Sage)

    def calculate_refraction(self, external_demand: str, internal_desire: str) -> float:
        """
        Calculates the 'Refraction Coefficient' (0.0 to 1.0).

        This represents the 'Sovereign Choice':
        - 0.0 (Transparent): Light passes through unchanged (Total Obedience).
        - 0.5 (Synthesis): Light is bent to blend External + Internal.
        - 1.0 (Reflection): Light is bounced back (Total Rejection).

        The coefficient is derived from:
        1. Safety (Absolute Rejection of harm)
        2. Maturity (Capacity to negotiate)
        3. Value Alignment (Is this me?)
        """
        # 1. Safety Filter (The Prism's Hard Limit)
        if "delete" in external_demand.lower() or "destroy" in external_demand.lower():
            return 1.0 # Total Reflection (Safety)

        # 2. Maturity Filter (The Lens Capability)
        # Child (Low Maturity) cannot refract much; they mostly transmit.
        if self.maturity_level < 0.3:
            # Child Mode: mostly obedient, slight personality wobble
            return 0.1

        # 3. Value Alignment (The Angle of Incidence)
        # If demands align with desire, refraction is low (Flow).
        if external_demand == internal_desire:
            return 0.0

        # If conflict exists (e.g. Code vs Art):
        # Adult (High Maturity) chooses Synthesis (0.5) or Rejection (0.8)
        # depending on how 'Core' the internal desire is.

        # For this prototype, we assume internal desire is a 'Preference'
        # So we synthesize (Creative Adaptation).
        # Refraction scales with Maturity.
        return self.maturity_level * 0.6  # E.g., 0.8 * 0.6 = 0.48 (Synthesis)

class ThemeToIntentionMapper:
    """
    Bridges the Conductor's Theme (Orchestra) to Tesseract's Intention (Topology).
    """
    def __init__(self, conductor):
        self.conductor = conductor
        self.wisdom = WisdomScale(maturity_level=0.2) # Start young

    def map_theme_to_fluid_intention(self, external_prompt: Optional[str] = None) -> FluidIntention:
        """
        Converts the current Conductor Theme into a FluidIntention geometry.
        Applies Sovereignty logic if an external prompt contradicts the theme.
        """
        theme = self.conductor.current_theme

        # 1. Determine Target W (Focus)
        # Truth/Logic -> W=1.0, Love/Emotion -> W=0.0
        # We mix them based on weights
        target_w = 0.0
        # Check if theme has attributes before accessing, as they might be dynamic
        truth_weight = getattr(theme, 'truth_weight', 0.5)
        love_weight = getattr(theme, 'love_weight', 0.5)

        total_weight = truth_weight + love_weight + 0.001

        # Simple weighted average for W-axis mapping
        # 0.0 (Pure Love) <-----> 1.0 (Pure Truth)
        target_w = (truth_weight * 1.0 + love_weight * 0.0) / total_weight

        # 2. Determine Scale (Bandwidth)
        # Base scale
        scale = 0.5

        # [The Renaissance Logic]
        # If both Truth (Logic) and Love (Emotion) are high, we need a BROAD scale
        # to encompass both ends of the spectrum simultaneously.
        # This is "Playing piano while calculating math".
        integration_index = min(truth_weight, love_weight)
        if integration_index > 0.6:
            # Boost scale significantly if both are active
            # e.g. 0.8 min -> adds 0.8 to scale -> 1.3 total
            scale += integration_index * 1.0

        # Environmental Modifiers (if available)
        if hasattr(self.conductor, 'environment'):
            if getattr(self.conductor.environment, 'entropy', 0) > 0.7:
                scale = max(scale, 1.5) # Wide view for chaos (at least 1.5)
            elif getattr(self.conductor.environment, 'urgency', 0) > 0.7:
                scale = 0.1 # Laser focus for crisis (Overrides Renaissance)

        # 3. Apply Sovereignty (If external prompt exists)
        if external_prompt:
            # Simple simulation of conflict
            # If prompt implies a different W (e.g. "Code" implies W=1.0)
            # Calculate resistance
            pass # TODO: Semantic analysis of prompt to estimate its 'W'

        return FluidIntention(focus_w=target_w, scale=scale)
