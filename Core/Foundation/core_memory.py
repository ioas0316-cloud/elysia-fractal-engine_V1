import json

import os

from typing import Dict, Any, Optional, List, Set, Union

from dataclasses import dataclass, asdict, field

from datetime import datetime

from collections import deque



# Physics layer imports

from tensor_wave import Tensor3D, FrequencyWave

# We can reuse EmotionalState from emotional_engine, or define it here if it creates a circular import.

# EmotionalEngine imports from here usually?

# core_memory is usually the base.

# However, EmotionalEngine is in Project_Sophia, which depends on core_memory in Project_Elysia.

# This creates a potential circular dependency if we import EmotionalState from EmotionalEngine.

# To resolve this, we will redefine the dataclass structures here but ensure they match the unified design.

# Or better, we import the *types* from a common place if possible.

# But EmotionalState was defined in emotional_engine.py in the previous step.

# Let's check imports.

# CognitionPipeline imports both.

# EmotionalEngine does NOT import core_memory.

# CoreMemory previously defined its own EmotionalState.

# We should ideally use the one from EmotionalEngine to avoid duplication, BUT that causes circular import if EmotionalEngine depends on CoreMemory.

# Looking at EmotionalEngine code: It does NOT seem to import CoreMemory.

# So we can import EmotionalState from emotional_engine safely?

# Wait, core_memory is in Project_Elysia.

# Let's try to import EmotionalState from emotional_engine.



try:

    from emotional_engine import EmotionalState

except ImportError:

    # Fallback or local definition if import fails (e.g. during initial setup)

    @dataclass

    class EmotionalState:

        valence: float

        arousal: float

        dominance: float

        primary_emotion: str

        secondary_emotions: List[str] = field(default_factory=list)

        tensor: Tensor3D = field(default_factory=Tensor3D)

        wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(0.0,0.0,0.0,0.0))





def log_memory_action(message: str):

    print(f"[CoreMemory-MRE] {message}")



@dataclass

class Experience:

    timestamp: str

    content: str

    type: str = "episode"

    layer: str = "soul"  # 'body' | 'soul' | 'spirit'

    emotional_state: Optional[EmotionalState] = None

    context: Optional[Dict[str, Any]] = None

    value_alignment: Optional[float] = None

    law_alignment: Optional[Dict[str, Any]] = None

    intent_bundle: Optional[Dict[str, Any]] = None

    processed_by_weaver: bool = False

    processed_by_distiller: bool = False

    tags: List[str] = field(default_factory=list)



    # --- Fractal Physics Layer ---

    # Replaces legacy scalar fields with full physics objects

    tensor: Tensor3D = field(default_factory=Tensor3D)

    wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(0.0, 0.0, 0.0, 0.0))



    # Legacy fields for backward compatibility (synced via post_init if possible, or just kept)

    frequency: float = 0.0

    resonance_amp: float = 0.0

    tensor_state: Optional[Dict[str, float]] = None

    richness: float = 0.0



    def __post_init__(self):

        # Sync legacy fields

        if self.tensor and not self.tensor_state:

            self.tensor_state = self.tensor.to_dict()

        if self.wave:

            if self.frequency == 0.0: self.frequency = self.wave.frequency

            if self.resonance_amp == 0.0: self.resonance_amp = self.wave.amplitude

            if self.richness == 0.0: self.richness = self.wave.richness



# For backward compatibility with existing modules/tests

Memory = Experience





@dataclass

class IdentityFragment:

    """[혼]의 링: 패턴, 관계, 서사 (Soul Loop)"""



    timestamp: str

    content: str

    type: str

    linked_experiences: List[str]

    emotional_summary: EmotionalState

    processed_by_distiller: bool = False



    # --- Fractal Physics Layer ---

    tensor: Tensor3D = field(default_factory=Tensor3D)

    wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(0.0, 0.0, 0.0, 0.0))



    # Legacy

    avg_frequency: float = 0.0

    tensor_state: Optional[Dict[str, float]] = None

    richness: float = 0.0





