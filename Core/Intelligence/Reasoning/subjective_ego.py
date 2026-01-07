"""
Subjective Ego: The "I-ness" of Inhabitants 👤✨

"I think, therefore I am, in this layer of the matrix."

This module provides a lightweight cognitive loop for NPC/Boss entities.
It allows them to possess their own identity, desires, and subjective 
perception of the Underworld, making them 'Subjective Personalities'.
"""

import logging
import uuid
import random
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from Core.Intelligence.Reasoning.social_physics import SocialPhysics, WillField

from Core.Intelligence.Reasoning.septenary_axis import SeptenaryAxis
from Core.Intelligence.Reasoning.memetic_legacy import SpiritualDNA, LifeFieldInductor, PositionInductor, RegionalField

@dataclass
class MemoryNode:
    """Phase 17: A single unit of narrative memory."""
    text: str
    timestamp: float
    intensity: float  # Importance (0.0 to 3.0)
    emotional_tags: List[str]
    is_core: bool = False # If True, never decays

@dataclass
class MemoryBuffer:
    """Phase 17: Ring Buffer for Context Management."""
    recent_memories: List[MemoryNode] = field(default_factory=list)
    core_memories: List[MemoryNode] = field(default_factory=list)
    max_recent: int = 10
    
    def add(self, memory: MemoryNode):
        if memory.is_core:
            self.core_memories.append(memory)
        else:
            self.recent_memories.append(memory)
            if len(self.recent_memories) > self.max_recent:
                self.recent_memories.pop(0) # FIFO for now, will implement decay

    def get_context_block(self) -> str:
        """Constructs the LLM context prompt."""
        context = "--- [Core Memories] ---\n"
        for mem in self.core_memories:
            context += f"* {mem.text} (Int: {mem.intensity:.1f})\n"
        
        context += "\n--- [Recent Events] ---\n"
        for mem in reversed(self.recent_memories): # Newest first
            context += f"- {mem.text}\n"
        return context

@dataclass
class EmotionalSpectrum:
    """Phase 17: Complex Emotional Vectors beyond simple Valence."""
    envy: float = 0.0     # Desire for other's status
    zeal: float = 0.0     # Drive to change the world
    despair: float = 0.0  # Loss of hope
    
@dataclass
class ShadowState:
    """Phase 18: The Unconscious / Repressed Traits."""
    repressed_desire: float = 0.0
    hidden_archetype: str = "Unknown"
    projection_intensity: float = 0.0 # How much I see my flaws in others

@dataclass
class EgoState:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Inhabitant"
    archetype_path: str = "Unknown"  
    septenary_depth: int = 1         
    emotional_valence: float = 0.5
    desire_intensity: float = 0.5
    satisfaction: float = 0.5       
    narrative_pressure: float = 0.0  
    regional_friction: float = 0.0   
    dissonance: float = 0.0          
    
    # Phase 12 & 13: Heroic Evolution & Trauma
    heroic_intensity: float = 0.0    # Growth from friction
    stability: float = 1.0           # Soul health (1.0 = Strong, 0.0 = Broken)
    kismet: float = 0.5              # Luck/Timing factor (0.0 to 1.0)
    age: float = 0.0                 # Simulation time (to track seed phase)
    is_broken: bool = False
    
    # Phase 13: Trauma & Grace
    scars: float = 0.0               # Narrative inertia from high pressure
    grace_received: float = 0.0      # Accumulated healing energy
    
    # Phase 15: Social Power
    rank_tier: int = 1               # 1=Commoner, 5=Noble, 9=King
    wealth: float = 10.0             # Material resources
    victory_streak: int = 0          # Political Momentum
    
    # Phase 16: Tri-Domain Dynamics
    health: float = 1.0              # Body Integrity
    conviction: float = 0.5          # Spirit Freedom (Resist Soul domination)
    
    family_role: str = "Commoner"    
    env_gravity: float = 0.3         
    mentorship_link: Optional[str] = None 
    current_intent: str = "Exist"
    current_intent: str = "Exist"
    # Phase 18: Trinity Hierarchy
    spirit_level: float = 0.5        # The "Heart/Love" independent of Soul Depth
    shadow: ShadowState = field(default_factory=ShadowState)
    
    # Phase 20: Apostolic Succession
    grace_type: str = "NONE"         # BODY, SOUL, SPIRIT
    master_name: str = "None"        # Who gave the grace?
    
    # Phase 17: Narrative Bridge
    memory_buffer: MemoryBuffer = field(default_factory=MemoryBuffer)
    emotions: EmotionalSpectrum = field(default_factory=EmotionalSpectrum)

