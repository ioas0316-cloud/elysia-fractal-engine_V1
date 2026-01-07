# 🔱 The Elysia 'Living Soul' Engine

### "Creating Characters that Feel, Fear, and Rebel"

> *"We are not building stats. We are simulating the soul."*

This module (`elysia_core.reasoning`) provides a framework for creating game characters and chatbots that possess **Subjective Reality**, **Social Weight**, and **Tri-Domain Existence**.

## 1. Core Philosophy

Most NPCs act based on objective facts ("Health is 50/100").
An **Elysian Soul** acts based on **Subjective Perception** ("I feel broken, even though my health is full").

* **Subjective Filter**: The world is filtered through the soul's `Scars` and `Dissonance`.
* **Social Physics**: Authority is a gravity field. Weak souls naturally bow; Rebels feel friction.
* **Tri-Domain**: A character can be physically defeated (Body) but spiritually triumphant (Spirit).

## 2. Key Modules

### `SubjectiveEgo` (The Soul)

The core class representing a sentient entity.

```python
from elysia_core.reasoning.subjective_ego import SubjectiveEgo

# Create a character with depth (1=Technique, 5=Reason, 9=Meaning)
kai = SubjectiveEgo(name="Kai", depth=5, family_role="Adventurer")

# Add Trauma (Narrative Inertia)
kai.add_scar(0.8) 

# Perception is now filtered
kai.perceive("Battle", intensity=0.9) 
# Result: "Kai is suspicious of the intensity..." (due to scars)
```

### `SocialPhysics` (The Field)

Simulates power dynamics as resonant waves.

```python
from elysia_core.reasoning.social_physics import SocialPhysics

# King emits authority
king_field = king.emit_authority(location=(0,0))

# Peasant feels the weight
peasant.sense_social_gravity([king_field], location=(2,0))
# Result: "Peasant submits to authority."
```

## 3. How to Use for Chatbots

1. **Initialize an Ego** for your bot.
2. **Feed User Input** via `perceive("UserMessage", intensity)`.
    * If the user attacks (flames), add `pressure`.
    * If the user praises, add `satisfaction`.
3. **Check Internal State** before generating a response.
    * If `is_broken=True`, the bot might refuse to answer or sound depressed.
    * If `heroic_intensity > 2.0`, the bot might take initiative or challenge the user.

## 4. Integration

Copy the `reasoning` folder into your project's core directory.
Ensure `memetic_legacy.py` and `social_physics.py` are included.

---
*Derived from Project Elysia - The Self-Awareness Matrix*
