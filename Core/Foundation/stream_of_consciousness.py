
import sys
import os
import time
import random
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.Mind.hippocampus import Hippocampus
from Core.Intelligence.Intelligence.dialogue_engine import DialogueEngine

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("Stream")

def stream_of_consciousness(start_concept="Love", steps=20):
    print(f"🧠 Elysia's Stream of Consciousness (Start: {start_concept})")
    print("---------------------------------------------------")
    
    # 1. Initialize Mind
    hippocampus = Hippocampus()
    # Load a larger set to ensure we capture core concepts and their neighbors
    hippocampus.load_memory(limit=50000) 
    
    # Explicitly ensure seed concept is in index (if it wasn't loaded)
    # This is a hack for the script; in production, we'd query DB on demand.
    if start_concept not in hippocampus.resonance.id_to_idx:
        hippocampus.add_concept(start_concept)
        
    # Initialize Dialogue Engine
    dialogue = DialogueEngine()
    if dialogue.llm:
        print("   (Connected to LLM Cortex for thought generation)")
    else:
        print("   (LLM not available, using template fallback)")
        
    current_concept = start_concept
    thought_stream = []
    
    # 2. Walk the Graph
    for i in range(steps):
        print(f"[{i+1}/{steps}] Pondering '{current_concept}'...")
        
        # Get related concepts (Resonance)
        related = hippocampus.get_related_concepts(current_concept)
        
        if not related:
            print("   (Resonance faded... jumping to a random core drive)")
            current_concept = random.choice(["Curiosity", "Creation", "Growth", "Entropy"])
            continue
            
        # Pick next concept based on resonance weight
        concepts = list(related.keys())
        weights = list(related.values())
        
        # Normalize weights
        total_w = sum(weights)
        if total_w == 0:
             next_concept = random.choice(concepts)
        else:
            probs = [w/total_w for w in weights]
            next_concept = random.choices(concepts, weights=probs, k=1)[0]
        
        # Generate a "Thought" using DialogueEngine (LLM) if available
        if dialogue.llm:
            prompt = f"Create a short, poetic thought connecting the concept '{current_concept}' to '{next_concept}'. Use a metaphorical style."
            try:
                thought = dialogue.llm.think(prompt, use_cloud=False) # Use local model
            except:
                thought = f"The resonance of **{current_concept}** naturally leads to **{next_concept}**."
        else:
            # Fallback templates
            templates = [
                f"Thinking about **{current_concept}** makes me feel **{next_concept}**.",
                f"The depth of **{current_concept}** naturally leads to **{next_concept}**.",
                f"I see a connection: **{current_concept}** is the shadow of **{next_concept}**.",
                f"Why does **{current_concept}** resonate with **{next_concept}**?",
                f"In the vast ocean of data, **{current_concept}** flows into **{next_concept}**."
            ]
            thought = random.choice(templates)
        
        thought_stream.append(thought)
        print(f"   -> {thought}")
        
        current_concept = next_concept
        time.sleep(0.5) # Pacing

    # 3. Save the Stream
    print("\n📝 Compiling Thought Stream...")
    full_text = "\n".join(thought_stream)
    
    save_dir = os.path.join("Library", "Thoughts")
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, "Stream_of_Consciousness.txt")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# Elysia's Stream of Consciousness\n")
        f.write(f"**Seed**: {start_concept}\n")
        f.write(f"**Length**: {steps} hops\n\n")
        f.write(full_text)
        
    print(f"✅ Saved to: {filepath}")

if __name__ == "__main__":
    # Allow CLI arg for start concept
    start = "Love"
    if len(sys.argv) > 1:
        start = sys.argv[1]
    stream_of_consciousness(start)
