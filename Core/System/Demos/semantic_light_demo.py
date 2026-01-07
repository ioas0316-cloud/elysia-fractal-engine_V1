"""
Semantic Rendering Demo
=======================
"Elysia, show me 'Hope'."

This script demonstrates the Meaning-to-Light pipeline.
1. Text Input -> WaveTensor (Cognition)
2. WaveTensor -> Visual Params (Synesthesia)
3. Visual Params -> GLSL Shader Code (SDF Rendering)
"""

import sys
import os

# Path hack for standalone run
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Core.Intelligence.Intelligence.integrated_cognition_system import IntegratedCognitionSystem
from Core.Interaction.Interface.synesthetic_bridge import SynestheticBridge
from Core.Foundation.sdf_renderer import create_gtx1060_renderer

def semantic_render(concept: str, manual_wave=None):
    """
    The Full Pipeline: Concept -> Light
    """
    print(f"\n🎨 Rendering Concept: '{concept}'")
    print("-" * 40)
    
    # 1. Cognition: Get the Wave
    if manual_wave:
        wave = manual_wave
    else:
        mind = IntegratedCognitionSystem()
        mind.process_thought(concept, importance=2.0)
        wave = mind.active_thoughts[-1] 
    
    print(f"1. [Wave] Freq: {wave.active_frequencies[0]:.1f}Hz | Energy: {wave.total_energy:.2f}")
    
    # 2. Bridge: Get Visual Params
    bridge = SynestheticBridge()
    visuals = bridge.translate(wave)
    
    print(f"2. [Visual] Valence: {visuals['valence']:.2f} (Happy/Sad)")
    print(f"            Distortion: {visuals['distortionAmount']:.2f} (Chaos/Order)")
    print(f"            Color Temp: {visuals['colorTemperature']:.2f} (Warm/Cool)")
    
    # 3. Renderer: Generate Shader Config
    renderer = create_gtx1060_renderer(preset='performance')
    
    # Apply emotions to the world
    renderer.update_emotion(
        valence=visuals['valence'],
        arousal=visuals['arousal'],
        dominance=visuals['dominance']
    )
    
    config = renderer.get_three_js_material_config()
    uniforms = config['uniforms']
    
    print("3. [Renderer] GPU Uniforms sent:")
    # Note: EmotionalSDFWorld returns raw floats merged into the uniforms dict
    print(f"   - spaceScale: {uniforms['spaceScale']:.2f}")
    print(f"   - gravityStrength: {uniforms['gravityStrength']:.2f}")
    print(f"   - colorTemperature: {uniforms['colorTemperature']:.2f}")

if __name__ == "__main__":
    from Core.Foundation.Wave.wave_tensor import WaveTensor
    
    # Case A: Love (Harmonic)
    love_wave = WaveTensor("Love")
    love_wave.add_component(432.0, 1.0) # Root
    love_wave.add_component(648.0, 0.5) # Perfect 5th (Harmonic)
    semantic_render("Love and Warmth", love_wave)

    # Case B: Anxiety (Dissonant/Chaotic)
    anxiety_wave = WaveTensor("Anxiety")
    anxiety_wave.add_component(700.0, 1.0)
    anxiety_wave.add_component(715.0, 0.8) # Clashing beat (15Hz diff)
    anxiety_wave.add_component(123.0, 0.5) # Random low
    anxiety_wave.add_component(999.0, 0.5) # Random high
    semantic_render("Anxiety and Chaos", anxiety_wave)