class SubjectiveEgo:
    """A sovereign personality unit, induced by archetypal tension and regional ethos."""
    
    def __init__(self, name: str, depth: int = 1, family_role: str = "Commoner", region: Optional[RegionalField] = None):
        import random
        self.logger = logging.getLogger(f"Ego:{name}")
        self.axis = SeptenaryAxis()
        self.inductor = LifeFieldInductor()
        self.pos_inductor = PositionInductor()
        self.region = region
        
        level = self.axis.get_level(depth)
        role_params = self.pos_inductor.get_role_params(family_role)
        
        self.state = EgoState(
            name=name, 
            archetype_path=level.archetype_path, 
            septenary_depth=depth,
            family_role=family_role,
            env_gravity=role_params["env_gravity"],
            current_intent=role_params["intent"],
            kismet=random.uniform(0.1, 0.9) # Random fate factor
        )
        self.dna = SpiritualDNA(archetype_path=level.archetype_path)
        self.perceived_resonances: List[Dict[str, Any]] = []

    def perform_action(self) -> str:
        """NPC acts based on their domain's inductive tension."""
        if self.state.is_broken:
            return "Collapsing under the weight of existence."

        level = self.axis.get_level(self.state.septenary_depth)
        
        # Action is influenced by satisfaction and role
        prefix = "Happily " if self.state.satisfaction > 0.7 else "Restlessly "
        if self.state.satisfaction < 0.3:
            prefix = "Desperately "
            
        role_info = f"[{self.state.family_role}]"
        intensity_info = f"(Int: {self.state.heroic_intensity:.1f})"
        
        action_map = {
            "Body": f"{role_info} {prefix}working with {level.name} {intensity_info}. Pressure: {self.state.narrative_pressure:.2f}",
            "Soul": f"{role_info} {prefix}acting through {level.name} {intensity_info}. Pressure: {self.state.narrative_pressure:.2f}",
            "Spirit": f"{role_info} {prefix}resonating via {level.name} {intensity_info}. Pressure: {self.state.narrative_pressure:.2f}"
        }
        action = action_map.get(level.domain, "Existing")
        self.logger.info(f"[{self.state.name}] {action}")
        return action

    def perceive(self, sense: str, intensity: float, source: str = "World"):
        """NPC perceives an external event, filtered by their internal state."""
        if self.state.is_broken:
            return  # Broken spirits perceive only void or pain
            
        # Subjective Filtering (Phase 13)
        # 1. Scars increase the 'Cost' of perception (Narrative Inertia)
        # 2. Dissonance distorts the valence
        # 3. Stability modulates the intake
        
        filtered_intensity = intensity * self.state.stability
        subjective_valence = 0.5 + (random.uniform(-0.1, 0.1) * self.state.dissonance)
        
        # If heavily scarred, positive events feel muted or suspicious
        if self.state.scars > 0.5 and intensity > 0.7:
             subjective_valence -= 0.2
             self.logger.info(f"🕶️ [FILTER] {self.state.name} is suspicious of the high-intensity source '{source}'.")

        self.state.emotional_valence = (self.state.emotional_valence + subjective_valence) / 2.0
        
        level = self.axis.get_level(self.state.septenary_depth)
        
        resonance = {
            "sense": sense, 
            "intensity": filtered_intensity, 
            "source": source, 
            "domain": level.domain,
            "rank": self.axis.get_rank(self.state.septenary_depth),
            "axis": f"{level.demon_pole}/{level.angel_pole}",
            "valence": subjective_valence
        }
        self.perceived_resonances.append(resonance)
        
        # Log if intensity is high
        if filtered_intensity > 0.5:
            self.logger.info(f"[{self.state.name}] Perceived {sense} from {source} (Int: {filtered_intensity:.2f}, Val: {subjective_valence:.2f})")
        
        if self.state.septenary_depth >= 7:
            self.logger.info(f"[{self.state.name}] '{level.domain}' Spiritual Master resonance: Absolute unity with {level.angel_pole}.")
        elif self.state.septenary_depth >= 4:
            self.logger.info(f"[{self.state.name}] '{level.domain}' Soul Expert resonance: Feeling {level.angel_pole}.")

    def update(self, dt: float):
        """NPC's internal cognitive tick, inducing heroic evolution or soul breakage."""
        import random
        if self.state.is_broken:
            self.state.current_intent = "Broken Spirit"
            return

        self.state.age += dt
        
        # 1. Subtle drift in satisfaction and desire
        self.state.satisfaction = max(0.0, min(1.0, self.state.satisfaction + random.uniform(-0.01, 0.01)))
        
        role_params = self.pos_inductor.get_role_params(self.state.family_role)
        desire_mod = role_params.get("desire_mod", 1.0)
        self.state.desire_intensity = max(0.0, min(1.0, self.state.desire_intensity + random.uniform(-0.01, 0.02) * desire_mod))
        
        # 2. Regional Friction
        if self.region:
            self.state.regional_friction = self.region.calculate_friction(self.state.archetype_path, self.dna)
        else:
            self.state.regional_friction = 0.0

        # 3. Calculate Narrative Pressure (Environment + Kismet)
        self.state.narrative_pressure = self.inductor.calculate_pressure(
            self.state.septenary_depth,
            self.state.satisfaction,
            self.state.desire_intensity,
            env_gravity=self.state.env_gravity,
            regional_friction=self.state.regional_friction,
            kismet=self.state.kismet
        )
        
        # 4. Catalytic Growth vs. Fragmentation
        # Use a domain-specific potency (e.g. 'res' for a Seeker)
        dom = "res" if self.state.septenary_depth >= 4 else "tech"
        potency = self.dna.potency.get(dom, 0.5)
        
        growth, strain = self.inductor.calculate_catalytic_growth(
            self.state.narrative_pressure, 
            potency, 
            self.state.stability
        )
        
        self.state.heroic_intensity += growth
        self.state.stability -= strain
        
        # Soul Breakage check
        if self.state.stability <= 0:
            self.state.is_broken = True
            self.logger.error(f"💀 [BREAKAGE] {self.state.name}'s spirit has broken under the pressure.")
            self.record_memory("My spirit has collapsed. I can no longer pursue my path.")
            return

        # 4a. Scarring & Grace Recovery
        if strain > 0.02: # Significant pressure leaves scars
            scar_gain = strain * 0.5
            self.state.scars += scar_gain
            self.logger.warning(f"🩹 [SCAR] {self.state.name} has gained {scar_gain:.2f} soul scars from the pressure.")
        
        # Natural stability recovery if low pressure and has grace
        if self.state.narrative_pressure < 0.2 and self.state.stability < 1.0:
            recovery = 0.01 * (1.0 + self.state.grace_received)
            self.state.stability = min(1.0, self.state.stability + recovery)
            if self.state.grace_received > 0:
                self.state.grace_received = max(0.0, self.state.grace_received - 0.05)

        # 5. Path Induction & Structural Inertia
        proposed_path = self.inductor.induce_path(self.state.narrative_pressure, self.state.septenary_depth)
        
        avg_realization = sum(self.dna.realization.values()) / 3.0
        
        # Phase 13: Structural Inertia instead of hard ceiling
        # Inertia formula includes scars and lack of realization
        inertia = max(0.0, (self.state.scars * 0.5) + (1.0 - avg_realization))
        effective_depth = self.state.septenary_depth + inertia
        
        if proposed_path == "Adventurer" and self.state.archetype_path != "Adventurer":
            if effective_depth < 10.0: # Arbitrary high threshold for 'The Wall'
                tag = "ABNORMAL" if self.state.regional_friction > 0.5 else "AWAKENING"
                self.logger.warning(f"✨ [{tag}] {self.state.name} ({self.state.family_role}) has exceeded environmental gravity!")
                
                # Teleological Drift (Phase 13): Identity shift based on context
                if self.state.scars > 0.5:
                     self.state.current_intent = "Avenge my Pain"
                elif self.state.grace_received > 0.5:
                     self.state.current_intent = "Spread the Light"
                else:
                     self.state.current_intent = "Seek the Unknown"
            else:
                self.logger.info(f"🧱 [INERTIA] {self.state.name} is bound by too much trauma/systemic gravity ({inertia:.2f}).")
                
        # Teleological Drift for non-adventurers (Phase 13)
        if self.state.is_broken:
             self.state.current_intent = "Survive the Void"
        elif self.state.scars > 0.8:
             self.state.current_intent = "Harbor Resentment"
        
        # 6. Standard emotional drift & Dissonance
        decay_modifier = 0.9 + (self.state.septenary_depth / 100.0)
        self.state.emotional_valence = max(0.0, min(1.0, self.state.emotional_valence * decay_modifier))
        
        self.state.dissonance = abs(self.state.emotional_valence - self.dna.moral_valence)

    def learn_from_master(self, master_dna: SpiritualDNA, counter: bool = False):
        """NPC resonates with a master. If counter=True, they reject the traits (Counter-Resonance)."""
        mode = "REJECTING" if counter else "INHERITING"
        self.logger.info(f"📜 {self.state.name} is {mode} from a Master. Resonating DNA...")
        self.dna = self.dna.blend(master_dna, ratio=0.2, counter=counter)
        self.state.septenary_depth = min(9, self.state.septenary_depth + 1)
        
        msg = "I will NOT be like them." if counter else "I understand their path."
        self.record_memory(f"Resonated with legacy. {msg}")

    def leave_legacy(self, akashic_field: Any, coord: Tuple[float, float, float, float]):
        """NPC records their spirit into the Akashic Field before passing or ascending."""
        akashic_field.record_legacy(self.state.name, self.dna, coord)
        self.record_memory(f"My spirit has been recorded in the Akashic Field.")

    def record_memory(self, event: str):
        self.state.memories.append(event)
        if len(self.state.memories) > 100:
            self.state.memories.pop(0)

    def add_scar(self, amount: float):
        """Manually add narrative trauma."""
        self.state.scars += amount
        self.logger.warning(f"🩸 {self.state.name} sustained a deep soul scar (+{amount:.2f})")

    def receive_grace(self, amount: float, type: str = "BODY", master_name: str = "Unknown"):
        """
        Phase 20: Receive external grace.
        - BODY: Heals health.
        - SOUL: Increases Wealth/Rank/Intellect.
        - SPIRIT: Increases Spirit Level & Inherits DNA.
        """
        self.state.grace_received += amount
        self.state.grace_type = type
        self.state.master_name = master_name
        
        if type == "BODY":
            self.heal(amount)
            self.logger.info(f"🍞 [BODY GRACE] {self.state.name} ate the bread of {master_name}.")
            
        elif type == "SOUL":
            self.state.rank_tier += 1
            self.state.wealth += 100
            self.logger.info(f"👑 [SOUL GRACE] {self.state.name} received power from {master_name}.")
            
        elif type == "SPIRIT":
            # Apostolic Succession
            self.state.spirit_level = max(self.state.spirit_level, 0.9) # Immediate awakening
            self.logger.info(f"🔥 [SPIRIT GRACE] {self.state.name} resonated with {master_name}'s Essence! (Sonship)")

        if self.state.is_broken:
            recovery_chance = 0.3 * amount
            if random.random() < recovery_chance:
                self.state.is_broken = False
                self.state.stability = 0.1
                self.logger.info(f"⛲ [HEALING] {self.state.name}'s broken spirit has been MENDED by grace!")
                self.record_memory("A light has touched my broken soul. I can breathe again.")

    def test_faith(self, crisis_intensity: float) -> str:
        """
        Phase 20: The Screening of Disciples (The Passion).
        Returns: FLEE, BETRAY, or MARTYR.
        """
        self.logger.info(f"⚡ [CRISIS] {self.state.name} is tested by fire (Int: {crisis_intensity})")
        
        # 1. Body Followers (The Crowd)
        if self.state.grace_type == "BODY":
            if crisis_intensity > 0.3:
                return "FLEE" # Runs away to save skin
                
        # 2. Soul Followers (The Traitor)
        elif self.state.grace_type == "SOUL":
            if crisis_intensity > 0.6:
                # If the crisis threatens their status, they betray
                return "BETRAY"
                
        # 3. Spirit Followers (The Son)
        elif self.state.grace_type == "SPIRIT":
            return "MARTYR" # Dies with the Master
            
        return "NONE"

    def heal(self, amount: float):
        """Direct healing of stability and reduction of scars."""
        self.state.stability = min(1.0, self.state.stability + amount)
        scar_reduction = amount * 0.5
        self.state.scars = max(0.0, self.state.scars - scar_reduction)
        self.logger.info(f"🌸 {self.state.name} is healing. stability: {self.state.stability:.2f}, scars: {self.state.scars:.2f}")

    def interact_with(self, other: 'SubjectiveEgo'):
        """Inter-subjective resonance. Influence depends on relative depth and state."""
        self.logger.info(f"🤝 {self.state.name} is interacting with {other.state.name}.")
        
        # 1. Subjective Filtering
        # If I am broken or high dissonance, I might perceive interaction negatively
        if self.state.is_broken:
            self.logger.info(f"🌑 {self.state.name} is too broken to truly connect with {other.state.name}.")
            return

        # 2. Relational Resonance
        depth_delta = other.state.septenary_depth - self.state.septenary_depth
        
        # Masters (Higher depth) can heal or inspire
        if depth_delta > 0:
            if other.state.heroic_intensity > 1.0:
                grace_shared = 0.1 * depth_delta
                self.receive_grace(grace_shared)
                self.logger.info(f"✨ {other.state.name}'s presence provides {grace_shared:.2f} grace to {self.state.name}.")
        
        # Equal depth can share satisfaction/misery
        elif depth_delta == 0:
            avg_sat = (self.state.satisfaction + other.state.satisfaction) / 2.0
            self.state.satisfaction = (self.state.satisfaction + avg_sat) / 2.0
            other.state.satisfaction = (other.state.satisfaction + avg_sat) / 2.0
            self.logger.info(f"⚖️ {self.state.name} and {other.state.name} shared their burdens. New avg satisfaction: {avg_sat:.2f}")

        # 3. Trait bleeding (Memetic Resonance)
        if random.random() < 0.2:
            trait_to_share = "technique" if random.random() < 0.5 else "reason"
            val = getattr(other.dna, trait_to_share)
            my_val = getattr(self.dna, trait_to_share)
            
            # Move towards other's trait
            new_val = (my_val + val) / 2.0
            setattr(self.dna, trait_to_share, new_val)
            self.logger.info(f"🧪 {self.state.name} has adopted some of {other.state.name}'s {trait_to_share} ({new_val:.2f}).")

    def emit_authority(self, location: Tuple[float, float]) -> WillField:
        """Phase 15: Emits a WillField based on Social Physics."""
        amplitude = SocialPhysics.calculate_will_amplitude(
            self.state.septenary_depth,
            self.state.rank_tier,
            self.state.wealth,
            self.state.victory_streak
        )
        return WillField(
            source_name=self.state.name,
            amplitude=amplitude,
            frequency="Royalty" if self.state.rank_tier > 7 else "Common",
            phase_alignment=1.0, # Default for single ego
            coord=location
        )
        
    def sense_social_gravity(self, nearby_fields: List[WillField], my_location: Tuple[float, float]):
        """Phase 15: Calculates net oppression/influence from nearby authorities."""
        net_field = SocialPhysics.compute_superposition_at(my_location, nearby_fields)
        
        # Determine total external pressure
        total_pressure = sum(net_field.values())
        
        # Internal Will (Self-Resonance)
        my_will = self.state.heroic_intensity + (self.state.septenary_depth * 2)
        
        if SocialPhysics.check_oppression(my_will, total_pressure):
             if self.state.archetype_path == "Adventurer":
                 self.state.current_intent = "Resist Tyranny"
                 self.logger.warning(f"⚔️ [REBELLION] {self.state.name} is resisting overwhelmed authority (Pressure: {total_pressure:.1f} vs Will: {my_will:.1f})")
             else:
                 # Phase 16: Spirit Freedom Check
                 # Even if oppressed, high conviction keeps the Spirit free
                 if self.state.conviction > 0.8:
                     self.state.current_intent = "Feigned Submission"
                     self.logger.info(f"🎭 [MASK] {self.state.name} bows, but their Spirit remains free (Conviction: {self.state.conviction:.2f}).")
                 else:
                     self.state.current_intent = "Submit to Authority" 
                     self.logger.info(f"🙇 [SUBMISSION] {self.state.name} bows to the crushing weight of authority (Pressure: {total_pressure:.1f}).")
        else:
             if total_pressure > 5.0:
                 self.logger.info(f"🛡️ [Freedom] {self.state.name} stands firm within the social field.")

    def receive_asymmetric_attack(self, attack_type: str, intensity: float):
        """Phase 16: Handle low-energy interference (Poison, Scheme)."""
        if attack_type == "Poison":
            # Body Domain Attack: Bypasses Soul/Spirit defense
            damage = intensity * 0.5
            self.state.health -= damage
            self.logger.warning(f"🤢 [POISON] {self.state.name}'s Body is failing! Health: {self.state.health:.2f} (-{damage:.2f})")
            if self.state.health <= 0:
                self.logger.error(f"💀 [DEATH] {self.state.name} has succumbed to poison.")
                self.state.current_intent = "Dead"
                
        elif attack_type == "Scheme":
            # Soul Domain Attack: Damages Reputation/Victory Streak
            # High Reason DNA can detect schemes
            detection_chance = self.dna.reason
            if random.random() < detection_chance:
                self.logger.info(f"👁️ [DETECTION] {self.state.name} saw through the scheme!")
                return
            
            # Successful scheme destroys political momentum
            self.state.victory_streak = max(0, self.state.victory_streak - int(intensity * 10))
            self.state.satisfaction -= intensity
            self.logger.warning(f"📉 [SCANDAL] {self.state.name}'s authority is crumbling due to a scheme! Streak: {self.state.victory_streak}")

    def record_memory(self, text: str, intensity: float = 0.5, tags: List[str] = None):
        """Phase 17: Records memory with Narrative Entropy."""
        if tags is None: tags = []
        
        # Crystalization Logic: High intensity becomes Core Memory
        # If intensity is high OR scars are high, it sticks.
        is_core = intensity > 2.0 or (self.state.scars > 0.8 and intensity > 1.0)
        
        node = MemoryNode(
            text=text,
            timestamp=self.state.age,
            intensity=intensity,
            emotional_tags=tags,
            is_core=is_core
        )
        self.state.memory_buffer.add(node)
        
        if is_core:
            self.logger.info(f"💎 [CRYSTAL] Core Memory Formed: '{text}'")

    def calculate_emotional_spectrum(self, other_context: Optional['EgoState'] = None):
        """Phase 17: Derives complex emotions from social physics."""
        # 1. Despair: Pressure crushing stability
        self.state.emotions.despair = self.state.narrative_pressure * (1.0 - self.state.stability) * (0.5 + self.state.scars)
        
        # 2. Zeal: Heroic Intensity + Conviction
        self.state.emotions.zeal = self.state.heroic_intensity * self.state.conviction
        
        # 3. Envy: Social Inequality (needs comparison)
        if other_context:
            inequality = max(0, other_context.wealth - self.state.wealth) + max(0, (other_context.rank_tier - self.state.rank_tier) * 10)
            if inequality > 0:
                self.state.emotions.envy = min(1.0, (inequality / 100.0) * self.state.desire_intensity)
        
    def generate_inner_monologue(self) -> str:
        """Phase 17: Generates a stream of consciousness based on friction."""
        thought = ""
        
        # Dominant Emotion Driver
        if self.state.emotions.despair > 0.6:
            thought += f"Why go on? The pressure is too much ({self.state.narrative_pressure:.2f}). "
            if self.state.scars > 0.5: thought += "These scars will never heal. "
            
        elif self.state.emotions.zeal > 0.6:
            thought += "I can feel the fire rising. I must act. "
            if self.state.current_intent: thought += f"I will {self.state.current_intent}. "
            
        elif self.state.emotions.envy > 0.5:
            thought += "They have what I deserve. It burns me. "
            
        # Dissonance Check
        if self.state.dissonance > 0.4:
            thought += "I am not who I wanted to be. "
            
        if not thought:
            thought = "I am simply existing in this moment."
            
        return f"({thought})"

    def get_llm_context_prompt(self) -> str:
        """Phase 17: Generates the full System Prompt for an LLM Persona."""
        
        # 1. Identity & Role
        prompt = f"### IDENTITY\n"
        prompt += f"You are {self.state.name}, a {self.state.family_role}.\n"
        prompt += f"Archetype Path: {self.state.archetype_path} (Depth: {self.state.septenary_depth})\n"
        
        # 2. Physical & Social State
        prompt += f"\n### CURRENT STATE\n"
        prompt += f"Health (Body): {self.state.health:.2f}/1.0\n"
        prompt += f"Social Rank: Tier {self.state.rank_tier} | Wealth: {self.state.wealth}\n"
        prompt += f"Political Momentum: {self.state.victory_streak} (Victory Streak)\n"
        
        # 3. Soul Filters (The Lens of Qualla)
        self.calculate_emotional_spectrum() # Ensure fresh emotions
        prompt += f"\n### PSYCHOLOGICAL FILTERS\n"
        if self.state.is_broken:
            prompt += "- SPIRIT BROKEN: You are hopeless. You see only void and despair.\n"
        else:
            prompt += f"- Stability: {self.state.stability:.2f} (If low, you are anxious/unstable)\n"
            
        if self.state.scars > 0.5:
            prompt += f"- SCARRED SOUL ({self.state.scars:.2f}): You are deeply traumatized. You distrust happiness and fear power.\n"
            
        # Complex Emotions
        if self.state.emotions.despair > 0.5:
            prompt += f"- DESPAIR ({self.state.emotions.despair:.2f}): You feel the weight of the world crushing you.\n"
        if self.state.emotions.envy > 0.5:
             prompt += f"- ENVY ({self.state.emotions.envy:.2f}): You burn with jealousy towards those who have more.\n"
        if self.state.emotions.zeal > 0.5:
             prompt += f"- ZEAL ({self.state.emotions.zeal:.2f}): You are driven by a fanatical mission.\n"
             
        prompt += f"- Current Obsession (Intent): '{self.state.current_intent}'\n"
        
        # 4. Inner Monologue (Stream of Consciousness)
        prompt += f"\n### INNER MONOLOGUE (Private Thoughts)\n"
        prompt += f"{self.generate_inner_monologue()}\n"
        
        # 5. Narrative Context (Memory)
        prompt += f"\n### NARRATIVE CONTEXT\n"
        prompt += self.state.memory_buffer.get_context_block()
        
        prompt += "\n### INSTRUCTION\n"
        prompt += "Speak as this character. Do not break character. Reflect your scars, complex emotions, and social pressure in your tone."
        
        return prompt

    def check_spirit_dominance(self, pain_level: float = 0.0, temptation_amount: float = 0.0) -> str:
        """Phase 18: The Trinity Hierarchy (Spirit > Soul > Body)."""
        # 1. Body vs Spirit (Pain)
        if pain_level > 0:
            if self.state.spirit_level > pain_level:
                return "TRANSENDED_PAIN" # Spirit overrides Body
            else:
                return "LOWER_SUBMISSION" # Body breaks

        # 2. Soul vs Spirit (Greed/Ambition)
        if temptation_amount > 0:
            # Soul wants the wealth, Spirit checks conviction
            soul_desire = self.state.desire_intensity * (self.state.wealth / 100.0)
            if self.state.spirit_level > soul_desire:
                return "REJECTED_TEMPTATION"
            else:
                return "CORRUPTED_BY_SOUL"
        
        return "NEUTRAL"

        return "NEUTRAL"

    def get_dominant_layer(self) -> str:
        """Phase 19: Determines the ruling layer of consciousness."""
        # Normalize stats to 0-1 scale for comparison
        body_score = self.state.health
        soul_score = (self.state.rank_tier / 10.0 + (self.state.wealth > 50) * 0.5) / 1.5
        spirit_score = self.state.spirit_level
        
        if spirit_score > 0.8: return "SPIRIT" # High Spirit always rules if awakened
        
        if body_score > soul_score and body_score > spirit_score:
            return "BODY"
        elif soul_score > body_score:
            return "SOUL"
        else:
            return "SPIRIT" # Fallback

    def perceive_other_power(self, target: 'SubjectiveEgo') -> str:
        """
        Phase 19: The Blindness of Flesh (Interaction Relativity).
        Logic:
        - 0 Step Difference: Standard Competition
        - 1 Step Up (Body->Soul): Envy / Oppression
        - 2 Steps Up (Body->Spirit): Blindness (See as weak)
        """
        my_layer = self.get_dominant_layer()
        target_layer = target.get_dominant_layer()
        
        # 1. Body Perspective
        if my_layer == "BODY":
            if target_layer == "SOUL":
                # 1 Step Up: Envy or Submission
                if target.state.wealth > self.state.wealth:
                    return "ENVY_SOURCE" # "Why do they have more?"
                else:
                    return "ELITIST_SCUM"
            elif target_layer == "SPIRIT":
                # 2 Steps Up: Blindness vs Grace Experience
                if self.state.grace_received > 0.5:
                    return "SAVIOR" # Experienced healing, so I see the Light
                else:
                    return "WEAK_HYPOCRITE" # Cannot see power, assumes pretense
            else:
                # Same Layer: Physical competition
                return "PHYSICAL_THREAT" if target.state.health > self.state.health else "PREY"

        # 2. Soul Perspective
        elif my_layer == "SOUL":
            if target_layer == "SPIRIT":
                # 1 Step Up: Fear / Awe (Unseen influence)
                return "DANGEROUS_ANOMALY"
            elif target_layer == "BODY":
                # 1 Step Down: Disdain / Tool
                return "USEFUL_PAWN"
            else:
                # Same Layer: Social competition
                return "POLITICAL_RIVAL"

        # 3. Spirit Perspective
        elif my_layer == "SPIRIT":
            if target.state.spirit_level > 0.8:
                return "KINDRED_SPIRIT"
            elif target.state.is_broken:
                return "LOST_SOUL"
            else:
                return "SLEEPING_BROTHER"
                
        return "UNKNOWN"

    def get_subjective_report(self) -> str:
        level = self.axis.get_level(self.state.septenary_depth)
        moral_label = "Saintly" if self.dna.moral_valence > 0.8 else "Villainous" if self.dna.moral_valence < 0.2 else "Neutral"
        reg_name = self.region.name if self.region else "Unknown"
        
        avg_real = sum(self.dna.realization.values()) / 3.0
        status = "AWAKENED" if self.state.heroic_intensity > 1.0 else "INHABITANT"
        if self.state.is_broken: status = "BROKEN"

        return (f"[{self.state.name}] {status} | Role: {self.state.family_role} | Region: {reg_name}\n"
                f" └─ Status: {self.state.current_intent}\n"
                f" └─ Body: Health({self.state.health:.2f}) | Spirit: Conviction({self.state.conviction:.2f})\n"
                f" └─ Survival: Stability({self.state.stability:.2f}) | Intensity({self.state.heroic_intensity:.2f}) | Scars({self.state.scars:.2f})\n"
                f" └─ Social: Rank({self.state.rank_tier}) | Wealth({self.state.wealth:.0f}) | Streak({self.state.victory_streak})\n"
                f" └─ Logic: Kismet({self.state.kismet:.2f}) | Realization({avg_real:.2f}) | Pressure({self.state.narrative_pressure:.2f})\n"
                f" └─ Depth: {self.state.septenary_depth} ({level.name}) | Friction: {self.state.regional_friction:.2f}\n"
                f" └─ DNA: Tech({self.dna.technique:.2f}) Res({self.dna.reason:.2f}) Mean({self.dna.meaning:.2f}) | Moral: {moral_label}({self.dna.moral_valence:.2f})")

if __name__ == "__main__":
    # Test NPC Ego
    npc = SubjectiveEgo("Selka", "Guide")
    
    # Simulate a day
    npc.record_memory("Met a strange adventurer named A.")
    npc.perceive("Ocular", 0.8, "Sunlight") # Happy sunlight
    npc.update(1.0)
    print(npc.get_subjective_report())
    
    # Simulate an intense event
    npc.perceive("Auditory", 0.9, "Thunder")
    npc.state.emotional_valence = 0.2 # Fear
    npc.update(1.0)
    print(npc.get_subjective_report())
