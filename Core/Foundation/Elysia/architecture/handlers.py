

from typing import Optional, Any

import re

from datetime import datetime

import logging



from Project_Elysia.architecture.context import ConversationContext

from Project_Elysia.architecture.cortex_registry import CortexRegistry

from Project_Elysia.core_memory import CoreMemory

from tools.kg_manager import KGManager

from Core.Foundation.question_generator import QuestionGenerator

from Core.Foundation.relationship_extractor import extract_relationship_type

from Core.Foundation.response_styler import ResponseStyler

from Core.Foundation.logical_reasoner import LogicalReasoner

from Project_Elysia.value_centered_decision import ValueCenteredDecision

from Core.Foundation.insight_synthesizer import InsightSynthesizer

from Project_Mirror.creative_cortex import CreativeCortex

from Core.Foundation.emotional_engine import EmotionalState

from Project_Mirror.perspective_cortex import PerspectiveCortex

from Core.Foundation.emotional_engine import EmotionalEngine





class HypothesisHandler:

    """Handles asking and processing responses for hypotheses."""



    def __init__(

        self,

        core_memory: CoreMemory,

        kg_manager: KGManager,

        question_generator: QuestionGenerator,

        response_styler: ResponseStyler,

        logger: logging.Logger,

    ):

        self.core_memory = core_memory

        self.kg_manager = kg_manager

        self.question_generator = question_generator

        self.response_styler = response_styler

        self.logger = logger

        self.ask_user_via_ui = None  # Optional callback for pushing questions to the UI



    def should_ask_new_hypothesis(self) -> bool:

        return bool(self.core_memory.get_unasked_hypotheses())

    def _relation_flow_score(self, relation: str, confidence: float) -> float:
        """
        Lightweight 'flow' heuristic: higher confidence relations flow faster.
        Purely advisory/logging; does not change branching.
        """
        base = {
            "ascension": 0.8,
            "proposes_correction": 0.6,
            "forms_new_concept": 0.7,
        }.get(relation, 0.5)
        return max(0.0, min(1.0, base * confidence))



    def handle_ask(self, context: ConversationContext, emotional_state: EmotionalState) -> Optional[Any]:

        hypotheses = self.core_memory.get_unasked_hypotheses()

        if not hypotheses:

            return None



        hypothesis_to_ask = hypotheses[0]

        context.pending_hypothesis = hypothesis_to_ask



        tail = hypothesis_to_ask.get("tail")

        self.core_memory.mark_hypothesis_as_asked(hypothesis_to_ask["head"], tail)



        confidence = hypothesis_to_ask.get("confidence", 0.5)

        relation = hypothesis_to_ask.get("relation")



        question: Optional[str] = None

        if relation == "forms_new_concept" and 0.7 <= confidence < 0.9:

            self.logger.info(

                "Generating wisdom-seeking question for mid-confidence insight: %s",

                hypothesis_to_ask.get("new_concept_id"),

            )

            question = self.question_generator.generate_wisdom_seeking_question(hypothesis_to_ask)

        elif relation in ("ascension", "승천"):
            question = hypothesis_to_ask.get(
                "text",
                f"새 개념 '{hypothesis_to_ask['head']}'을(를) 지식망에 올릴까요?",
            )

        elif relation == "proposes_correction":

            self.logger.info(

                "Generating correction proposal question for: %s <-> %s",

                hypothesis_to_ask.get("head"),

                hypothesis_to_ask.get("tail"),

            )

            question = self.question_generator.generate_correction_proposal_question(hypothesis_to_ask)



        if not question:

            question = self.question_generator.generate_question_from_hypothesis(hypothesis_to_ask)



        if self.ask_user_via_ui:

            payload = hypothesis_to_ask.copy()

            payload["text"] = question

            self.ask_user_via_ui(payload)

            return {"type": "system_action", "action": "hypothesis_pushed_to_ui"}



        return {"type": "text", "text": question}



    def handle_response(

        self, message: str, context: ConversationContext, emotional_state: EmotionalState

    ) -> Optional[Any]:

        hypothesis = context.pending_hypothesis

        if not hypothesis:

            return None



        response_text = ""

        relation = hypothesis.get("relation")



        if relation in ("ascension", "승천"):
            self.logger.info("Processing user response for Ascension hypothesis: %s", hypothesis.get("head"))
            flow_score = self._relation_flow_score("ascension", hypothesis.get("confidence", 0.5))
            self.logger.debug(f"Ascension flow score: {flow_score:.2f}")
            if any(word in message for word in ["네", "예", "맞아", "그래", "승천", "승천시켜", "허용"]):
                metadata = hypothesis.get("metadata", {})
                properties = {
                    "type": "concept",
                    "discovery_source": "Cell_Ascension_Ritual",
                    "parents": metadata.get("parents", []),
                    "ascended_at": datetime.now().isoformat(),
                }
                self.kg_manager.add_node(hypothesis.get("head"), properties=properties)
                response_text = f"알겠어요. 새 개념 '{hypothesis.get('head')}'을(를) 지식망에 승천시켰습니다."
            else:
                response_text = f"알겠어요. 개념 '{hypothesis.get('head')}'의 승천은 보류합니다."


        elif relation == "proposes_correction":
            self.logger.info(
                "Processing user response for Correction proposal: %s <-> %s",
                hypothesis.get("head"),
                hypothesis.get("tail"),
            )
            flow_score = self._relation_flow_score("proposes_correction", hypothesis.get("confidence", 0.5))
            self.logger.debug(f"Correction flow score: {flow_score:.2f}")
            if any(word in message for word in ["네", "예", "맞아", "그래", "수정", "허락"]):
                insight = hypothesis.get("metadata", {}).get("contradictory_insight")
                if insight:
                    new_head = insight.get("head")
                    new_tail = insight.get("tail")
                    new_relation = insight.get("relation")


                    if self.kg_manager.edge_exists(source=new_tail, target=new_head, relation=new_relation):

                        self.kg_manager.remove_edge(new_tail, new_head, new_relation)

                        self.logger.info("Removed reversal edge %s -> %s (%s)", new_tail, new_head, new_relation)



                    inverse_relations = {"causes": "caused_by", "caused_by": "causes"}

                    inverse_of_new = inverse_relations.get(new_relation)

                    if inverse_of_new and self.kg_manager.edge_exists(

                        source=new_head, target=new_tail, relation=inverse_of_new

                    ):

                        self.kg_manager.remove_edge(new_head, new_tail, inverse_of_new)

                        self.logger.info("Removed inverse edge %s -> %s (%s)", new_head, new_tail, inverse_of_new)


                    self.kg_manager.add_edge(new_head, new_tail, new_relation)
                    response_text = "모순을 바로잡았습니다. 고마워요."
                else:
                    response_text = "수정을 진행하기엔 기존 관찰 정보가 부족합니다."
            else:
                response_text = "알겠어요. 기존 지식을 그대로 유지합니다."

        else:
            self.logger.info(
                "Processing user response for relationship hypothesis: %s -> %s",
                hypothesis.get("head"),
                hypothesis.get("tail"),
            )
            confirmed_relation = extract_relationship_type(message) or (
                "related_to" if any(word in message for word in ["네", "예", "맞아", "그래"]) else None
            )
            if confirmed_relation:
                head = hypothesis.get("head")
                tail = hypothesis.get("tail")
                self.kg_manager.add_edge(head, tail, confirmed_relation)
                response_text = (
                    f"알겠어요. '{head}'와(과) '{tail}'의 관계를 "
                    f"'{confirmed_relation}'으로 기록했습니다."
                )
            else:
                head = hypothesis.get("head")
                tail = hypothesis.get("tail")
                response_text = f"알겠어요. {head} -> {tail} 관계는 기록하지 않습니다."


        self.core_memory.remove_hypothesis(hypothesis.get("head"), hypothesis.get("tail"), relation=relation)

        context.pending_hypothesis = None

        final_response = self.response_styler.style_response(response_text, emotional_state)

        return {"type": "text", "text": final_response}





