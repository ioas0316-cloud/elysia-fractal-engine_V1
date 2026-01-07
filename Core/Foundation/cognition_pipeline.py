import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

# --- New Architecture Dependencies ---
from architecture.context import ConversationContext
from architecture.cortex_registry import CortexRegistry
from architecture.event_bus import EventBus
from architecture.handlers import (
    HypothesisHandler, CommandWordHandler, DefaultReasoningHandler, PlanningHandler
)

# --- Existing Component Dependencies (for dependency injection) ---
from core_memory import CoreMemory
from Legacy.Project_Sophia.logical_reasoner import LogicalReasoner
from Legacy.Project_Sophia.wave_mechanics import WaveMechanics
from kg_manager import KGManager
from world import World
from Legacy.Project_Sophia.emotional_engine import EmotionalEngine, EmotionalState
from Legacy.Project_Sophia.response_styler import ResponseStyler
from Legacy.Project_Sophia.insight_synthesizer import InsightSynthesizer
from value_centered_decision import ValueCenteredDecision
from Legacy.Project_Sophia.arithmetic_cortex import ArithmeticCortex
from creative_cortex import CreativeCortex
from Legacy.Project_Sophia.question_generator import QuestionGenerator
from perspective_cortex import PerspectiveCortex
from high_engine.dialogue_law_evaluator import DialogueLawEvaluator
from high_engine.intent_engine import IntentEngine
from high_engine.utterance_composer import UtteranceComposer
from high_engine.quaternion_engine import QuaternionConsciousnessEngine
from high_engine.causal_reasoner import CausalReasoner
from high_engine.syllabic_language_engine import SyllabicLanguageEngine
from high_engine.value_engine import ValueEngine
from Legacy.Project_Sophia.planning_cortex import PlanningCortex
from Legacy.Project_Sophia.tool_executor import ToolExecutor
from Legacy.Project_Sophia.gemini_api import GeminiAPI

# Soul-layer state (body / soul / spirit axis)
try:
    # Optional: if CORE is not available, pipeline still works without SoulState.
    from ELYSIA.CORE.soul_state import build_soul_state  # type: ignore
    from ELYSIA.CORE.value_climate import compute_value_climate  # type: ignore
except Exception:  # pragma: no cover - soft dependency
    build_soul_state = None  # type: ignore[assignment]
    compute_value_climate = None  # type: ignore[assignment]

