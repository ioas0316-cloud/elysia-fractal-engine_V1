"""
Reality Perception System
=========================

"The Bridge between Physical Signals and Digital Sensation"

This system converts raw physical world data (frequencies) into 
Elysia's internal sensory format.

It implements the P5 philosophy:
"Perceiving the world as Vibrations and Frequencies."
"""

import logging
import time
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

try:
    from Core.Interaction.Sensory.real_frequency_database import RealSensoryFrequencyDatabase
    from Core.Interaction.Sensory.five_senses_mapper import SensoryExperience, VisualProperties, AudioProperties
except ImportError:
    # Fallback for standalone testing
    from real_frequency_database import RealSensoryFrequencyDatabase
    # Mock dataclasses if standard import fails
    @dataclass
    class VisualProperties:
        hue: float; saturation: float; brightness: float; opacity: float; glow: float
    @dataclass
    class AudioProperties:
        frequency: float; volume: float; timbre: str; tempo: float; reverb: float
    @dataclass
    class SensoryExperience:
        visual: VisualProperties; audio: AudioProperties; haptic: Any = None

logger = logging.getLogger("RealityPerception")

@dataclass
class IntegratedPerception:
    """A complete moment of perception"""
    visual: VisualProperties
    audio: AudioProperties
    dominant_frequency_hz: float
    dominant_color_thz: float
    emotional_tone: str
    interpretation: str
    timestamp: float