class CommandWordHandler:

    def __init__(self, cortex_registry: CortexRegistry, logger: logging.Logger):

        self.cortex_registry = cortex_registry

        self.logger = logger

        self.command_map = {

            r"^(calculate|계산)\s*:": "arithmetic",
        }



    def can_handle(self, message: str) -> bool:

        return any(re.match(pattern, message.strip(), re.IGNORECASE) for pattern in self.command_map)



    def handle(

        self, message: str, context: ConversationContext, emotional_state: EmotionalState

    ) -> Optional[Any]:

        for pattern, cortex_name in self.command_map.items():

            match = re.match(pattern, message.strip(), re.IGNORECASE)

            if match:

                self.logger.info("Command '%s' detected.", cortex_name)

                raw_command = message.strip()[match.end():].strip()

                cortex = self.cortex_registry.get(cortex_name)

                if cortex:

                    result_text = cortex.process(raw_command)

                    return {"type": "text", "text": result_text}

        return None





class DefaultReasoningHandler:

    def __init__(

        self,

        reasoner: LogicalReasoner,

        vcd: ValueCenteredDecision,

        synthesizer: InsightSynthesizer,

        creative_cortex: CreativeCortex,

        styler: ResponseStyler,

        logger: logging.Logger,

        perspective_cortex: PerspectiveCortex,

        question_generator: QuestionGenerator,

        emotional_engine: EmotionalEngine,

    ):

        self.reasoner = reasoner

        self.vcd = vcd

        self.synthesizer = synthesizer

        self.creative_cortex = creative_cortex

        self.styler = styler

        self.logger = logger

        self.perspective_cortex = perspective_cortex

        self.question_generator = question_generator

        self.emotional_engine = emotional_engine

        self.creative_expression_threshold = 2.5



    def handle(

        self, message: str, context: ConversationContext, emotional_state: EmotionalState

    ) -> Optional[Any]:

        potential_thoughts = self.reasoner.deduce_facts(message)



        if not potential_thoughts:
            insightful_text = "흥미로운 관점이네요. 조금 더 생각해볼게요."
            final_response = self.styler.style_response(insightful_text, emotional_state)
            return {"type": "text", "text": final_response}



        chosen_thought = self.vcd.select_thought(

            candidates=potential_thoughts,

            context=[message],

            emotional_state=emotional_state,

            guiding_intention=context.guiding_intention,

        )

        if not chosen_thought:

            chosen_thought = potential_thoughts[0]



        insightful_text = self.synthesizer.synthesize([chosen_thought])

        final_response = self.styler.style_response(insightful_text, emotional_state)



        response_data: Dict[str, Any] = {"type": "text", "text": final_response}

        vcd_score = getattr(chosen_thought, "vcd_score", 0)



        if vcd_score > self.creative_expression_threshold:

            self.logger.info(

                "VCD score (%.2f) exceeded threshold (%.2f). Triggering Creative Cortex.",

                vcd_score,

                self.creative_expression_threshold,

            )

            creative_output = self.creative_cortex.generate_creative_expression(chosen_thought)

            response_data["creative_output"] = creative_output

            response_data["type"] = "composite_insight"



        return response_data


