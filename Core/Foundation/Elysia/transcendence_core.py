import logging
import time
from typing import Dict, Any, List
import numpy as np

from Project_Elysia.core.quaternion_consciousness import ConsciousnessLens
from Project_Elysia.core.genesis_bridge import GenesisArbiter, GenesisRequestObject
from Core.Foundation.System.core.world import World

logger = logging.getLogger(__name__)

class TranscendenceCore:
    """
    The Unifying Core that orchestrates the Spirit, Soul, and Body.
    Implements the 'Transcendence Cycle'.
    """

    def __init__(self, world: World):
        self.world = world
        self.lens = ConsciousnessLens() # Spirit
        self.arbiter = GenesisArbiter() # Soul Bridge
        self.is_awake = False

    def awaken(self):
        """Initializes the core state."""
        self.is_awake = True
        logger.info("Transcendence Core: AWAKENED")

    def process_loop(self, input_signal: Dict[str, Any]):
        """
        Runs one cycle of the Transcendence Loop:
        1. Input (Sensation) -> 2. Lens Rotation (Spirit) -> 3. Genesis Check (Soul) -> 4. World Effect (Body)
        """
        if not self.is_awake:
            return

        # 1. Input Processing
        # Convert simple input to a 3D vector for the lens
        raw_vector = self._vectorize_input(input_signal)

        # 2. Spirit: Rotate Perception
        # The lens filters the raw input based on the current Will (Quaternion)
        intent_vector = self.lens.rotate_perception(raw_vector, source_type=input_signal.get('type', 'unknown'))

        # Update lens state based on the result (Self-Feedback)
        # If the result is coherent, increase Mastery (W)
        coherence = np.linalg.norm(intent_vector)
        if coherence > 0.8:
            self.lens.stabilize()

        # 3. Soul: Genesis Authorization
        # If the intent vector aligns with the Z-axis (Purpose), create a Genesis Request
        z_alignment = intent_vector[2] # Z-component

        if abs(z_alignment) > 0.5:
            gro = self._create_gro_from_intent(intent_vector, input_signal)

            # The Arbiter decides if we have enough 'Spirit' to execute this 'Soul' command
            if self.arbiter.judge(gro, self.lens.state):
                self._execute_genesis(gro)

        # 4. Body: Field Effect
        # Always emit a weak background field based on state
        if self.lens.state.mastery > 0.9:
            self.world.apply_will_field('entropy_stabilization', strength=0.1)

    def _vectorize_input(self, signal: Dict[str, Any]) -> List[float]:
        """Simple mapper from dict to 3D vector."""
        # This is a placeholder for a real embedding
        val = 0.0
        if 'value' in signal:
             val = float(signal['value'])
        return [0.1, val, 0.1] # Dummy vector

    def _create_gro_from_intent(self, intent_vector, signal) -> GenesisRequestObject:
        """Constructs a GRO based on the intent."""
        # Map Z-direction to specific intents
        direction = "unknown"
        z = intent_vector[2]

        if z > 0.8:
            direction = "growth"
        elif z < -0.8:
            direction = "pruning"
        else:
            direction = "stabilize"

        return GenesisRequestObject(
            id=f"GRO-{int(time.time())}",
            intent=direction,
            target_layer="world",
            operation="modify",
            payload={"field_type": direction, "strength": abs(z)},
            required_mastery=0.6,
            required_alignment=0.4
        )

    def _execute_genesis(self, gro: GenesisRequestObject):
        """Executes the approved GRO on the world."""
        if gro.target_layer == "world":
            payload = gro.payload
            self.world.apply_will_field(
                field_type=payload.get('field_type'),
                strength=payload.get('strength', 0.1)
            )
            logger.info(f"GENESIS EXECUTED: {gro.intent}")
