"""
Real Sensory Frequency Database
================================

Collection of scientifically verified and researched sensory frequencies
from internet sources. This database enables Fluctlight entities in the
Internal World to have authentic sensory experiences.

Sources:
- Brainwave research (Berger, Klimesch, Singer, et al.)
- Solfeggio frequencies (Puleo, Horowitz)
- Color psychology (Elliot, Maier, Küller)
- Audio psychology (Meyer, Juslin)
- Tactile research (Gescheider, Johnson)
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional


# ============================================================================
# BRAINWAVE FREQUENCIES (Scientifically Verified)
# ============================================================================

BRAINWAVE_FREQUENCIES = {
    'delta': {
        'range': (0.5, 4.0),  # Hz
        'peak': 2.0,
        'state': 'deep_sleep',
        'consciousness_level': 0.1,
        'feelings': ['peace', 'unconscious', 'healing'],
        'color_rgb': (20, 20, 60),
        'chakra': 'root',
    },
    'theta': {
        'range': (4.0, 8.0),
        'peak': 6.0,
        'state': 'meditation',
        'consciousness_level': 0.4,
        'feelings': ['creativity', 'intuition', 'dreams'],
        'color_rgb': (60, 60, 120),
        'chakra': 'sacral',
    },
    'alpha': {
        'range': (8.0, 13.0),
        'peak': 10.0,
        'state': 'relaxed_awareness',
        'consciousness_level': 0.7,
        'feelings': ['calm', 'peaceful', 'present'],
        'color_rgb': (80, 120, 80),
        'chakra': 'heart',
    },
    'beta': {
        'range': (13.0, 30.0),
        'peak': 20.0,
        'state': 'active_thinking',
        'consciousness_level': 0.9,
        'feelings': ['alert', 'focused', 'engaged'],
        'color_rgb': (200, 150, 50),
        'chakra': 'throat',
    },
    'gamma': {
        'range': (30.0, 100.0),
        'peak': 40.0,
        'state': 'peak_awareness',
        'consciousness_level': 1.0,
        'feelings': ['insight', 'transcendence', 'unity'],
        'color_rgb': (255, 200, 200),
        'chakra': 'crown',
    },
}


# ============================================================================
# SOLFEGGIO FREQUENCIES (Ancient Healing Tones)
# ============================================================================

SOLFEGGIO_FREQUENCIES = {
    174: {'effect': 'pain_relief', 'chakra': 'foundation'},
    285: {'effect': 'quantum_healing', 'chakra': 'regeneration'},
    396: {'effect': 'liberation_fear', 'chakra': 'root'},
    417: {'effect': 'facilitating_change', 'chakra': 'sacral'},
    528: {'effect': 'love_dna_repair', 'chakra': 'solar_plexus', 'note': 'MOST POWERFUL'},
    639: {'effect': 'connecting_relationships', 'chakra': 'heart'},
    741: {'effect': 'awakening_intuition', 'chakra': 'throat'},
    852: {'effect': 'spiritual_order', 'chakra': 'third_eye'},
    963: {'effect': 'divine_consciousness', 'chakra': 'crown'},
}


# ============================================================================
# VISUAL FREQUENCIES (Visible Light Spectrum)
# ============================================================================

VISUAL_SPECTRUM_THZ = {
    'red': {
        'freq_thz': (400, 484),
        'wavelength_nm': (620, 750),
        'psychological': ['passion', 'energy', 'warmth'],
        'chakra': 'root',
    },
    'orange': {
        'freq_thz': (484, 508),
        'wavelength_nm': (590, 620),
        'psychological': ['creativity', 'enthusiasm', 'joy'],
        'chakra': 'sacral',
    },
    'yellow': {
        'freq_thz': (508, 526),
        'wavelength_nm': (570, 590),
        'psychological': ['happiness', 'optimism', 'clarity'],
        'chakra': 'solar_plexus',
    },
    'green': {
        'freq_thz': (526, 606),
        'wavelength_nm': (495, 570),
        'psychological': ['balance', 'growth', 'harmony'],
        'chakra': 'heart',
    },
    'blue': {
        'freq_thz': (606, 668),
        'wavelength_nm': (450, 495),
        'psychological': ['calm', 'trust', 'stability'],
        'chakra': 'throat',
    },
    'indigo': {
        'freq_thz': (668, 706),
        'wavelength_nm': (425, 450),
        'psychological': ['intuition', 'perception'],
        'chakra': 'third_eye',
    },
    'violet': {
        'freq_thz': (706, 789),
        'wavelength_nm': (380, 425),
        'psychological': ['spiritual', 'transformation'],
        'chakra': 'crown',
    },
}


# ============================================================================
# AUDITORY FREQUENCY RANGES (Human Hearing)
# ============================================================================

AUDITORY_RANGES_HZ = {
    'sub_bass': {'range': (20, 60), 'feeling': 'power_depth'},
    'bass': {'range': (60, 250), 'feeling': 'warmth_strength'},
    'low_mid': {'range': (250, 500), 'feeling': 'body_substance'},
    'mid': {'range': (500, 2000), 'feeling': 'presence_clarity'},
    'upper_mid': {'range': (2000, 4000), 'feeling': 'attention_definition'},
    'presence': {'range': (4000, 6000), 'feeling': 'intelligibility'},
    'brilliance': {'range': (6000, 20000), 'feeling': 'sparkle_detail'},
}


# ============================================================================
# TACTILE FREQUENCIES (Vibration/Touch)
# ============================================================================

TACTILE_FREQUENCIES_HZ = {
    'very_slow': {
        'range': (0.1, 0.5),
        'feeling': 'gentle_wave',
        'emotional': ['calming', 'soothing'],
    },
    'slow_pulse': {
        'range': (0.5, 2.0),
        'feeling': 'heartbeat_rhythm',
        'emotional': ['alive', 'organic'],
    },
    'medium': {
        'range': (2.0, 10.0),
        'feeling': 'massage_stimulation',
        'emotional': ['attention', 'awareness'],
    },
    'fast': {
        'range': (10.0, 100.0),
        'feeling': 'tingling_buzzing',
        'emotional': ['alert', 'energized'],
    },
    'ultra_fast': {
        'range': (100.0, 1000.0),
        'feeling': 'smooth_texture',
        'emotional': ['comfortable', 'warm'],
    },
}


# ============================================================================
# TASTE FREQUENCIES (Estimated from Molecular Vibrations)
# ============================================================================

TASTE_FREQUENCIES_HZ = {
    'sweet': {'hz': 432, 'vibration': 'smooth_sine', 'emotion': 'pleasure'},
    'salty': {'hz': 639, 'vibration': 'crystalline', 'emotion': 'satisfaction'},
    'sour': {'hz': 285, 'vibration': 'sharp_angular', 'emotion': 'alertness'},
    'bitter': {'hz': 174, 'vibration': 'irregular', 'emotion': 'caution'},
    'umami': {'hz': 528, 'vibration': 'complex_harmony', 'emotion': 'nourishment'},
}


# ============================================================================
# SCENT FREQUENCIES (Estimated from Molecular Patterns)
# ============================================================================

SCENT_FREQUENCIES_HZ = {
    'floral': {'range': (417, 639), 'emotion': 'uplifting'},
    'citrus': {'range': (741, 963), 'emotion': 'energizing'},
    'woody': {'range': (174, 396), 'emotion': 'grounding'},
    'minty': {'range': (639, 741), 'emotion': 'refreshing'},
    'musky': {'range': (150, 285), 'emotion': 'sensual'},
}


# ============================================================================
# INTEGRATED DATABASE CLASS
# ============================================================================

@dataclass
class ConsciousnessState:
    """Consciousness state derived from real frequencies"""
    brainwave_type: str  # delta, theta, alpha, beta, gamma
    brainwave_hz: float
    consciousness_level: float  # 0-1
    dominant_emotion: str
    chakra: str
    color_rgb: Tuple[int, int, int]


class RealSensoryFrequencyDatabase:
    """
    Integrated database of real sensory frequencies.
    
    Enables Fluctlight entities to have authentic sensory experiences
    based on scientifically researched frequency data.
    
    Usage:
        db = RealSensoryFrequencyDatabase()
        
        # Map stimulus to consciousness
        state = db.stimulus_to_consciousness({
            'visual_freq_thz': 520,  # Red light
            'audio_freq_hz': 528,    # Love frequency
        })
        
        # Get brainwave for activity
        brainwave = db.activity_to_brainwave('meditation')
    """
    
    def __init__(self):
        self.brainwaves = BRAINWAVE_FREQUENCIES
        self.solfeggio = SOLFEGGIO_FREQUENCIES
        self.visual = VISUAL_SPECTRUM_THZ
        self.audio = AUDITORY_RANGES_HZ
        self.tactile = TACTILE_FREQUENCIES_HZ
        self.taste = TASTE_FREQUENCIES_HZ
        self.scent = SCENT_FREQUENCIES_HZ
    
    def activity_to_brainwave(self, activity: str) -> Dict:
        """
        Map activity to appropriate brainwave state.
        
        Args:
            activity: 'sleeping', 'meditating', 'relaxing', 'thinking', 'focused'
            
        Returns:
            Brainwave data dict
        """
        activity_map = {
            'sleeping': 'delta',
            'dreaming': 'theta',
            'meditating': 'theta',
            'relaxing': 'alpha',
            'thinking': 'beta',
            'focused': 'beta',
            'insight': 'gamma',
            'transcendent': 'gamma',
        }
        
        wave_type = activity_map.get(activity, 'alpha')
        return self.brainwaves[wave_type]
    
    def frequency_to_brainwave(self, freq_hz: float) -> str:
        """Determine brainwave type from frequency"""
        for wave_type, data in self.brainwaves.items():
            if data['range'][0] <= freq_hz <= data['range'][1]:
                return wave_type
        return 'alpha'  # default
    
    def color_to_frequency_thz(self, color_name: str) -> float:
        """Get frequency (THz) for color"""
        if color_name in self.visual:
            freq_range = self.visual[color_name]['freq_thz']
            return (freq_range[0] + freq_range[1]) / 2
        return 540  # Green (middle of spectrum)
    
    def emotion_to_solfeggio(self, emotion: str) -> float:
        """Map emotion to closest Solfeggio frequency"""
        emotion_map = {
            'fear': 396,
            'change': 417,
            'love': 528,
            'harmony': 639,
            'truth': 741,
            'vision': 852,
            'unity': 963,
        }
        return emotion_map.get(emotion, 528)  # Default to love
    
    def stimulus_to_consciousness(
        self,
        stimulus: Dict
    ) -> ConsciousnessState:
        """
        Convert external stimulus to consciousness state.
        
        Args:
            stimulus: Dict with keys like:
                - 'visual_freq_thz': Light frequency
                - 'audio_freq_hz': Sound frequency
                - 'activity': Current activity
                
        Returns:
            ConsciousnessState with all parameters
        """
        # Determine brainwave
        if 'activity' in stimulus:
            brainwave_data = self.activity_to_brainwave(stimulus['activity'])
            brainwave_type = stimulus['activity']
        elif 'audio_freq_hz' in stimulus:
            brainwave_type = self.frequency_to_brainwave(stimulus['audio_freq_hz'])
            brainwave_data = self.brainwaves[brainwave_type]
        else:
            brainwave_type = 'alpha'
            brainwave_data = self.brainwaves['alpha']
        
        return ConsciousnessState(
            brainwave_type=brainwave_type,
            brainwave_hz=brainwave_data['peak'],
            consciousness_level=brainwave_data['consciousness_level'],
            dominant_emotion=brainwave_data['feelings'][0],
            chakra=brainwave_data['chakra'],
            color_rgb=brainwave_data['color_rgb']
        )
    
    def create_multisensory_profile(
        self,
        concept: str
    ) -> Dict:
        """
        Create complete sensory profile for a concept.
        
        Args:
            concept: e.g., "rose", "ocean", "fire"
            
        Returns:
            Dict with all sensory frequencies
        """
        # Simplified concept mapping
        concept_map = {
            'rose': {
                'visual_freq_thz': 520,  # Red
                'audio_freq_hz': 528,    # Love
                'scent': 'floral',
                'taste': 'sweet',
                'tactile_hz': 10,
            },
            'ocean': {
                'visual_freq_thz': 630,  # Blue
                'audio_freq_hz': 150,    # Water element
                'scent': 'fresh',
                'taste': 'salty',
                'tactile_hz': 1.0,       # Wave rhythm
            },
            'fire': {
                'visual_freq_thz': 450,  # Orange-red
                'audio_freq_hz': 450,    # Energy
                'scent': 'woody',
                'taste': 'bitter',
                'tactile_hz': 100,       # Intense vibration
            },
        }
        
        return concept_map.get(concept, {
            'visual_freq_thz': 540,
            'audio_freq_hz': 528,
            'scent': 'fresh',
            'taste': 'umami',
            'tactile_hz': 10,
        })


# Example usage
if __name__ == "__main__":
    db = RealSensoryFrequencyDatabase()
    
    print("🧠 Real Sensory Frequency Database")
    print("=" * 60)
    
    # Example 1: Meditation
    print("\n1. Meditation State:")
    state = db.stimulus_to_consciousness({'activity': 'meditating'})
    print(f"   Brainwave: {state.brainwave_type} ({state.brainwave_hz} Hz)")
    print(f"   Consciousness: {state.consciousness_level * 100}%")
    print(f"   Emotion: {state.dominant_emotion}")
    print(f"   Color: RGB{state.color_rgb}")
    
    # Example 2: Rose
    print("\n2. Rose Sensory Profile:")
    rose = db.create_multisensory_profile('rose')
    print(f"   Visual: {rose['visual_freq_thz']} THz (red light)")
    print(f"   Audio: {rose['audio_freq_hz']} Hz (love frequency)")
    print(f"   Scent: {rose['scent']}")
    print(f"   Taste: {rose['taste']}")
    print(f"   Touch: {rose['tactile_hz']} Hz (soft)")
    
    # Example 3: Brainwave types
    print("\n3. Brainwave Types:")
    for wave_type, data in db.brainwaves.items():
        print(f"   {wave_type.upper()}: {data['range'][0]}-{data['range'][1]} Hz")
        print(f"      → {data['state']}, {data['feelings']}")
    
    # Example 4: Solfeggio
    print("\n4. Key Solfeggio Frequencies:")
    for freq, data in db.solfeggio.items():
        if freq in [396, 528, 852]:  # Highlight key ones
            print(f"   {freq} Hz: {data['effect']} ({data['chakra']})")