class PlanningHandler:
    """Handles planning requests using the PlanningCortex."""

    def __init__(self, planning_cortex, logger: logging.Logger):
        self.planning_cortex = planning_cortex
        self.logger = logger
        self.trigger_patterns = [
            r"^(plan|계획|goal|목표)\s*[:\s]",
        ]

    def can_handle(self, message: str) -> bool:
        return any(re.match(pattern, message.strip(), re.IGNORECASE) for pattern in self.trigger_patterns)

    def handle(self, message: str, context: ConversationContext, emotional_state: EmotionalState) -> Optional[Any]:
        self.logger.info("PlanningHandler triggered.")
        
        # Extract goal from message
        # Simple extraction: remove the trigger prefix
        goal = message
        for pattern in self.trigger_patterns:
            match = re.match(pattern, message.strip(), re.IGNORECASE)
            if match:
                goal = message.strip()[match.end():].strip()
                break
        
        if not goal:
            return {"type": "text", "text": "계획할 목표를 말씀해 주세요."}

        plan = self.planning_cortex.develop_plan(goal)
        
        if not plan:
            return {"type": "text", "text": "죄송해요, 계획을 세우는 데 실패했어요."}
            
        # Format plan for display
        plan_text = f"목표 '{goal}'에 대한 계획입니다:\n"
        for i, step in enumerate(plan):
            tool_name = step.get('tool_name')
            params = step.get('parameters')
            plan_text += f"{i+1}. **{tool_name}**: {params}\n"
            
        return {"type": "text", "text": plan_text, "plan": plan}
