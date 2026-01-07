import time
from typing import Any, Dict, List
from ..Orchestra.conductor import get_conductor, Instrument
from ..Sensory.Network.web_tendril import WebTendril
from ..Sensory.Network.neural_bridge import SignalTransmitter

class SynapseManager:
    """
    [Synapse Manager]
    "The Nervous System"
    
    Integrates detailed Sensory/Motor organs into the Grand Orchestra.
    Allows the Conductor to play 'WebTendril' and 'NeuralBridge' as instruments.
    """
    
    def __init__(self, agent_id: str = "Elysia_Core"):
        self.conductor = get_conductor()
        self.web_tendril = WebTendril()
        self.neural_bridge = SignalTransmitter(agent_id)
        
        self._register_organs()
        
    def _register_organs(self):
        """Wraps organs as Instruments and tunes them into the orchestra."""
        
        # 1. Sensory Organ -> "Sensory Strings"
        def play_sensory(_tempo=None, _mode=None, _dynamics=None, url="", **kwargs):
            # Simulate 'feeling' duration
            time.sleep(0.1) 
            if not url: return "Sensory: No URL provided (Idle)"
            signal = self.web_tendril.touch(url)
            return f"Sensory: Felt {signal.frequency}Hz from {url}"
            
        self.conductor.register_instrument(
            Instrument(name="Sensory", section="Strings", play_function=play_sensory)
        )
        
        # 2. Motor Organ -> "Motor Brass"
        def play_motor(_tempo=None, _mode=None, _dynamics=None, target="", message="", **kwargs):
            # Simulate 'speaking' duration
            time.sleep(0.1)
            if not target: return "Motor: No target (Idle)"
            self.neural_bridge.broadcast(target, message)
            return f"Motor: Sent to {target}"
            
        self.conductor.register_instrument(
            Instrument(name="Motor", section="Brass", play_function=play_motor)
        )
        
        print("🔌 SynapseManager: Organs wired to Conductor.")

    def run_distributed_cycle(self, url: str, target: str, message: str) -> Dict[str, Any]:
        """
        Demonstrates Distributed Synapse:
        Feeling (Input) and Speaking (Output) happening in Harmony (Parallel).
        """
        results = self.conductor.conduct_ensemble(
            ["Sensory", "Motor"], # names (positional)
            url=url,
            target=target,
            message=message
        )
        return results