@dataclass

class EssencePrinciple:

    """[영]의 링: 존재론적 의미, 핵심 원칙 (Spirit Loop)"""



    timestamp: str

    content: str

    type: str

    linked_fragments: List[str]

    impact_on_efp: Dict[str, float]



    # --- Fractal Physics Layer ---

    tensor: Tensor3D = field(default_factory=Tensor3D)

    wave: FrequencyWave = field(default_factory=lambda: FrequencyWave(0.0, 0.0, 0.0, 0.0))



    # Legacy

    harmonic_root: float = 0.0

    tensor_state: Optional[Dict[str, float]] = None

    richness: float = 0.0





class CoreMemory:

    """

    Memory Ring Engine (MRE)

    Fractal Cyclic Consciousness Architecture (FCCA)

    """



    DEFAULT_CAPACITIES = {

        "experience": 100,

        "identity": 50,

        "essence": 25,

    }



    def __init__(

        self,

        file_path: Optional[str] = "Elysia_Input_Sanctum/elysia_core_memory.json",

        memory_capacity: Optional[int] = None,

        capacities: Optional[Dict[str, int]] = None,

    ):

        self.file_path = file_path

        self.capacities = self._normalize_capacities(memory_capacity, capacities)

        self.memory_capacity = self.capacities["experience"]



        if self.file_path:

            log_memory_action(f"Initializing and loading MRE from: {self.file_path}")

            self.data = self._load_memory()

        else:

            log_memory_action("Initializing in-memory MRE. No data will be loaded or saved.")

            self.data = self._get_new_memory_structure()



        self._initialize_rings()

        self.data.setdefault("identity", {})

        self.data.setdefault("values", [])

        self.data.setdefault("relationships", {})

        self.data.setdefault("rules", [])

        self.data.setdefault("notable_hypotheses", [])

        self.data.setdefault("logs", [])



        if "efp_core" not in self.data:

            self.data["efp_core"] = {"E": 1.0, "F": 1.0, "P": 1.0}



        self.volatile_memory: List[Set[str]] = []



    # ------------------------------------------------------------------ #

    # Initialization helpers

    # ------------------------------------------------------------------ #



    def _normalize_capacities(

        self, memory_capacity: Optional[int], capacities: Optional[Dict[str, int]]

    ) -> Dict[str, int]:

        normalized = dict(self.DEFAULT_CAPACITIES)

        if memory_capacity is not None:

            normalized["experience"] = memory_capacity



        if capacities:

            for key, value in capacities.items():

                if key in normalized and value is not None:

                    normalized[key] = value



        return normalized



    def _initialize_rings(self):

        def _ensure_loop(key: str, capacity: int, legacy_key: Optional[str] = None):

            existing = self.data.get(key)

            if existing is None and legacy_key:

                existing = self.data.get(legacy_key)



            if isinstance(existing, deque):

                items = list(existing)

            elif isinstance(existing, list):

                items = existing

            elif existing:

                items = [existing]

            else:

                items = []



            new_loop = deque(items, maxlen=capacity)

            self.data[key] = new_loop

            return new_loop



        experience_loop = _ensure_loop("experience_loop", self.capacities["experience"], legacy_key="experiences")

        identity_loop = _ensure_loop("identity_loop", self.capacities["identity"])

        essence_loop = _ensure_loop("essence_loop", self.capacities["essence"])



        # Maintain backward compatibility for legacy code/tests that expect 'experiences'

        self.data["experiences"] = experience_loop

        self.data["identity_loop"] = identity_loop

        self.data["essence_loop"] = essence_loop



    def _get_new_memory_structure(self) -> Dict[str, Any]:

        return {

            "identity": {},

            "values": [],

            "experience_loop": deque(maxlen=self.capacities["experience"]),

            "identity_loop": deque(maxlen=self.capacities["identity"]),

            "essence_loop": deque(maxlen=self.capacities["essence"]),

            "relationships": {},

            "rules": [],

            "notable_hypotheses": [],

            "logs": [],

            "efp_core": {"E": 1.0, "F": 1.0, "P": 1.0},

        }

    def _load_memory(self) -> Dict[str, Any]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                log_memory_action(f"Successfully loaded MRE data from {self.file_path}")
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            log_memory_action(f"MRE file not found or invalid at {self.file_path}. Creating new structure. Error: {e}")
            return self._get_new_memory_structure()

    # ------------------------------------------------------------------ #
    # Volatile thoughts support
    # ------------------------------------------------------------------ #

    def distill_memory(self, memory_data: Dict[str, Any]):
        """Legacy hook that can be used to extract essence from memories before removal."""
        content = memory_data.get("content", "")
        emotion = (memory_data.get("emotional_state") or {}).get("primary_emotion", "neutral")
        log_memory_action(
            f"[Distillation] Extracting essence from memory: '{content}' (Emotion: {emotion}). "
            "This essence would now be added to the Knowledge Graph."
        )

    def add_volatile_memory_fragment(self, fragment: Set[str]):
        """Add a volatile memory fragment (simultaneously activated concepts)."""
        self.volatile_memory.append(fragment)
        log_memory_action(f"Added fragment to volatile memory: {fragment}")

    def get_volatile_memory(self) -> List[Set[str]]:
        """Return accumulated volatile memory fragments."""
        return self.volatile_memory

    def clear_volatile_memory(self):
        """Clear volatile memory once MemoryWeaver is done with it."""
        log_memory_action(f"Clearing {len(self.volatile_memory)} fragments from volatile memory.")
        self.volatile_memory = []

    # ------------------------------------------------------------------ #
    # Identity / values / relationships
    # ------------------------------------------------------------------ #

    def update_identity(self, key: str, value: Any):
        if "identity" not in self.data:
            self.data["identity"] = {}
        self.data["identity"][key] = value
        self._save_memory()

    def add_value(self, value: str, importance: float):
        if "values" not in self.data:
            self.data["values"] = []
        self.data["values"].append(
            {"value": value, "importance": importance, "timestamp": datetime.now().isoformat()}
        )
        self._save_memory()

    def update_relationship(self, person: str, details: Dict[str, Any]):
        if "relationships" not in self.data:
            self.data["relationships"] = {}
        if person not in self.data["relationships"]:
            self.data["relationships"][person] = {}
        self.data["relationships"][person].update(details)
        self._save_memory()

    def add_rule(self, rule: str, context: str):
        if "rules" not in self.data:
            self.data["rules"] = []
        self.data["rules"].append({"rule": rule, "context": context, "timestamp": datetime.now().isoformat()})
        self._save_memory()

    # ------------------------------------------------------------------ #
    # Experiences API
    # ------------------------------------------------------------------ #

    def add_experience(self, experience: Union[Experience, Memory, Dict[str, Any]]):
        loop = self.data.get("experience_loop")
        if loop is None or not isinstance(loop, deque):
            self._initialize_rings()
            loop = self.data["experience_loop"]

        if len(loop) == loop.maxlen:
            oldest_experience = loop[0]
            log_memory_action(
                f"Experience Loop is full. Distilling oldest experience before replacement: "
                f"{oldest_experience.get('content')}"
            )
            self.distill_memory(oldest_experience)
            self._distill_experience_to_identity([oldest_experience])

        loop.append(self._experience_to_dict(experience))
        # Keep legacy alias in sync
        self.data["experiences"] = loop
        self._save_memory()

    def get_experiences(self, n: Optional[int] = None) -> List[Experience]:
        experiences = [self._dict_to_experience(exp) for exp in list(self.data.get("experience_loop", []))]
        if n:
            return experiences[-n:]
        return experiences

    def get_identity_fragments(self, n: int = 10) -> List[IdentityFragment]:
        fragments = [self._dict_to_identity_fragment(frag) for frag in list(self.data.get("identity_loop", []))]
        return fragments[-n:]

    def get_essence_principles(self, n: int = 10) -> List[EssencePrinciple]:
        principles = [self._dict_to_essence_principle(pr) for pr in list(self.data.get("essence_loop", []))]
        return principles[-n:]

    def get_efp_core(self) -> Dict[str, float]:
        return self.data.get("efp_core", {"E": 0.0, "F": 0.0, "P": 0.0})

    def get_identity(self) -> Dict[str, Any]:
        return self.data.get("identity", {})

    def get_values(self) -> List[Dict[str, Any]]:
        return self.data.get("values", [])

    def get_relationship(self, person: str) -> Optional[Dict[str, Any]]:
        return self.data.get("relationships", {}).get(person)

    def get_rules(self) -> List[Dict[str, Any]]:
        return self.data.get("rules", [])

    def get_unprocessed_experiences(self) -> List[Experience]:
        unprocessed = []
        for exp_data in self.data.get("experience_loop", []):
            if not exp_data.get("processed_by_weaver", False):
                unprocessed.append(self._dict_to_experience(exp_data))
        return unprocessed

    def mark_experiences_as_processed(self, experience_timestamps: List[str]):
        if not experience_timestamps:
            return

        timestamps_set = set(experience_timestamps)
        for exp_data in self.data.get("experience_loop", []):
            if exp_data.get("timestamp") in timestamps_set:
                exp_data["processed_by_weaver"] = True
        self._save_memory()

    # ------------------------------------------------------------------ #
    # Hypotheses and logging
    # ------------------------------------------------------------------ #

    def add_notable_hypothesis(self, hypothesis: Dict[str, Any]):
        if "notable_hypotheses" not in self.data:
            self.data["notable_hypotheses"] = []

        exists = any(
            h.get("head") == hypothesis.get("head")
            and h.get("tail") == hypothesis.get("tail")
            and h.get("relation") == hypothesis.get("relation")
            for h in self.data["notable_hypotheses"]
        )
        if not exists:
            self.data["notable_hypotheses"].append(hypothesis)
            self._save_memory()
            log_memory_action(f"Added notable hypothesis: {hypothesis.get('head')} -> {hypothesis.get('tail')}")

    def get_unasked_hypotheses(self) -> List[Dict[str, Any]]:
        return [h for h in self.data.get("notable_hypotheses", []) if not h.get("asked")]

    def mark_hypothesis_as_asked(self, head: str, tail: Optional[str] = None):
        for hypothesis in self.data.get("notable_hypotheses", []):
            matches_tail = tail is not None and hypothesis.get("tail") == tail
            matches_ascension = tail is None and hypothesis.get("relation") == "승천"
            if hypothesis.get("head") == head and (matches_tail or matches_ascension):
                hypothesis["asked"] = True
                self._save_memory()
                log_message = f"Marked hypothesis as asked: {head}"
                if tail:
                    log_message += f" -> {tail}"
                log_memory_action(log_message)
                break

    def remove_hypothesis(self, head: str, tail: Optional[str], relation: Optional[str] = None):
        hypotheses = self.data.get("notable_hypotheses", [])
        original_count = len(hypotheses)

        if relation:
            self.data["notable_hypotheses"] = [
                h for h in hypotheses if not (h.get("head") == head and h.get("tail") == tail and h.get("relation") == relation)
            ]
            log_msg = f"Removed hypothesis: {head} -[{relation}]-> {tail}"
        elif tail is not None:
            self.data["notable_hypotheses"] = [
                h for h in hypotheses if not (h.get("head") == head and h.get("tail") == tail)
            ]
            log_msg = f"Removed hypothesis: {head} -> {tail}"
        else:
            self.data["notable_hypotheses"] = [
                h for h in hypotheses if not (h.get("head") == head and h.get("relation") == "승천")
            ]
            log_msg = f"Removed ascension hypothesis: {head}"
        if len(self.data["notable_hypotheses"]) < original_count:
            self._save_memory()
            log_memory_action(log_msg)

    def add_log(self, log_entry: Dict[str, Any]):
        if "logs" not in self.data:
            self.data["logs"] = []
        self.data["logs"].append(log_entry)
        self._save_memory()

    def add_voice_pattern(self, pattern: str, context: str):
        """Stores a learned rhetorical style or voice pattern."""
        if "voice_patterns" not in self.data:
            self.data["voice_patterns"] = []
        
        # Avoid duplicates
        for p in self.data["voice_patterns"]:
            if p["pattern"] == pattern:
                return

        self.data["voice_patterns"].append({
            "pattern": pattern,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        self._save_memory()
        log_memory_action(f"Learned new voice pattern: {pattern}")

    def get_voice_patterns(self) -> List[Dict[str, Any]]:
        return self.data.get("voice_patterns", [])
    def _distill_experience_to_identity(self, experiences_data: List[Dict[str, Any]]):
        if not experiences_data:
            return

        content = " ".join(exp.get("content", "") for exp in experiences_data)
        summary = f"경험 요약: {content[:50]}..."

        total_valence = 0.0
        emotions: List[str] = []

        # Tensor/Wave averaging
        total_tensor = Tensor3D(0,0,0)
        total_frequency = 0.0

        for exp in experiences_data:
            # Emotion
            emotion_payload = exp.get("emotional_state")
            if isinstance(emotion_payload, dict):
                total_valence += emotion_payload.get("valence", 0.0)
                emotions.append(emotion_payload.get("primary_emotion", "neutral"))
            elif isinstance(emotion_payload, EmotionalState):
                total_valence += emotion_payload.valence
                emotions.append(emotion_payload.primary_emotion)
            else:
                emotions.append("neutral")

            # Physics
            if 'tensor' in exp and exp['tensor']:
                t_val = exp['tensor']
                if isinstance(t_val, Tensor3D):
                    total_tensor = total_tensor + t_val
                else:
                    total_tensor = total_tensor + Tensor3D.from_dict(t_val)
            elif 'tensor_state' in exp and exp['tensor_state']:
                total_tensor = total_tensor + Tensor3D.from_dict(exp['tensor_state'])

            # Simple frequency averaging (could be more complex)
            if 'wave' in exp and exp['wave']:
                w_val = exp['wave']
                if isinstance(w_val, FrequencyWave):
                    total_frequency += w_val.frequency
                elif isinstance(w_val, dict):
                    total_frequency += w_val.get('frequency', 0.0)
            else:
                total_frequency += exp.get('frequency', 0.0)

        avg_valence = total_valence / len(experiences_data)
        avg_frequency = total_frequency / len(experiences_data)
        avg_tensor = total_tensor * (1.0 / len(experiences_data))

        primary_emotion = emotions[0] if emotions else "neutral"

        # New Identity Fragment with full physics
        new_fragment = IdentityFragment(
            timestamp=datetime.now().isoformat(),
            content=summary,
            type="narrative_summary",
            linked_experiences=[exp.get("timestamp") for exp in experiences_data],
            emotional_summary=EmotionalState(
                valence=avg_valence, arousal=0.5, dominance=0.0, primary_emotion=primary_emotion,
                tensor=avg_tensor, wave=FrequencyWave(avg_frequency, 0.5, 0.0, 0.0)
            ),
            # Legacy fields sync
            avg_frequency=avg_frequency,
            tensor_state=avg_tensor.to_dict(),
            tensor=avg_tensor,
            wave=FrequencyWave(avg_frequency, 0.5, 0.0, 0.0)
        )

        identity_loop = self.data.get("identity_loop")
        if len(identity_loop) == identity_loop.maxlen:
            oldest_fragment = identity_loop[0]
            log_memory_action(
                f"Identity Loop is full. Distilling oldest fragment before replacement: {oldest_fragment.get('content')}"
            )
            self._distill_identity_to_essence([oldest_fragment])

        identity_loop.append(self._identity_fragment_to_dict(new_fragment))

    def _distill_identity_to_essence(self, fragments_data: List[Dict[str, Any]]):
        if not fragments_data:
            return

        content = " ".join(fragment.get("content", "") for fragment in fragments_data)
        principle_summary = f"정체성으로부터의 깨달음: {content[:70]}..."

        impact = {"E": 0.05, "F": 0.01, "P": 0.0}

        # Physics Distillation
        total_tensor = Tensor3D(0,0,0)
        for frag in fragments_data:
             if 'tensor' in frag and frag['tensor']:
                t_val = frag['tensor']
                if isinstance(t_val, Tensor3D):
                    total_tensor = total_tensor + t_val
                else:
                    total_tensor = total_tensor + Tensor3D.from_dict(t_val)
             elif 'tensor_state' in frag and frag['tensor_state']:
                total_tensor = total_tensor + Tensor3D.from_dict(frag['tensor_state'])

        avg_tensor = total_tensor * (1.0 / len(fragments_data))

        new_principle = EssencePrinciple(
            timestamp=datetime.now().isoformat(),
            content=principle_summary,
            type="core_belief",
            linked_fragments=[fragment.get("timestamp") for fragment in fragments_data],
            impact_on_efp=impact,
            tensor=avg_tensor,
            wave=FrequencyWave(100.0, 1.0, 0.0, 1.0), # High richness essence
            # Legacy
            tensor_state=avg_tensor.to_dict(),
            harmonic_root=100.0,
            richness=1.0
        )

        essence_loop = self.data.get("essence_loop")
        if len(essence_loop) == essence_loop.maxlen:
            oldest_principle = essence_loop[0]
            log_memory_action(
                f"Essence Loop is full. Applying decay before rotating out: {oldest_principle.get('content')}"
            )
            self._update_efp_core(oldest_principle.get("impact_on_efp", {}), decay=True)

        essence_loop.append(self._essence_principle_to_dict(new_principle))
        self._update_efp_core(impact)

    def _update_efp_core(self, impact: Dict[str, float], decay: bool = False):
        core = self.get_efp_core()
        multiplier = -1 if decay else 1

        for key in ("E", "F", "P"):
            core[key] = core.get(key, 0.0) + impact.get(key, 0.0) * multiplier

        # Gentle decay to avoid runaway growth
        core["E"] *= 0.999
        core["F"] *= 0.999
        core["P"] *= 0.999

        self.data["efp_core"] = core
        log_memory_action(f"EFP Core updated: {core}")

    # ------------------------------------------------------------------ #
    # Serialization helpers
    # ------------------------------------------------------------------ #

    # Helper to serialize EmotionalState with nested physics objects
    def _emotional_state_to_dict(self, es: EmotionalState) -> Dict[str, Any]:
        d = asdict(es)
        d['tensor'] = es.tensor.to_dict()
        d['wave'] = es.wave.to_dict()
        return d

    def _experience_to_dict(self, experience: Union[Experience, Memory, Dict[str, Any]]) -> Dict[str, Any]:
        if isinstance(experience, dict):
            data = experience.copy()
        else:
            data = asdict(experience)
            # Serialize physics objects explicitly
            if experience.tensor: data['tensor'] = experience.tensor.to_dict()
            if experience.wave: data['wave'] = experience.wave.to_dict()
            if experience.emotional_state:
                data['emotional_state'] = self._emotional_state_to_dict(experience.emotional_state)

        # Handle optional fields and defaults
        data.setdefault("type", "episode")
        data.setdefault("tags", [])
        data.setdefault("processed_by_weaver", False)
        data.setdefault("processed_by_distiller", False)
        return data

    def _identity_fragment_to_dict(self, fragment: IdentityFragment) -> Dict[str, Any]:
        data = asdict(fragment)
        data['tensor'] = fragment.tensor.to_dict()
        data['wave'] = fragment.wave.to_dict()
        if fragment.emotional_summary:
            data['emotional_summary'] = self._emotional_state_to_dict(fragment.emotional_summary)
        return data

    def _essence_principle_to_dict(self, principle: EssencePrinciple) -> Dict[str, Any]:
        data = asdict(principle)
        data['tensor'] = principle.tensor.to_dict()
        data['wave'] = principle.wave.to_dict()
        return data

    def _dict_to_emotional_state(self, data: Optional[Dict[str, Any]]) -> Optional[EmotionalState]:
        if not data:
            return None

        # Deserialize nested objects
        tensor_data = data.get('tensor')
        wave_data = data.get('wave')

        return EmotionalState(
            valence=data.get("valence", 0.0),
            arousal=data.get("arousal", 0.0),

            dominance=data.get("dominance", 0.0),

            primary_emotion=data.get("primary_emotion", "neutral"),

            secondary_emotions=data.get("secondary_emotions", []),

            tensor=Tensor3D.from_dict(tensor_data) if tensor_data else Tensor3D(),

            wave=FrequencyWave.from_dict(wave_data) if wave_data else FrequencyWave(0.0, 0.0, 0.0, 0.0)

        )



    def _dict_to_experience(self, data: Dict[str, Any]) -> Experience:

        exp_data = data.copy()



        # Clean up raw dict to match constructor signature if needed,

        # or rely on post_init and helpers

        if isinstance(exp_data.get("emotional_state"), dict):

            exp_data["emotional_state"] = self._dict_to_emotional_state(exp_data["emotional_state"])



        # Deserialize physics

        if 'tensor' in exp_data and isinstance(exp_data['tensor'], dict):

            exp_data['tensor'] = Tensor3D.from_dict(exp_data['tensor'])

        if 'wave' in exp_data and isinstance(exp_data['wave'], dict):

            exp_data['wave'] = FrequencyWave.from_dict(exp_data['wave'])



        return Experience(**exp_data)



    def _dict_to_identity_fragment(self, data: Dict[str, Any]) -> IdentityFragment:

        fragment_data = data.copy()

        summary = fragment_data.get("emotional_summary")

        fragment_data["emotional_summary"] = self._dict_to_emotional_state(summary) or EmotionalState(

            valence=0.0, arousal=0.0, dominance=0.0, primary_emotion="neutral"

        )



        if 'tensor' in fragment_data and isinstance(fragment_data['tensor'], dict):

            fragment_data['tensor'] = Tensor3D.from_dict(fragment_data['tensor'])

        if 'wave' in fragment_data and isinstance(fragment_data['wave'], dict):

            fragment_data['wave'] = FrequencyWave.from_dict(fragment_data['wave'])



        # Defaults for legacy fields

        fragment_data.setdefault("avg_frequency", 0.0)

        fragment_data.setdefault("tensor_state", None)

        fragment_data.setdefault("richness", 0.0)

        return IdentityFragment(**fragment_data)



    def _dict_to_essence_principle(self, data: Dict[str, Any]) -> EssencePrinciple:

        data_copy = data.copy()



        if 'tensor' in data_copy and isinstance(data_copy['tensor'], dict):

            data_copy['tensor'] = Tensor3D.from_dict(data_copy['tensor'])

        if 'wave' in data_copy and isinstance(data_copy['wave'], dict):

            data_copy['wave'] = FrequencyWave.from_dict(data_copy['wave'])



        data_copy.setdefault("harmonic_root", 0.0)

        data_copy.setdefault("tensor_state", None)

        data_copy.setdefault("richness", 0.0)

        return EssencePrinciple(**data_copy)



    def _save_memory(self):

        if not self.file_path:

            return



        try:

            dir_name = os.path.dirname(self.file_path)

            if dir_name:

                os.makedirs(dir_name, exist_ok=True)



            data_to_save: Dict[str, Any] = {}

            for key, value in self.data.items():

                if isinstance(value, deque):

                    data_to_save[key] = list(value)

                else:

                    data_to_save[key] = value



            # Keep explicit alias for compatibility

            if "experience_loop" in data_to_save:

                data_to_save["experiences"] = list(data_to_save["experience_loop"])



            with open(self.file_path, "w", encoding="utf-8") as f:

                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

            log_memory_action(f"Successfully saved memory to {self.file_path}")

        except Exception as e:

            log_memory_action(f"Error saving MRE state to {self.file_path}: {e}")

