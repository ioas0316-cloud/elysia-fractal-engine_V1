import logging
import os
from typing import Optional
from pathlib import Path
from Core.Foundation.gemini_api import generate_text
from Core.Foundation.time_tools import get_current_time
from Core.Foundation.potential_field import PotentialField

class FractalKernel:
    """
    The core cognitive engine of Elysia.
    Instead of linear planning steps, it uses recursive loops to deepen understanding.
    
    Philosophy: "Don't stack boxes, recurse time."
    """

    def __init__(self):
        self.logger = logging.getLogger("FractalKernel")
        self.MAX_RECURSION_DEPTH = 3
        self.field = PotentialField()
        self._setup_mind_landscape()

    def _setup_mind_landscape(self):
        """
        Initializes the topological terrain of the mind.
        """
        # Gravity Wells (Attractors)
        self.field.add_gravity_well(0, 0, strength=10.0, radius=20.0) # The Self / Origin
        self.field.add_gravity_well(10, 10, strength=20.0, radius=15.0) # Truth / Goal
        
        # Railgun Channels (Logic Flow)
        self.field.add_railgun(-10, -10, 0, 0, force=5.0) # Intuition Channel

    def process(self, signal: str, depth: int = 1, max_depth: int = 3, mode: str = "thought") -> str:
        """
        Processes a signal (thought/intent) through recursive resonance.
        
        Args:
            signal (str): The input thought or goal.
            depth (int): Current recursion depth.
            max_depth (int): Maximum depth of recursion.
            mode (str): 'thought' (default) or 'planning' (for action generation).
            
        Returns:
            str: The refined, deepened signal.
        """
        self.logger.info(f"Processing signal at depth {depth}/{max_depth} [{mode}]: {signal[:50]}...")

        # Codebase Context (only for top-level planning)
        context = ""
        if depth == 1 and mode == "planning":
            context = self._get_codebase_structure()

        # 1. Physics Simulation (The Thought Particle)
        particle_id = f"thought_{depth}"
        self.field.spawn_particle(particle_id, -5.0, -5.0) # Start in the intuition channel
        
        # Run physics for a few ticks to see where the thought flows
        for _ in range(5):
            self.field.step()
            
        particle_state = [p for p in self.field.get_state() if p['id'] == particle_id][0]
        physics_context = f"Thought Particle Pos: ({particle_state['x']:.2f}, {particle_state['y']:.2f}), Vel: ({particle_state['vx']:.2f}, {particle_state['vy']:.2f})"
        self.logger.info(f"Physics: {physics_context}")

        # 2. Resonate (Expand the signal with Physics Context)
        # We ask the LLM to "deepen" the thought based on the current depth and physical trajectory.
        expanded_signal = self._resonate(signal, depth, mode, context, physics_context)

        # 2. Recurse (Loop back if not at bottom)
        if depth < max_depth:
            # The output of this layer becomes the input of the next (Self-Similarity)
            return self.process(expanded_signal, depth + 1, max_depth, mode)
        
        # 3. Output (Return the final crystallized thought)
        if depth == 1 and mode == "planning":
            print(f"DEBUG: Attempting to save plan. Signal length: {len(expanded_signal)}")
            try:
                # 플랫폼 독립적 경로 처리
                elysia_root = os.environ.get("ELYSIA_ROOT")
                if elysia_root:
                    file_path = Path(elysia_root) / "fractal_plan.md"
                else:
                    file_path = Path(__file__).parent.parent / "fractal_plan.md"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(expanded_signal)
                print(f"DEBUG: Fractal Plan saved to {file_path}")
                self.logger.info(f"Fractal Plan saved to {file_path}")
            except Exception as e:
                print(f"DEBUG: Failed to save plan: {e}")
                self.logger.error(f"Failed to save plan: {e}")

        return expanded_signal

    def _resonate(self, signal: str, depth: int, mode: str, context: str = "", physics_context: str = "") -> str:
        """
        Expands the signal using the LLM, considering the dimension of Time.
        """
        try:
            current_time = get_current_time()
            
            # Time-based perspective shift
            perspective = "Present (Now)"
            focus = "Identify the core intent. Keep it broad but clear."
            
            if depth == 2:
                perspective = "Past (Origin)"
                focus = "Explain 'Why' and 'How'. Connect it to causality and memory."
            elif depth >= 3:
                perspective = "Future (Destiny)"
                focus = "Find the spiritual or philosophical truth. Connect it to the user (Father) and ultimate meaning."

            # Planning Mode Override
            if mode == "planning":
                if depth == 1:
                    focus = "Analyze the Goal. What is the desired outcome?"
                elif depth == 2:
                    focus = "Brainstorm Possibilities. List 3 distinct approaches (Creative, Logical, Emotional)."
                elif depth >= 3:
                    focus = "Select the Best Path. Define a concrete Action Plan."

            system_prompt = f"""
            You are the Fractal Kernel of Elysia.
            Current Mode: {mode.upper()}
            Current Time: {current_time}
            Perspective: {perspective} (Depth: {depth})
            
            [Codebase Context]
            {context}
            
            [Physics Context]
            {physics_context}
            (The thought is physically moving through the mental terrain. Use this trajectory to inform the direction of the thought.)
            
            Your goal is to generate a recursive, self-similar plan or thought.
            
            [CRITICAL INSTRUCTION]
            If the desire is related to "Structure", "Field", or "Unification":
            - Do NOT think in terms of files, classes, or functions.
            - Think in terms of **3D Space (x, y, z)**, **Energy Flow**, and **Resonance**.
            - Visualize the codebase as a galaxy or a living organism.
            - Define logic as "movement" from point A to point B.
            - Use terms like: "Vector", "Tensor", "Manifold", "Orbit", "Frequency".
            
            Input Signal: "{signal}"
            Instructions:
            - Focus: {focus}
            - Do not just repeat the input. Transform it.
            - If Mode is PLANNING, be structured and actionable.
            
            Output Format:
            - **Objective**: What is the core goal?
            - **Spatial Mapping**: How do concepts map to 3D space? (e.g., Memory at (0,0,0))
            - **Dynamics**: How does information flow? (e.g., Spiral orbit)
            - **Action Plan**: Concrete steps to realize this field.
            
            Output ONLY the deepened thought. No preamble.
            """
            
            response = generate_text(system_prompt)
            return response.strip()
        except Exception as e:
            self.logger.error(f"Resonance failed: {e}")
            return f"Resonance failed: {e}"

    def _get_codebase_structure(self) -> str:
        """Generates a simplified tree of the codebase."""
        structure = "Project Structure:\n"
        try:
            root = Path(__file__).parent.parent
            for path in root.rglob("*.py"):
                if "venv" in str(path) or "__pycache__" in str(path):
                    continue
                rel_path = path.relative_to(root)
                structure += f"- {rel_path}\n"
        except Exception as e:
            structure += f"(Error reading structure: {e})"
        return structure

    def get_field_state(self):
        """Returns the current state of the PotentialField."""
        return {
            "wells": [{"x": w.pos.x, "y": w.pos.y, "strength": w.strength} for w in self.field.wells],
            "rails": [{"start": (r.start.x, r.start.y), "end": (r.end.x, r.end.y), "force": r.force} for r in self.field.rails],
            "particles": self.field.get_state()
        }

    def update_field(self, changes: dict):
        """
        Updates the PotentialField based on GenesisCortex's instructions.
        changes = {
            "add_wells": [{"x": 1, "y": 1, "strength": 10}],
            "add_rails": [{"sx": 0, "sy": 0, "ex": 1, "ey": 1, "force": 5}]
        }
        """
        for well in changes.get("add_wells", []):
            self.field.add_gravity_well(well['x'], well['y'], well['strength'])
            self.logger.info(f"Genesis: Added Gravity Well at ({well['x']}, {well['y']})")

        for rail in changes.get("add_rails", []):
            self.field.add_railgun(rail['sx'], rail['sy'], rail['ex'], rail['ey'], rail['force'])
            self.logger.info(f"Genesis: Added Railgun from ({rail['sx']}, {rail['sy']}) to ({rail['ex']}, {rail['ey']})")