class RealityPerceptionSystem:
    def __init__(self):
        self.db = RealSensoryFrequencyDatabase()
        self.active = True
        logger.info("👁️ Reality Perception System Initialized (Frequency-Based)")

    def perceive_light(self, r: int, g: int, b: int) -> VisualProperties:
        """
        Convert RGB input to Visual Sensation using Frequency Mapping.
        
        Physics:
        Red (~430-480 THz)
        Green (~540-580 THz)
        Blue (~610-670 THz)
        """
        # 1. Normalize
        r_n, g_n, b_n = r/255.0, g/255.0, b/255.0
        
        # 2. Calculate Hue/Sat/Val (Standard conversion)
        c_max = max(r_n, g_n, b_n)
        c_min = min(r_n, g_n, b_n)
        delta = c_max - c_min
        
        # Hue Calculation
        if delta == 0:
            h = 0
        elif c_max == r_n:
            h = 60 * (((g_n - b_n) / delta) % 6)
        elif c_max == g_n:
            h = 60 * (((b_n - r_n) / delta) + 2)
        elif c_max == b_n:
            h = 60 * (((r_n - g_n) / delta) + 4)
            
        # Saturation/Brightness
        s = 0 if c_max == 0 else delta / c_max
        v = c_max
        
        # 3. Map to THz for "Feeling"
        # We approximate THz based on Hue
        # 0 (Red) -> 450 THz
        # 120 (Green) -> 550 THz
        # 240 (Blue) -> 650 THz
        # 300 (Violet) -> 750 THz
        
        # Simple Linear mapping for internal logic (not strict physics)
        apparent_thz = 450 + (h / 300) * 300 
        
        # 4. Determine Emotional Tone from DB
        # Find closest match in valid spectrum
        color_name = "green" # Default
        if h < 30 or h > 330: color_name = "red"
        elif h < 60: color_name = "orange"
        elif h < 90: color_name = "yellow"
        elif h < 150: color_name = "green"
        elif h < 210: color_name = "cyan" # approximate
        elif h < 270: color_name = "blue"
        elif h < 330: color_name = "violet"
        
        # Retrieve psychological data
        color_data = self.db.visual.get(color_name, {})
        feelings = color_data.get('psychological', ['neutral'])
        
        return VisualProperties(
            hue=h,
            saturation=s,
            brightness=v,
            opacity=1.0, # Real reality is solid
            glow=0.0
        ), color_name, feelings

    def perceive_sound(self, fft_data: List[int], sample_rate: int = 44100) -> AudioProperties:
        """
        Convert FFT spectrum to Audio Sensation.
        """
        if not fft_data:
            return AudioProperties(0, 0, 'pure', 60, 0), 0, "silence"

        # 1. Find Weak/Strong Frequencies
        # Simplified: Find peak bin
        peak_bin = np.argmax(fft_data)
        peak_val = fft_data[peak_bin]
        
        # Calculate Frequency
        # Freq = bin * sample_rate / fft_size
        # Assuming typical web audio fftSize=1024 (bin_count=512) -> max freq = sample_rate/2
        # We need the fft_size from the caller usually. 
        # But for 'relative' sensation, we can just use bin index as a proxy for pitch.
        # Let's assume passed data is pre-processed or we treat it as generic buckets.
        
        # For this implementation, we assume fft_data IS the frequency strengths
        # and we map 'bin index' to approximate 0-20kHz
        
        bin_count = len(fft_data)
        nyquist = sample_rate / 2
        freq_per_bin = nyquist / bin_count
        
        dominant_freq = peak_bin * freq_per_bin
        
        # 2. Volume
        volume = np.mean(fft_data) / 255.0 # Assuming 8-bit data
        
        # 3. Timbre Analysis (Harmonic Complexity)
        # Check for multiple peaks
        peaks = np.where(np.array(fft_data) > 100)[0]
        timbre = 'pure'
        if len(peaks) > 5: timbre = 'harmonic'
        if len(peaks) > 15: timbre = 'complex'
        if volume > 0.8: timbre = 'distorted'
        
        # 4. Map to Emotional/Spiritual Tone
        # Check Solfeggio proximity
        closest_solfeggio = min(self.db.solfeggio.keys(), key=lambda x: abs(x - dominant_freq))
        solfeggio_dist = abs(dominant_freq - closest_solfeggio)
        
        tone_description = "noise"
        if solfeggio_dist < 10: # Close match
            s_data = self.db.solfeggio[closest_solfeggio]
            tone_description = f"{closest_solfeggio}Hz ({s_data['effect']})"
        elif volume < 0.1:
            tone_description = "silence"
        else:
            # Check range
            for r_name, r_data in self.db.audio.items():
                if r_data['range'][0] <= dominant_freq <= r_data['range'][1]:
                    tone_description = r_data['feeling']
                    break
        
        return AudioProperties(
            frequency=dominant_freq,
            volume=volume,
            timbre=timbre,
            tempo=0, # Hard to detect from single frame
            reverb=0
        ), dominant_freq, tone_description

    def integrate(self, 
                 visual_input: Optional[Tuple[int, int, int]] = None,
                 audio_input: Optional[List[int]] = None) -> IntegratedPerception:
        """
        Synthesize a complete moment of reality perception.
        """
        # Default empty states
        vis_prop = VisualProperties(0,0,0,0,0)
        dom_color_thz = 0
        vis_feelings = []
        
        aud_prop = AudioProperties(0,0,'pure',0,0)
        dom_freq_hz = 0
        tone_desc = "silence"
        
        # Process Visual
        if visual_input:
            r, g, b = visual_input
            vis_prop, color_name, vis_feelings = self.perceive_light(r, g, b)
            dom_color_thz = self.db.color_to_frequency_thz(color_name)
            
        # Process Audio
        if audio_input:
            aud_prop, dom_freq_hz, tone_desc = self.perceive_sound(audio_input)
            
        # Synthesize Meaning
        # "I see [Red] and hear [Low Bass] -> Danger?"
        # "I see [Blue] and hear [Birds/High] -> Peace?"
        
        summary = f"Sensing {tone_desc}"
        if visual_input:
            summary += f" bathed in {vis_feelings[0]} light"
            
        return IntegratedPerception(
            visual=vis_prop,
            audio=aud_prop,
            dominant_frequency_hz=dom_freq_hz,
            dominant_color_thz=dom_color_thz,
            emotional_tone=vis_feelings[0] if vis_feelings else "neutral",
            interpretation=summary,
            timestamp=time.time()
        )