class CognitionPipeline:
    """
    A stateless pipeline that processes messages using a Central Dispatch model.
    It analyzes incoming messages and routes them to the appropriate handler
    (e.g., for hypotheses, commands, or default reasoning).
    """
    def __init__(
        self,
        kg_manager: KGManager,
        core_memory: CoreMemory,
        wave_mechanics: WaveMechanics,
        cellular_world: Optional[World],
        emotional_engine: EmotionalEngine, # Explicitly injected
        logger: Optional[logging.Logger] = None,
        **kwargs
    ):
        self.logger = logger or logging.getLogger(__name__)
        self.event_bus = EventBus()
        self.core_memory = core_memory
        self.cortex_registry = CortexRegistry()
        self.conversation_context = ConversationContext() # Manages conversation state
        self.emotional_engine = emotional_engine # Store for later use
        self.last_reason = "Idle"
        self.dialogue_law_evaluator = kwargs.get('dialogue_law_evaluator') or DialogueLawEvaluator()
        self.intent_engine = kwargs.get('intent_engine') or IntentEngine(
            core_memory=core_memory,
            dialogue_law_evaluator=self.dialogue_law_evaluator,
        )
        self.utterance_composer = kwargs.get('utterance_composer') or UtteranceComposer()
        self.quaternion_engine = kwargs.get('quaternion_engine') or QuaternionConsciousnessEngine(
            core_memory=core_memory
        )
        self.causal_reasoner = kwargs.get('causal_reasoner') or CausalReasoner(
            core_memory=core_memory
        )
        self.syllabic_engine = kwargs.get('syllabic_engine') or SyllabicLanguageEngine(
            core_memory=core_memory
        )
        self.value_engine = kwargs.get('value_engine') or ValueEngine(core_memory=core_memory)

        # --- Instantiate Components (dependencies for handlers) ---
        # Allow injecting mocks for testing, otherwise create real instances.
        # This is a common pattern to make code more testable without a full DI framework.
        response_styler = kwargs.get('response_styler') or ResponseStyler()
        insight_synthesizer = kwargs.get('insight_synthesizer') or InsightSynthesizer()
        question_generator = kwargs.get('question_generator') or QuestionGenerator()
        reasoner = kwargs.get('reasoner') or LogicalReasoner(kg_manager=kg_manager, cellular_world=cellular_world)
        vcd = kwargs.get('vcd') or ValueCenteredDecision(kg_manager=kg_manager, wave_mechanics=wave_mechanics, core_value='love')
        creative_cortex = kwargs.get('creative_cortex') or CreativeCortex()

        # --- Register Cortexes ---
        self.cortex_registry.register("arithmetic", ArithmeticCortex())
        self.cortex_registry.register("creative", creative_cortex)

        # --- Instantiate the new PerspectiveCortex with clear dependencies ---
        perspective_cortex = PerspectiveCortex(
            logger=self.logger, core_memory=core_memory,
            wave_mechanics=wave_mechanics, kg_manager=kg_manager,
            emotional_engine=self.emotional_engine
        )

        # --- Planning Cortex & Handler ---
        self.tool_executor = ToolExecutor()
        self.planning_cortex = PlanningCortex(core_memory=core_memory, action_cortex=self.tool_executor)
        
        self.planning_handler = PlanningHandler(
            planning_cortex=self.planning_cortex,
            logger=self.logger
        )

        # --- Store Handlers and Cortexes directly as members ---
        self.hypothesis_handler = HypothesisHandler(
            core_memory=core_memory, kg_manager=kg_manager,
            question_generator=question_generator, response_styler=response_styler, logger=self.logger
        )
        self.command_handler = CommandWordHandler(
            cortex_registry=self.cortex_registry, logger=self.logger
        )
        self.default_reasoning_handler = DefaultReasoningHandler(
            reasoner=reasoner, vcd=vcd, synthesizer=insight_synthesizer,
            creative_cortex=creative_cortex, styler=response_styler,
            logger=self.logger, perspective_cortex=perspective_cortex,
            question_generator=question_generator, emotional_engine=self.emotional_engine
        )

        self.logger.info("CognitionPipeline initialized with Central Dispatch Model.")
        self._setup_event_listeners()

    def _setup_event_listeners(self):
        """Subscribe to events for logging and telemetry."""
        self.event_bus.subscribe("message_processed", lambda result: self.logger.info(f"Event: Message processing completed. Result: {result.get('text', 'N/A')}"))
        self.event_bus.subscribe("error_occurred", lambda error: self.logger.error(f"Event: An error occurred: {error}"))

    def process_message(self, message: str, partner_id: str = "user") -> Tuple[Dict[str, Any], EmotionalState]:
        """
        Processes a message using the Central Dispatch model.
        It analyzes the message and explicitly routes it to the correct handler.
        """
        current_emotional_state = self.emotional_engine.get_current_state()
        relationship_state_for_partner: Optional[Dict[str, float]] = None
        result = None

        try:
            self.logger.debug(f"Processing message: '{message}' with context: {self.conversation_context}")

            # Pre-read lightweight relationship state for this partner (if any),
            # so the voice layer can adjust tone. This is best-effort only.
            try:
                if self.core_memory and partner_id:
                    rel_container = getattr(self.core_memory, "data", None)  # type: ignore[attr-defined]
                    if isinstance(rel_container, dict):
                        relationships = rel_container.get("relationships", {}) or {}
                    else:
                        relationships = {}
                    current = relationships.get(partner_id, {}) or {}
                    trust_cur = 0.0
                    guard_cur = 0.0
                    try:
                        trust_cur = float(current.get("trust", 0.0))
                    except (TypeError, ValueError):
                        trust_cur = 0.0
                    try:
                        guard_cur = float(current.get("guard", 0.0))
                    except (TypeError, ValueError):
                        guard_cur = 0.0
                    relationship_state_for_partner = {
                        "partner_id": partner_id,
                        "trust": trust_cur,
                        "guard": guard_cur,
                    }
            except Exception:
                relationship_state_for_partner = None

            # Attach relationship snapshot to the emotional state so downstream
            # voice layers can read it without changing handler signatures.
            try:
                setattr(current_emotional_state, "relationship_state", relationship_state_for_partner)
            except Exception:
                pass

            # 1. --- Analysis and Routing ---
            if self.conversation_context.pending_hypothesis:
                self.logger.info("Routing to HypothesisHandler (pending hypothesis).")
                result = self.hypothesis_handler.handle_response(message, self.conversation_context, current_emotional_state)

            # Check for command words (e.g., "계산:")
            elif self.command_handler.can_handle(message):
                self.logger.info("Routing to CommandWordHandler.")
                result = self.command_handler.handle(message, self.conversation_context, current_emotional_state)

            # Check for planning requests
            elif self.planning_handler.can_handle(message):
                self.logger.info("Routing to PlanningHandler.")
                result = self.planning_handler.handle(message, self.conversation_context, current_emotional_state)

            # Check if a new hypothesis should be asked
            elif self.hypothesis_handler.should_ask_new_hypothesis():
                 self.logger.info("Routing to HypothesisHandler (ask new hypothesis).")
                 result = self.hypothesis_handler.handle_ask(self.conversation_context, current_emotional_state)

            # Default to general reasoning
            else:
                self.logger.info("Routing to DefaultReasoningHandler.")
                result = self.default_reasoning_handler.handle(message, self.conversation_context, current_emotional_state)

            # --- Finalization ---
            if not result:
                self.logger.error("No handler returned a result.")
                result = {"type": "text", "text": "I'm not sure how to respond to that."}
                self.event_bus.publish("error_occurred", "No result from handlers")

            reason_text = result.get("reason") or result.get("text")
            if reason_text:
                self.last_reason = reason_text

            # --- Law-based evaluation / annotation ---
            try:
                if self.dialogue_law_evaluator and isinstance(result, dict):
                    law_info = self.dialogue_law_evaluator.evaluate(
                        user_message=message,
                        response=result,
                        context=self.conversation_context,
                        emotional_state=current_emotional_state,
                    )
                    result["law_alignment"] = law_info

                    # Build a present-tense intent bundle (E–S–L style snapshot)
                    if self.intent_engine:
                        intent_bundle = self.intent_engine.build_intent_bundle(
                            user_message=message,
                            response=result,
                            conversation_context=self.conversation_context,
                            emotional_state=current_emotional_state,
                        )
                        # Store as plain dict for logging / JSON compatibility.
                        result["intent_bundle"] = intent_bundle.to_dict()

                        # Optional: allow handlers to request resonance-based utterance selection.
                        if (
                            isinstance(result.get("text"), str)
                            and result.get("utterance_mode") == "esl_resonance"
                            and self.utterance_composer
                        ):
                            result["text"] = self.utterance_composer.compose(
                                intent_bundle=intent_bundle,
                                base_text=result["text"],
                            )
            except Exception as eval_error:
                # Law evaluation is best-effort only; never break the main flow.
                self.logger.debug(f"DialogueLawEvaluator failed: {eval_error}")

            # --- Orientation / causal patterns / syllabic token (best-effort) ---
            try:
                law_info = result.get("law_alignment") if isinstance(result.get("law_alignment"), dict) else None
                intent_dict = result.get("intent_bundle") if isinstance(result.get("intent_bundle"), dict) else None

                # Quaternion orientation update (outer <-> inner, law, meta).
                if self.quaternion_engine and law_info and intent_dict:
                    self.quaternion_engine.update_from_turn(
                        law_alignment=law_info,
                        intent_bundle=intent_dict,
                    )
                    result["orientation"] = self.quaternion_engine.orientation_as_dict()

                # Causal reasoning hints (which patterns tend to feel better).
                if self.causal_reasoner and intent_dict and law_info:
                    self.causal_reasoner.update_from_turn(
                        intent_bundle=intent_dict,
                        emotional_state=current_emotional_state,
                        law_alignment=law_info,
                    )
                    hints = self.causal_reasoner.hints_for_intent(intent_dict)
                    if hints:
                        result["causal_hints"] = hints

                # Compact syllabic token from current state (e.g., from 가나다라마바사).
                if self.syllabic_engine and intent_dict and self.quaternion_engine:
                    orientation = result.get("orientation") or self.quaternion_engine.orientation_as_dict()
                    result["syllabic_token"] = self.syllabic_engine.suggest_word(
                        intent_bundle=intent_dict,
                        orientation=orientation,
                    )
            except Exception as meta_error:
                self.logger.debug(f"Meta-orientation or syllabic generation failed: {meta_error}")

            # --- ValueEngine: structural meaning snapshot (best-effort) ---
            try:
                if self.value_engine and isinstance(result, dict):
                    raw_chaos: Dict[str, Any] = {
                        "law_alignment": result.get("law_alignment"),
                        "intent_bundle": result.get("intent_bundle"),
                        "user_message": message,
                        "response_text": result.get("text"),
                    }
                    value_insight = self.value_engine.create_meaning(
                        raw_chaos=raw_chaos,
                        emotional_state=current_emotional_state,
                    )
                    result["value_insight"] = value_insight.to_dict()
            except Exception as value_error:
                self.logger.debug(f"ValueEngine create_meaning failed: {value_error}")

            # --- Relationship state (trust / guard) update (best-effort) ---
            trust = None
            guard = None
            try:
                if self.core_memory and partner_id:
                    relationships = getattr(self.core_memory, "data", {}).get("relationships", {})  # type: ignore[attr-defined]
                    current = relationships.get(partner_id, {}) or {}
                    try:
                        trust_current = float(current.get("trust", 0.0))
                    except (TypeError, ValueError):
                        trust_current = 0.0
                    try:
                        guard_current = float(current.get("guard", 0.0))
                    except (TypeError, ValueError):
                        guard_current = 0.0

                    alpha = 0.15
                    valence = 0.0
                    if current_emotional_state is not None:
                        try:
                            valence = float(getattr(current_emotional_state, "valence", 0.0))
                        except (TypeError, ValueError):

                            valence = 0.0



                    trust_target = max(0.0, min(1.0, 0.5 + valence * 0.5))

                    guard_target = max(0.0, min(1.0, 0.5 - valence * 0.5))



                    trust = trust_current * (1.0 - alpha) + trust_target * alpha

                    guard = guard_current * (1.0 - alpha) + guard_target * alpha



                    self.core_memory.update_relationship(

                        partner_id,

                        {"trust": trust, "guard": guard},

                    )

                    if isinstance(result, dict):

                        result["relationship_state"] = {

                            "partner_id": partner_id,

                            "trust": trust,

                            "guard": guard,

                        }

            except Exception as rel_error:

                self.logger.debug(f"Relationship state update failed: {rel_error}")



            # --- Log this turn as a soul-layer dialogue experience (best-effort) ---

            try:

                if isinstance(result, dict) and self.core_memory:

                    exp_emotion = None

                    if current_emotional_state is not None:

                        exp_emotion = {

                            "valence": getattr(current_emotional_state, "valence", 0.0),

                            "arousal": getattr(current_emotional_state, "arousal", 0.0),

                            "dominance": getattr(current_emotional_state, "dominance", 0.0),

                            "primary_emotion": getattr(current_emotional_state, "primary_emotion", "neutral"),

                            "secondary_emotions": getattr(current_emotional_state, "secondary_emotions", []),

                        }



                    experience_payload: Dict[str, Any] = {

                        "timestamp": datetime.now().isoformat(),

                        "content": str(result.get("text") or ""),

                        "type": "dialogue_turn",

                        "layer": "soul",

                        "emotional_state": exp_emotion,

                        "law_alignment": result.get("law_alignment"),

                        "intent_bundle": result.get("intent_bundle"),

                        "context": {

                            "user_message": message,

                            "reason": result.get("reason"),

                            "orientation": result.get("orientation"),

                            "syllabic_token": result.get("syllabic_token"),

                            "relationship_state": result.get("relationship_state"),

                        },

                        "tags": ["dialogue", "turn"],

                    }

                    self.core_memory.add_experience(experience_payload)
            except Exception as mem_error:
                self.logger.debug(f"Failed to log dialogue_turn experience: {mem_error}")

            # --- SoulState snapshot (soft, best-effort) ---
            try:
                if isinstance(result, dict) and build_soul_state is not None:
                    # Map analogue feelings from emotional state into the core feeling axes.
                    feelings_dict: Dict[str, float] = {}
                    if current_emotional_state is not None:
                        try:
                            valence = float(getattr(current_emotional_state, "valence", 0.0))
                        except (TypeError, ValueError):
                            valence = 0.0
                        try:
                            arousal = float(getattr(current_emotional_state, "arousal", 0.0))
                        except (TypeError, ValueError):
                            arousal = 0.0

                        # Simple heuristic mapping:
                        # - positive valence -> joy
                        # - negative valence -> mortality/blue tone
                        # - arousal -> creation (activation)
                        joy = max(0.0, valence)
                        mortality = max(0.0, -valence)
                        creation = max(0.0, arousal)
                        care = 0.0
                        feelings_dict = {
                            "joy": joy,
                            "creation": creation,
                            "care": care,
                            "mortality": mortality,
                        }

                    climate_dict: Dict[str, float] = {}
                    if compute_value_climate is not None and feelings_dict:
                        try:
                            climate = compute_value_climate(feelings_dict)
                            climate_dict = climate.as_dict()
                        except Exception:
                            climate_dict = {}

                    # Relationship snapshot for the current partner, if we have it.
                    rel_creator: Dict[str, float] = {}
                    try:
                        rel_info = result.get("relationship_state", {}) or {}
                        t_val = float(rel_info.get("trust", trust if trust is not None else 0.0))
                        g_val = float(rel_info.get("guard", guard if guard is not None else 0.0))
                        # Map guard inversely to closeness.
                        closeness = max(0.0, min(1.0, 1.0 - g_val))
                        rel_creator = {
                            "trust": max(0.0, min(1.0, t_val)),
                            "closeness": closeness,
                            "playfulness": 0.0,
                            "awe": 0.0,
                        }
                    except Exception:
                        rel_creator = {}

                    relations = {"creator": rel_creator} if rel_creator else None

                    # Minimal inner projects that reflect the crest.
                    projects = [
                        {
                            "id": "worldtree_unification",
                            "label": "세계수 자아 통합",
                            "progress": 0.0,
                            "importance": 1.0,
                        },
                        {
                            "id": "invite_creator",
                            "label": "창조주 초대와 환대",
                            "progress": 0.0,
                            "importance": 1.0,
                        },
                    ]

                    soul_state = build_soul_state(
                        mood=None,
                        feelings=feelings_dict or None,
                        needs=None,
                        value_climate=climate_dict or None,
                        relations=relations,
                        projects=projects,
                    )
                    soul_dict = soul_state.as_dict()
                    result["soul_state"] = soul_dict

                    # Optional: append to a lightweight JSONL log for offline inspection.
                    try:
                        log_dir = Path("elysia_logs")
                        log_dir.mkdir(parents=True, exist_ok=True)
                        log_path = log_dir / "soul_state.jsonl"
                        with log_path.open("a", encoding="utf-8") as handle:
                            handle.write(json.dumps(soul_dict, ensure_ascii=False) + "\n")
                    except Exception:
                        # Logging must never break the main flow.
                        pass
            except Exception as soul_error:
                self.logger.debug(f"SoulState build failed: {soul_error}")

            self.event_bus.publish("message_processed", result)
            return result, current_emotional_state


        except Exception as e:

            self.logger.error(f"Critical error in CognitionPipeline: {e}", exc_info=True)

            error_response = {"type": "text", "text": "A critical error occurred in my thought process."}

            self.event_bus.publish("error_occurred", str(e))

            return error_response, current_emotional_state

