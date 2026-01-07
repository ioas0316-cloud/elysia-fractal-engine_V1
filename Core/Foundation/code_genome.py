from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid
import time
from Core.Foundation.hyper_quaternion import Quaternion, HyperWavePacket

@dataclass
class CodeDNA:
    """
    The Genome of a Harmonic Thought.
    Stores the 'Harmonic Pattern' (sequence of Quaternions) that generated the code.
    This allows Elysia to 'remember' the feeling of the logic, not just the text.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = "Untitled Pattern"
    
    # The Core DNA: A sequence of wave parameters that can be re-crystallized
    harmonic_pattern: List[Dict[str, float]] = field(default_factory=list) # [{'w':..., 'x':..., 'y':..., 'z':...}, ...]
    
    # Phenotype (The Result)
    source_code: str = ""
    
    # Lineage
    generation: int = 0
    parents: List[str] = field(default_factory=list)
    
    # Epigenetics (Runtime stats)
    resonance_score: float = 0.0 # How well it resonated with the intent
    energy_cost: float = 0.0

    def add_gene(self, packet: HyperWavePacket):
        """Adds a wave packet to the genome."""
        gene = {
            'w': packet.orientation.w,
            'x': packet.orientation.x,
            'y': packet.orientation.y,
            'z': packet.orientation.z,
            'energy': packet.energy
        }
        self.harmonic_pattern.append(gene)

    def to_wave_packets(self) -> List[HyperWavePacket]:
        """Reconstructs the wave packets from the genome."""
        packets = []
        for gene in self.harmonic_pattern:
            q = Quaternion(gene['w'], gene['x'], gene['y'], gene['z'])
            packet = HyperWavePacket(energy=gene['energy'], orientation=q, time_loc=time.time())
            packets.append(packet)
        return packets

    def clone(self) -> 'CodeDNA':
        """Asexual reproduction with potential for mutation."""
        return CodeDNA(
            name=f"{self.name} (Clone)",
            harmonic_pattern=self.harmonic_pattern.copy(), # Deep copy needed if mutable
            source_code=self.source_code,
            generation=self.generation + 1,
            parents=[self.id],
            resonance_score=self.resonance_score
        )
