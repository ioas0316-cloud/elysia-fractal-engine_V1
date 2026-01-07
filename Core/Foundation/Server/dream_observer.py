# Project_Elysia/dream_observer.py



from typing import Dict, Any, List

import numpy as np



# A temporary, relative import for now. This will be solidified when the

# project structure is more mature.

import sys

import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))



from world import World



class DreamObserver:

    """

    Observes the Cellular World during an idle cycle (a 'dream') and extracts

    a summary of the key events and emotional tone.

    """



    def observe_dream(self, world: World) -> Dict[str, Any]:

        """

        Analyzes the state of the world after a dream cycle and returns a digest.



        Args:

            world: The CellularWorld instance after the dream simulation.



        Returns:

            A dictionary summarizing the dream's key aspects.

        """

        if not world or not world.cell_ids:

            return {

                "summary": "The world was quiet, a dreamless sleep.",

                "key_concepts": [],

                "emotional_landscape": "calm",

                "new_births": 0,

                "sensory": {

                    "light": "dark",

                    "temperature": "neutral",

                    "breeze": "still",

                    "scent": "neutral",

                    "wetness": "dry",

                },

            }



        # 1. Identify the most active cells (highest energy)

        # Using numpy for efficient sorting

        num_cells = len(world.cell_ids)

        top_n = min(3, num_cells)



        # We need to get the indices of living cells first

        living_indices = np.where(world.is_alive_mask[:num_cells])[0]



        if len(living_indices) == 0:

            return {

                "summary": "A silent world, with no living cells to dream.",

                "key_concepts": [],

                "emotional_landscape": "empty",

                "new_births": 0,

                "sensory": {

                    "light": "dark",

                    "temperature": "neutral",

                    "breeze": "still",

                    "scent": "neutral",

                    "wetness": "dry",

                },

            }



        energies = world.energy[living_indices]



        # Get the indices that would sort the energies in descending order

        sorted_energy_indices_local = np.argsort(energies)[::-1]



        # Map these local indices back to the world's global indices

        top_living_indices = living_indices[sorted_energy_indices_local[:top_n]]



        key_concepts = [world.cell_ids[i] for i in top_living_indices]



        # 2. Find newly born cells (not implemented in this version, would require tracking)

        # For now, we can count cells with age 0 or 1 as 'new'

        new_births = len([

            cell_id for i, cell_id in enumerate(world.cell_ids)

            if world.is_alive_mask[i] and world.quantum_states.get(cell_id, {}).get('age', 0) <= 1

        ])



        # 3. Determine the emotional landscape (placeholder logic)

        # In the future, this would involve the EmotionalCortex.

        # For now, we derive it from the top concept.

        emotional_landscape = self._deduce_emotion_from_concepts(key_concepts)



        # 4. Derive a coarse sensory snapshot from world state (light, temperature, breeze, scent, wetness)

        sensory = self._summarize_sensory(world)



        summary = f"A dream centered around '{', '.join(key_concepts)}', with a feeling of '{emotional_landscape}'."

        if sensory.get("light") == "bright_sun":

            summary += " Warm sunlight seemed to touch everything."

        elif sensory.get("light") == "dawn_dusk":

            summary += " The light felt soft, like dawn or dusk."

        elif sensory.get("light") == "night":

            summary += " It unfolded under a quiet night sky."



        if new_births > 0:

            summary += f" It felt like a moment of creation, with {new_births} new thoughts taking form."



        return {

            "summary": summary,

            "key_concepts": key_concepts,

            "emotional_landscape": emotional_landscape,

            "new_births": new_births,

            "sensory": sensory,

        }



    def _deduce_emotion_from_concepts(self, concepts: List[str]) -> str:

        """A simple placeholder to guess an emotion from concepts."""

        if not concepts:

            return "calm"



        top_concept = concepts[0].lower()

        if any(c in top_concept for c in ['love', 'joy', 'create', 'meaning']):

            return "hopeful"

        if any(c in top_concept for c in ['fear', 'shadow', 'contradiction']):

            return "introspective"

        if any(c in top_concept for c in ['reason', 'logic', 'system']):

            return "focused"



        return "neutral"



    def _summarize_sensory(self, world: World) -> Dict[str, str]:

        """Summarize coarse sensory context from the world's current state."""

        # Light

        s = float(getattr(world, "sun_intensity_global", 0.0))

        if s < 0.05:

            light = "night"

        elif s < 0.2:

            light = "dawn_dusk"

        elif s > 0.7:

            light = "bright_sun"

        else:

            light = "soft_light"



        # Temperature (Celsius)

        temp_c = float(getattr(world, "ambient_temperature_c", 15.0))

        if temp_c <= 0.0:

            temperature = "freezing_cold"

        elif temp_c <= 8.0:

            temperature = "chilly"

        elif temp_c <= 18.0:

            temperature = "cool"

        elif temp_c <= 26.0:

            temperature = "warm"

        else:

            temperature = "hot"



        # Breeze: inferred from tide + cloud cover as a soft proxy

        tide = float(getattr(world, "tide_level_global", 0.0))

        cloud = float(getattr(world, "cloud_cover", 0.0))

        breeze_intensity = abs(tide) + 0.5 * cloud

        if breeze_intensity < 0.3:

            breeze = "still"

        elif breeze_intensity < 0.8:

            breeze = "gentle_breeze"

        else:

            breeze = "strong_breeze"



        # Wetness / humidity

        humidity = float(getattr(world, "humidity", 0.5))

        try:

            wetness_mean = float(np.mean(world.wetness))

        except Exception:

            wetness_mean = 0.0

        moisture = max(humidity, wetness_mean)

        if moisture < 0.2:

            wetness = "dry"

        elif moisture < 0.6:

            wetness = "fresh"

        else:

            wetness = "damp"



        # Scent: very coarse heuristic

        try:

            fertility_mean = float(np.mean(world.soil_fertility))

        except Exception:

            fertility_mean = 0.5

        if fertility_mean > 0.7 and moisture >= 0.4:

            scent = "earthy_flower"

        elif moisture >= 0.6:

            scent = "rain_scent"

        else:

            scent = "neutral"



        return {

            "light": light,

            "temperature": temperature,

            "breeze": breeze,

            "scent": scent,

            "wetness": wetness,

        }

