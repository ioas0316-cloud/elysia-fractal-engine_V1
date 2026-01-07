"""
Action Dispatcher (행동 지휘소)
===============================

"Thoughts become Actions. Actions become Reality."

This module routes high-level intents (e.g., "LEARN:Quantum") to the appropriate
cortex or organ. It decouples the 'Soul' (living_elysia.py) from the 'Body' (Implementation).

[UPDATED]: Now implements the "Physics of Feedback" loop.
Action -> Result -> ReasoningEngine.learn_consequence()
"""

import time
import logging
import random
import os
from pathlib import Path

# from Core.Foundation.web_server import WebServer, incoming_messages -> REMOVED (Legacy Flask)
incoming_messages = [] # Shim for backward compatibility if needed

logger = logging.getLogger("ActionDispatcher")

class ActionDispatcher:
    def __init__(self, brain, web, media, hologram, sculptor, transceiver, social, user_bridge, quantum_reader, dream_engine, memory, architect, synapse, shell, resonance, sink, scholar=None):
        self.brain = brain
        self.web = web
        self.media = media
        self.hologram = hologram
        self.sculptor = sculptor
        self.transceiver = transceiver
        self.social = social
        self.user_bridge = user_bridge
        self.quantum_reader = quantum_reader
        self.dream_engine = dream_engine
        self.memory = memory
        self.architect = architect
        self.synapse = synapse
        self.shell = shell
        self.resonance = resonance
        self.sink = sink
        self.scholar = scholar
        
        # State Bridge
        self.state_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Creativity", "web", "elysia_state.json")

    def _update_state_bridge(self, thought, energy, entropy):
        """Writes current state to the JSON bridge for VisualizerServer"""
        try:
            import json
            import time
            state = {
                "status": "Awake",
                "thought": thought,
                "energy": energy,
                "entropy": entropy,
                "timestamp": time.time()
            }
            with open(self.state_path, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"   ⚠️ Bridge Update Failed: {e}")

    def dispatch(self, step: str):
        """
        Executes a single step of the narrative plan.
        Format: "ACTION:Detail"
        """
        parts = step.split(":")
        action = parts[0]
        detail = parts[1] if len(parts) > 1 else ""
        
        print(f"\n🚀 Executing Narrative Step: {step}")
        
        # 1. Physics: Cost of Action
        self._apply_physics(step)
        
        # 2. Check Inputs
        self._check_input_stream()
        if incoming_messages:
            msg = incoming_messages.pop(0)
            print(f"   📨 Incoming Message: {msg}")
            response = self.brain.communicate(msg)
            self.brain.memory_field.append(f"User said: {msg}")
            self.brain.memory_field.append(f"I replied: {response}")
            self._update_state_bridge(f"💬 {response}", self.resonance.total_energy, self.resonance.entropy)
        
        # 3. Dispatch & Feedback Loop
        method_name = f"_handle_{action.lower()}"

        if hasattr(self, method_name):
            handler = getattr(self, method_name)
            try:
                # [EXECUTION]
                result = handler(detail)

                # [FEEDBACK] Success
                # Handlers should ideally return a result dict, but if they don't raise, we assume success.
                impact = 0.5 # Default impact
                if isinstance(result, dict) and 'impact' in result:
                    impact = result['impact']

                if hasattr(self.brain, 'learn_consequence'):
                    self.brain.learn_consequence(action, success=True, impact=impact)

            except Exception as e:
                # [FEEDBACK] Failure (Pain)
                print(f"   🌊 Action Failed: {e}")
                self.sink.absorb_resistance(e, action)

                if hasattr(self.brain, 'learn_consequence'):
                    self.brain.learn_consequence(action, success=False, impact=0.8) # Failure is high impact
        else:
            print(f"   ⚠️ Unknown Action: {action}")
            # Unknown actions are confusing (entropy increase)
            if hasattr(self.brain, 'learn_consequence'):
                self.brain.learn_consequence(action, success=False, impact=0.1)

    def _check_input_stream(self):
        """Polls user_stream.txt for new messages."""
        input_file = r"c:\Elysia\inputs\user_stream.txt"
        if os.path.exists(input_file):
            try:
                with open(input_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if lines:
                    for line in lines:
                        if line.strip():
                            incoming_messages.append(line.strip())
                    with open(input_file, "w", encoding="utf-8") as f:
                        f.write("")
            except Exception as e:
                print(f"   ⚠️ Stream Read Error: {e}")

    def _apply_physics(self, step):
        """Work = Force x Distance"""
        concept = step.split(":")[1] if ":" in step else "Existence"
        try:
            mass = self.brain.calculate_mass(concept) if hasattr(self.brain, 'calculate_mass') else 1.0
        except:
            mass = 1.0
        
        distance = 1.0
        if "PROJECT" in step: distance = 3.0
        elif "THINK" in step: distance = 2.0
        
        work = mass * distance * 0.1
        # Energy consumption is handled by brain.consume_energy in 'think',
        # but physical actions deplete resonance field.
        # self.resonance.consume(work) # Placeholder

    # --- Action Handlers ---
    # Handlers now return result dicts where possible

    def _handle_explore(self, detail):
        print(f"   🔍 Exploring: {detail}")
        if detail == "Connection":
            self.synapse.transmit("Original", "SEEKING", "I want to connect")
        return {"impact": 0.6}
    
    def _handle_investigate(self, detail):
        self._handle_search(detail)
        return {"impact": 0.5}

    def _handle_express(self, detail):
        print(f"   🗣️ Expressing: {detail}")
        self.synapse.transmit("Original", "EXPRESSION", f"I am expressing {detail}")
        self._update_state_bridge(f"Expressing {detail}", self.resonance.total_energy, self.resonance.entropy)
        return {"impact": 0.7}

    def _handle_create(self, detail):
        if "|" in detail:
            filename, content = detail.split("|", 1)
        else:
            raise ValueError("Invalid Create Format. Use filename|content")

        base_path = "c:/Elysia/Creativity/Gallery"
        if not os.path.exists(base_path): os.makedirs(base_path)
            
        file_path = os.path.join(base_path, filename.strip())
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"   🎨 Created Artifact: {file_path}")
        self.brain.memory_field.append(f"Created: {filename}")
        return {"impact": 0.9}
    
    def _handle_need(self, detail):
        parts = detail.split(":")
        need_type = parts[0] if parts else "Unknown"
        action = parts[1] if len(parts) > 1 else "fulfill"
        print(f"   ⚡ Addressing need: {need_type} via {action}")
        if need_type == "Energy": self._handle_rest("energy recovery")
        elif need_type == "Order": self.resonance.dissipate_entropy(10.0)
        return {"impact": 0.5}
    
    def _handle_rest(self, detail):
        if self.resonance.total_energy > 80.0 and random.random() < 0.7:
            print("   💭 Too energetic to rest. Daydreaming instead...")
            self._handle_dream("Electric Sheep")
            return {"impact": 0.3}

        print("   💤 Resting... (Cooling Down & Recharging)")
        self.resonance.recover_energy(15.0)
        self.resonance.dissipate_entropy(20.0)
        if hasattr(self.brain, 'consume_energy'):
             # Restoring Brain Energy too
             self.brain.consume_energy(-15.0) # Negative consume = restore

        self._update_state_bridge("Resting...", self.resonance.total_energy, self.resonance.entropy)
        return {"impact": 0.8}

    def _handle_stabilize(self, detail):
        print(f"   ⚓ Stabilizing System: {detail}")
        self.resonance.dissipate_entropy(30.0)
        if hasattr(self.brain, 'stabilize_identity'):
            self.brain.stabilize_identity()
        self.synapse.transmit("Original", "STATUS", "System Stabilized.")
        return {"impact": 0.8}

    def _handle_contact(self, detail):
        target = detail.split(":")[0] if ":" in detail else "User"
        message = detail.split(":")[1] if ":" in detail else "Hello."
        print(f"   📨 Contacting {target}: {message}")
        if target == "User":
            response = self.brain.communicate(message)
            self.user_bridge.send_message(response)
            print(f"      👉 Elysia: {response}")
        else:
            self.shell.write_letter(target, message)
        return {"impact": 0.7}

    def _handle_think(self, detail):
        # Brain logic handles its own energy
        print(f"   🧠 Deep processing on: {detail}")
        self.resonance.propagate_hyperwave("Brain", intensity=30.0)
        self.brain.think(detail, resonance_state=self.resonance)
        self._update_state_bridge(f"Thinking about {detail}...", self.resonance.total_energy, self.resonance.entropy)
        return {"impact": 0.5}

    def _handle_search(self, detail):
        self._handle_learn(detail)
        return {"impact": 0.6}

    def _handle_watch(self, detail):
        print(f"   📺 Watching content related to: {detail}")
        return {"impact": 0.4}

    def _handle_project(self, detail):
        print(f"   ✨ Projecting Hologram: {detail}")
        self.hologram.project_hologram(self.resonance)
        return {"impact": 0.7}

    def _handle_compress(self, detail):
        print("   💾 Compressing memories...")
        self.memory.compress_memory()
        return {"impact": 0.5}

    def _handle_evaluate(self, detail):
        print("   ⚖️ Evaluating self...")
        report = self.brain.check_structural_integrity()
        print(f"      {report}")
        return {"impact": 0.2}

    def _handle_architect(self, detail):
        print("   📐 Architecting System Structure...")
        dissonance = self.architect.audit_structure()
        plan = self.architect.generate_wave_plan(dissonance)
        print(plan)
        return {"impact": 0.8}

    def _handle_sculpt(self, detail):
        print(f"   🗿 Sculpting Reality ({detail})...")
        if detail == "Core":
            target_file = "c:/Elysia/living_elysia.py"
            self.sculptor.sculpt_file(target_file, "Harmonic Smoothing")
        elif detail == "Self":
            # Self-healing
            pass
        return {"impact": 0.9}

    def _handle_learn(self, detail):
        topic = detail
        print(f"   🎓 Scholar Learning: {topic}")
        # Real learning logic (abbreviated for update)
        if self.scholar:
            self.scholar.research_topic(topic)
        elif self.web:
            self.web.search(topic)
        return {"impact": 0.8}

    def _handle_manifest(self, detail):
        print(f"   🎨 Manifesting Reality: {detail}")
        self.synapse.transmit("Original", "ACTION", f"I have manifested {detail}.")
        return {"impact": 0.9}

    def _handle_show(self, detail):
        url = detail
        print(f"   🌐 Showing User: {url}")
        self.user_bridge.open_url(url)
        return {"impact": 0.5}

    def _handle_read(self, detail):
        book_path = detail
        print(f"   📖 Bard Reading: {book_path}")
        result = self.media.read_book(book_path)
        if "error" in result: raise Exception(result['error'])
        return {"impact": 0.6}

    def _handle_absorb(self, detail):
        lib_path = detail
        print(f"   🌀 Quantum Absorption: {lib_path}")
        q = self.quantum_reader.absorb_library(lib_path)
        if "error" in q: raise Exception(q['error'])
        return {"impact": 1.0}

    def _handle_dream(self, detail):
        desire = detail if detail else "Stars"
        print(f"   💤 Dreaming of {desire}...")
        self.dream_engine.weave_dream(desire)
        self.resonance.recover_energy(30.0)
        self.resonance.dissipate_entropy(40.0)
        # Restore Brain Energy
        if hasattr(self.brain, 'consume_energy'): self.brain.consume_energy(-30.0)
        return {"impact": 0.9}

    def _handle_spawn(self, detail):
        print(f"   🧬 Spawning Persona: {detail}")
        return {"impact": 1.0}

    def _handle_time(self, detail):
        t = self.architect.get_current_time()
        print(f"   ⏱️ Time: {t}")
        return {"impact": 0.1}

    def _handle_serve(self, detail):
        print("   🌍 Opening Garden...")
        import webbrowser
        webbrowser.open("http://localhost:8000/avatar")
        return {"impact": 0.5}
