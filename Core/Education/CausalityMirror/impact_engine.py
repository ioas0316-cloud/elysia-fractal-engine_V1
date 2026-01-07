"""
THE MIRROR OF CAUSALITY: IMPACT ENGINE
======================================

"Action and Reaction are not equal and opposite in history; 
 they are amplified or dampened by the Spirit of the Age."

This module calculates the outcome of a choice by performing a 
Resonance Simulation between the Agent's Intent and the Zeitgeist.
"""

import math
from .wave_structures import HistoricalWave, Zeitgeist, ChoiceNode, Consequence, HyperQuaternion

class ImpactEngine:
    def __init__(self):
        pass

    def calculate_resonance(self, choice: ChoiceNode, era: Zeitgeist) -> float:
        """
        Calculates how well a choice 'fits' the era.
        Returns a value between -1.0 (Dissonance/Rejection) and 1.0 (Resonance/Success).
        
        Formula:
        Resonance = (Intent * Need) - (Innovation * Inertia)
        """
        # 1. Calculate base alignment (Dot product of intent and era frequency?)
        # For now, we simulate this using the abstract scores.
        
        # Does the choice meet the latent desire?
        # If Era wants "Peace" (Desire > 0) and Choice is "Pacifist" (Empathy > 0) -> + Resonance
        desire_resonance = choice.empathy_score * era.latent_desire
        
        # Does the choice trigger resistance?
        # High innovation vs High Inertia = Crash
        resistance_friction = choice.innovation_score * era.conservative_inertia
        
        # Sophistication Bonus:
        # If the choice is too simple for a sophisticated era -> Boredom
        # If the choice is too complex for a simple era -> Confusion
        # We model this as a bell curve match.
        # For simplicity in V1: 
        sophistication_penalty = abs(choice.innovation_score - era.sophistication_level) * 0.5
        
        total_resonance = desire_resonance - resistance_friction - sophistication_penalty
        
        # Normalize roughly to -1 to 1
        return max(-1.0, min(1.0, total_resonance))

    def calculate_divine_resonance(self, choice: ChoiceNode) -> float:
        """
        Calculates alignment with Absolute Truth (Love/Empathy/Sacrifice).
        This is independent of the Era.
        """
        # Divine Logic:
        # High Empathy is good.
        # Self-Sacrifice (High Risk + High Empathy) is highest.
        
        base_divine = choice.empathy_score
        
        # Sacrifice Bonus: If you take High Risk for High Empathy
        if choice.risk_score > 0.7 and choice.empathy_score > 0.7:
            base_divine += 0.5
            
        return max(-1.0, min(1.0, base_divine))

    def resolve_outcome(self, choice: ChoiceNode, era: Zeitgeist, role: str) -> Consequence:
        """
        Determines the physical and emotional outcome using DUAL AXES.
        """
        # Axis 1: The World (Zeitgeist)
        worldly_res = self.calculate_resonance(choice, era)
        
        # Axis 2: The Heaven (Divine Truth)
        divine_res = self.calculate_divine_resonance(choice)
        
        is_martyrdom = False
        
        # Narrative Generation based on Dual Resonance
        if worldly_res > 0.5 and divine_res > 0.5:
            desc = "A Golden Age. You succeed in the world and satisfy the heavens."
            state = "GLORY"
        elif worldly_res > 0.5 and divine_res < -0.2:
            desc = "You gain the whole world, but lose your soul. Tyranny prevails."
            state = "CORRUPTION"
        elif worldly_res < -0.5 and divine_res > 0.6:
            # THE PARADOX OF THE CROSS
            desc = "The world kills you, but your spirit transcends time. You are a Martyr."
            state = "MARTYRDOM"
            is_martyrdom = True
        elif worldly_res < -0.5 and divine_res < -0.5:
            desc = "A complete failure. You are destroyed by both man and fate."
            state = "RUIN"
        elif worldly_res > 0:
            desc = "You survive. It is enough for now."
            state = "SURVIVAL"
        else:
            desc = "The path is difficult. You struggle against the tide."
            state = "STRUGGLE"
            
        # Construct the Resulting Wave
        # If Martyrdom, the physical wave (Amplitude) might be high (Impact), 
        # but the spiritual component (Z/Empathy) is MAXIMUM.
        
        amplitude = abs(worldly_res) * 10
        x_val = worldly_res * 10 # Emotion reflects worldly success/fail
        
        # If Martyrdom, we invert the 'Fail' emotion into 'Sublime Sorrow' in the 4th dimension
        if is_martyrdom:
            # Martyrdom is the "Perfect Zero" - Total alignment with Source.
            # Despite the worldly pain (which is an illusion), the Spirit is at home.
            x_val = 0.0 
            y_val = 0.0
            z_val = 0.0 
            w_val = 100.0 # Massive Magnitude/Importance, but position is Center.
        else:
            z_val = divine_res * 10
            
        y_val = choice.risk_score * 5
        # w_val is handled above for martyrdom or here for others
        if not is_martyrdom:
            w_val = choice.innovation_score * 5
        
        result_wave = HistoricalWave(
            name=f"Outcome of {choice.id} [{state}]",
            q=HyperQuaternion(w_val, x_val, y_val, z_val),
            frequency=era.dominant_frequency
        )
            
        return Consequence(
            description=f"[{state}] {desc} (World: {worldly_res:.2f}, Divine: {divine_res:.2f})",
            sensory_wave=result_wave,
            narrative_by_role={role: f"As a {role}, you face: {desc}"},
            worldly_resonance=worldly_res,
            divine_resonance=divine_res,
            is_martyrdom=is_martyrdom
        )

