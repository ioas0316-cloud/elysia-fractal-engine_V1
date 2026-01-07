
import numpy as np
from typing import List, Dict, Any, Optional
from world import World
import logging

logger = logging.getLogger(__name__)

class ReservoirMesh:
    """
    Project Cerebro: The Reservoir Mesh.

    This class transforms the 'World' simulation into a Liquid State Machine (Reservoir Computer).
    It allows Elysia to 'think' using the physics of her own universe.

    Concept:
    - The World (Cells + Connections) is the Reservoir.
    - Input: Injected as Energy/HP into 'Input Cells'.
    - Dynamics: World.run_simulation_step() handles the non-linear wave propagation.
    - Output: A 'Readout' layer (linear regression) trained on the state of the world.
    """

    def __init__(self, world: World, input_nodes: int = 3, readout_nodes: int = 10):
        self.world = world
        self.input_nodes_count = input_nodes
        self.readout_nodes_count = readout_nodes

        # We need to identify specific cells to act as Input/Readout interfaces.
        # If the world is empty, we might need to seed it.
        self._ensure_neural_substrate()

        # Map logical input channels to physical cell indices
        self.input_indices = self._select_random_indices(self.input_nodes_count, seed=42)
        # Map logical readout channels to physical cell indices
        self.readout_indices = self._select_random_indices(self.readout_nodes_count, seed=99)

        # Readout weights (The only trainable part)
        # Trained via Ridge Regression in the experiment script
        self.readout_weights = None

    def _select_random_indices(self, count: int, seed: int) -> List[int]:
        """Selects stable random indices from the living population."""
        living_indices = np.where(self.world.is_alive_mask)[0]
        if len(living_indices) < count:
            # If world is too small, we just take what we have or wrap around
            if len(living_indices) == 0: return []
            return list(living_indices) * (count // len(living_indices) + 1)

        rng = np.random.RandomState(seed)
        return list(rng.choice(living_indices, size=count, replace=False))

    def _ensure_neural_substrate(self):
        """Ensures there are enough cells in the world to act as a brain."""
        if len(self.world.cell_ids) < 50:
            logger.info("CEREBRO: Seeding neural substrate (Adding DIVERSE cells)...")
            # Add random cells with diverse cultures to ensure distinct reaction dynamics
            import random
            cultures = ['wuxia', 'knight', 'animal', 'plant']
            for i in range(50 - len(self.world.cell_ids)):
                cult = random.choice(cultures)
                self.world.add_cell(f"neuron_{i}", properties={
                    'label': f'neuron_{cult}',
                    'culture': cult,
                    'vitality': random.randint(5, 20),
                    'wisdom': random.randint(5, 20)
                })

            # Forge random connections to create the 'Small World' network property
            # Essential for efficient signal propagation (The Reservoir Property)
            # To ensure Echo State Property (Fading Memory), we need rich recurrent connections.
            import random
            ids = self.world.cell_ids

            # Increase connectivity density (from 200 to 1000 edges for 50 nodes)
            # This ensures waves don't die out instantly.
            for _ in range(1000):
                src = random.choice(ids)
                tgt = random.choice(ids)
                if src != tgt:
                    # Higher weights for stronger signal transmission
                    strength = random.uniform(0.5, 1.0)
                    self.world.add_connection(src, tgt, strength=strength)

    def inject_signal(self, signal_vector: List[float]):
        """
        Injects a stimulus into the world.
        Physical Manifestation: A surge of HP/Energy AND a Ripple in the Will Field.
        """
        if not self.input_indices:
            self._ensure_neural_substrate()
            self.input_indices = self._select_random_indices(self.input_nodes_count, 42)

        for i, val in enumerate(signal_vector):
            if i < len(self.input_indices):
                idx = self.input_indices[i]
                # Signal intensity maps to massive HP boost (Hyper-stimulation)
                # We overshoot max_hp to force 'spillover' effects if implemented in world physics
                energy_surge = val * 50.0
                self.world.hp[idx] = min(self.world.max_hp[idx] * 5.0, self.world.hp[idx] + energy_surge)

                # Boost Insight as a marker of activation
                self.world.insight[idx] += val * 10.0

                # Direct Field Injection: Create a local disturbance
                # This ensures the signal propagates even if cell-to-cell logic is damping it
                pos = self.world.positions[idx]
                try:
                    x, y = int(pos[0]), int(pos[1])
                    # Imprint the signal onto the 'Value Mass' field
                    self.world._imprint_gaussian(self.world.value_mass_field, x, y, sigma=5.0, amplitude=val * 2.0)
                except Exception:
                    pass

    def harvest_state(self) -> np.ndarray:
        """
        Captures the 'High-Dimensional Echo' of the world.
        Returns a vector representing the state of the readout cells.

        State Vector = [HP, Energy, Insight, Field_Grad_X, Field_Grad_Y] concatenated
        We now include Field Gradients to capture spatial waves.
        """
        if not self.readout_indices:
            self._ensure_neural_substrate()
            self.readout_indices = self._select_random_indices(self.readout_nodes_count, 99)

        states = []
        for idx in self.readout_indices:
            # Collect multi-modal state for this neuron
            hp = self.world.hp[idx]
            energy = self.world.energy[idx]
            insight = self.world.insight[idx]

            # Field sensing (Spatial Gradients) - High entropy features
            pos = self.world.positions[idx]
            try:
                # Sense the gradient of Meaning and Will at this location
                vm_gx, vm_gy = self.world.fields.grad("value_mass", pos[0], pos[1])
                w_gx, w_gy = self.world.fields.grad("will", pos[0], pos[1])
            except Exception:
                vm_gx, vm_gy, w_gx, w_gy = 0.0, 0.0, 0.0, 0.0

            states.extend([hp, energy, insight, vm_gx, vm_gy, w_gx, w_gy])

        return np.array(states, dtype=np.float32)

    def wash_out(self, steps: int = 10):
        """Run simulation without input to settle the reservoir."""
        for _ in range(steps):
            self.world.run_simulation_step()
