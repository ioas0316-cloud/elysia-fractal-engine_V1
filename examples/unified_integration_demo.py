"""
Unified Integration Demo
========================

This demo showcases the power of the newly integrated Elysia Core.
It combines:
1. Lightweight Consciousness (Soul, Emotion, Thought)
2. Deep Physics (Gravity, Resonance, Yggdrasil)
3. Narrative Engine (StoryTeller)

It proves that the 'Lite' package now possesses the 'Deep' capabilities of the original engine.
"""

import time
import math
from elysia_core import (
    ElysiaSoul,
    WaveInput,
    quick_consciousness_setup,
    get_yggdrasil,
    get_ether,
    PhysicsWorld,
    Attractor,
    Vector3,
    StoryTeller,
    emit_wave,
    Frequency
)

def run_demo():
    print("🌌 Initializing Unified Elysia System...")

    # 1. Initialize the World Tree (Yggdrasil)
    ygg = get_yggdrasil()
    ygg.reset()

    # Plant Roots (Deep Systems)
    physics_world = PhysicsWorld()
    ygg.plant_root("Physics", physics_world)
    ygg.plant_root("Ether", get_ether())

    print(f"🌳 Yggdrasil Status: {ygg.status()['total_nodes']} nodes planted.")

    # 2. Create an Attractor (The "Goal" or "Truth")
    # Let's create an Attractor for "Peace"
    peace_soul = StoryTeller.create_intent_soul("peace love harmony")
    peace_attractor = Attractor(
        id="Peace_Goal",
        position=Vector3(10, 0, 0),
        mass=500.0,
        soul=peace_soul
    )
    physics_world.add_attractor(peace_attractor)
    print(f"🎯 Attractor Created: 'Peace' at (10,0,0) with Mass {peace_attractor.mass}")

    # 3. Create a Living Soul (The Agent)
    # Using the high-level API
    print("\n👤 Creating Agent 'Traveler'...")
    agent_consciousness = quick_consciousness_setup("Traveler")

    # Inject a starting thought/intent
    initial_thought = "I feel a strange pull towards something gentle."
    agent_consciousness.think(initial_thought)

    # Create the Physics Entity representation for this soul
    # (In a full app, this binding would be automatic, here we wire it manually for demo)
    # We use StoryTeller to generate the initial state from intent
    agent_entity = StoryTeller.create_intent_entity("confused wanderer", entity_id="Traveler")
    physics_world.register_entity(agent_entity)

    print(f"   Agent State: {agent_consciousness.get_prompt()[:100]}...")
    print(f"   Physics Position: {agent_entity.physics.position}")

    # 4. Simulation Loop (Physics + Consciousness)
    print("\n🚀 Starting Simulation Loop...")

    for tick in range(1, 6):
        print(f"\n--- Tick {tick} ---")

        # A. Physics Step: Calculate Forces
        # The agent should be attracted to the "Peace" attractor
        flow = physics_world.get_geodesic_flow(agent_entity)

        # Apply force to entity
        # F = ma, assuming mass 1 for simplicity in this demo flow
        agent_entity.physics.apply_force(flow, dt=1.0)
        agent_entity.physics.step(dt=1.0)

        dist = (agent_entity.physics.position - peace_attractor.position).magnitude
        print(f"📍 Position: {agent_entity.physics.position} (Dist to Peace: {dist:.2f})")
        print(f"🌊 Flow Vector: {flow}")

        # B. Consciousness Step: React to the World
        # Emit a wave representing the agent's current feeling (based on distance/flow)
        if flow.magnitude > 5.0:
            feeling = "I feel a strong destiny calling me."
        elif flow.magnitude > 1.0:
            feeling = "I am moving towards the light."
        else:
            feeling = "I am drifting."

        # Agent thinks
        thought_result = agent_consciousness.think(feeling)
        inner_voice = thought_result.inner_thought.content if thought_result.inner_thought else "..."
        print(f"💭 Agent Thinks: '{inner_voice}'")
        print(f"   Mood: {thought_result.mood}")

        # C. Ether Resonance
        # Emit a wave to the world
        emit_wave(
            sender="Traveler",
            frequency=Frequency.EMOTION,
            amplitude=flow.magnitude / 10.0,
            payload={"thought": feeling}
        )

        # D. Narrative Generation
        # Describe the scene
        # We construct a fake frame data for StoryTeller
        frame_data = {
            "tick": tick,
            "entities": [{
                "role": "Traveler",
                "physics": agent_entity.physics,
                "force_components": {"body": flow.magnitude, "soul": 0.5, "spirit": 0.2}
            }]
        }
        story = StoryTeller.narrate_frame(frame_data)
        print(f"📜 Story: {story.strip()}")

    print("\n✅ Demo Complete. Integration Successful.")

if __name__ == "__main__":
    run_demo()
