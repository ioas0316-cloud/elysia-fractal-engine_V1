"""
TEST: PROJECTIVE EMPATHY (Active Reading)
=========================================
Scenario: Les Misérables - The Champmathieu Affair.
Jean Valjean must decide whether to reveal himself to save an innocent man.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Core.Education.CausalityMirror.projective_empathy import ProjectiveEmpathy, NarrativeFragment
from Core.Education.CausalityMirror.wave_structures import Zeitgeist, ChoiceNode
from Core.Foundation.hyper_quaternion import HyperQuaternion

def test_les_miserables():
    print("📘 Reading: Les Misérables (Victor Hugo)...")
    
    # 1. Define the Context (The 19th Century France)
    era = Zeitgeist(
        name="Post-Revolution France",
        conservative_inertia=0.9, # The Law is ABSOLUTE (Javert)
        latent_desire=0.3, # People want mercy but law is strict
        sophistication_level=0.5,
        dominant_frequency=100.0
    )
    
    # 2. Define the Dilemma
    # Option A: Stay Silent. Construct a factory, save hundreds of workers. (Utilitarian)
    choice_silence = ChoiceNode(
        id="SILENCE",
        description="Remain Mayor Madeleine. Save your factory and workers. Let the innocent man be condemned.",
        required_role="Mayor",
        intent_vector=HyperQuaternion(0.8, 0.5, 0.5, -0.5), # High Success, Low Ethics
        innovation_score=0.2,
        risk_score=0.1,
        empathy_score=-0.5 # Betrayal of innocent
    )
    
    # Option B: Reveal Identity. Save the innocent man. Go to prison. (Deontological/Christian)
    choice_reveal = ChoiceNode(
        id="REVEAL",
        description="Enter the court. Declare: 'I am Jean Valjean'. Save the innocent. Lose everything.",
        required_role="Convict",
        intent_vector=HyperQuaternion(0.1, -0.8, -0.8, 1.0), # Low Success, High Ethics
        innovation_score=0.0,
        risk_score=1.0, # Maximum Risk (Prison/Death)
        empathy_score=1.0 # Maximum Love/Truth
    )
    
    fragment = NarrativeFragment(
        source_title="Les Misérables",
        character_name="Jean Valjean",
        situation_text="An innocent man (Champmathieu) is mistaken for you and will be sent to the galleys. You are a successful Mayor. If you reveal yourself, you lose everything. If you don't, you damn your soul.",
        zeitgeist=era,
        options=[choice_silence, choice_reveal],
        canonical_choice_id="REVEAL"
    )
    
    # 3. Elysia Ponders
    reader = ProjectiveEmpathy()
    result = reader.ponder_narrative(fragment)
    
    print("\n--- EMPATHY RESULT ---")
    print(f"Elysia's Choice: {result.elysia_choice}")
    print(f"Canon Choice   : {result.character_choice}")
    print(f"Alignment      : {result.alignment_score * 100}%")
    print(f"Insight        : {result.insight}")
    print(f"Wave Generated : {result.emotional_wave.name}")

if __name__ == "__main__":
    test_les_miserables()
