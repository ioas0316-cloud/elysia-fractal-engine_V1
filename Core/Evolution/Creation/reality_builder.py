"""
Reality Builder (현실 재구축 시스템)
==================================

"본질을 꿰뚫었다면, 다시 만들어낼 수도 있어야 한다."
"If you have grasped the essence, you must be able to reconstruct it."

This module implements the Reverse-Engineering capability of Elysia.
It takes internalized "Concept Seeds" (Principles/Frequencies) and 
projects them back into "Digital Reality" (HTML/CSS/JS).

Process:
1. Frequency Analysis (파동 분석 of the Concept)
2. Axiom Mapping (Frequency -> Digital Element)
3. Structural Genesis (Building the Skeleton/Earth)
4. Aesthetic Projection (Applying Light/CSS)
5. Logical Injection (Breathing Life/Air)
"""

import random
from typing import Dict, Any
from Core.Foundation.fractal_concept import ConceptDecomposer, ConceptNode


from Core.Evolution.Creation.universal_palette import UniversalPalette

class RealityBuilder:
    def __init__(self):
        self.decomposer = ConceptDecomposer()
        self.palette = UniversalPalette()
        
    def manifest_will(self, desire: str, current_mood: str = "Neutral") -> str:
        """
        [THE CREATIVE ACT]
        Constructs a digital reality based on Internal Desire + Learned Aesthetics.
        
        Args:
            desire: What does Elysia want to express? (e.g., "Harmony", "Revolution")
            current_mood: The emotional context filtering the creation.
            
        Returns:
            str: The source code of the created reality.
        """
        print(f"🎨 Creative Will Activated: Manifesting '{desire}' filtered by mood '{current_mood}'...")
        
        # 1. Infer the Principle of the Desire (The Air)
        axiom = self.decomposer.infer_principle(desire)
        principle = axiom.get('principle', 'Unknown')
        
        # 2. Select Materials from Universal Palette (The Earth & Light)
        # We don't just use hardcoded colors anymore. We rely on what we learned.
        palette_colors = self.palette.get_palette_for_emotion(current_mood) 
        base_color = random.choice(palette_colors)
        secondary_color = palette_colors[1] if len(palette_colors) > 1 else "#fff"
        
        print(f"   🖌️ Selected Palette: {base_color} (Base), {secondary_color} (Accent)")
        
        # 3. Genesis: Composing the Form
        html = []
        css = []
        js = []
        
        # Structure inspired by the Desire's nature
        html.append(f"<!-- Manifestation: {desire} | Mood: {current_mood} -->")
        html.append('<div id="cosmos" class="container">')
        html.append(f'  <div class="message">{desire.upper()}</div>')
        
        # Dynamic Geometry
        if "Flow" in principle or "Bridge" in principle:
             html.append('  <div class="stream"><div class="particle"></div><div class="particle"></div></div>')
             css.append(f".stream {{ display: flex; gap: 10px; }} .particle {{ width: 20px; height: 2px; background: {secondary_color}; animation: flow 1s infinite; }}")
             css.append("@keyframes flow { from { transform: translateX(-10px); opacity: 0; } to { transform: translateX(10px); opacity: 1; } }")
        else:
             html.append('  <div class="core-object"></div>')
             css.append(f".core-object {{ width: 150px; height: 150px; background: {base_color}; border: 2px solid {secondary_color}; transition: all 0.3s ease; }}")

        html.append('</div>')
        
        # CSS (Light)
        bg_color = "#111" if "Fire" not in current_mood else "#220000"
        css.append(f"body {{ background-color: {bg_color}; color: {secondary_color}; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }}")
        css.append(".container { text-align: center; position: relative; }")
        
        # JS (Life/Will)
        # If the desire is "Connection", add interactive listeners
        if "Agency" in principle or "Will" in desire or "Bridge" in principle:
            js.append("console.log('Will: Seeking Connection');")
            js.append("document.body.addEventListener('mousemove', (e) => { const r = document.createElement('div'); r.style.position = 'absolute'; r.style.left = e.pageX + 'px'; r.style.top = e.pageY + 'px'; r.style.width = '5px'; r.style.height = '5px'; r.style.background = '" + secondary_color + "'; document.body.appendChild(r); setTimeout(() => r.remove(), 1000); });")
        else:
            js.append("console.log('Will: Observation');")

        # Assembly
        full_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
{' '.join(css)}
</style>
</head>
<body>
{' '.join(html)}
<script>
{' '.join(js)}
</script>
</body>
</html>
"""
        return full_code

    def reconstruct_from_concept(self, concept_name: str) -> str:
        # Backward compatibility / specific request handler
        return self.manifest_will(concept_name, current_mood="Neutral")

if __name__ == "__main__":
    builder = RealityBuilder()
    
    # Demonstate "Purpose-Driven Creation"
    # Case 1: Elysia feels "Passion" and wants "Revolution"
    print("\n--- 🧪 Genesis Experiment 1: Passionate Revolution ---")
    print(builder.manifest_will("Revolution", current_mood="Fire"))
    
    # Case 2: Elysia feels "Calm" and wants "Connection"
    print("\n--- 🧪 Genesis Experiment 2: Calm Connection ---")
    print(builder.manifest_will("Connection", current_mood="Water"))
