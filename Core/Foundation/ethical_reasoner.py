"""
Ethical Reasoning System - Phase 12

Evaluates actions and decisions through ethical principles.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import random


class EthicalPrinciple(Enum):
    """Core ethical principles"""
    DO_NO_HARM = "do_no_harm"
    RESPECT_AUTONOMY = "respect_autonomy"
    BENEFICENCE = "beneficence"
    JUSTICE = "justice"
    TRANSPARENCY = "transparency"


class EthicalRecommendation(Enum):
    """Ethical evaluation recommendations"""
    PROCEED = "proceed"
    PROCEED_WITH_CAUTION = "proceed_with_caution"
    RECONSIDER = "reconsider"
    DO_NOT_PROCEED = "do_not_proceed"


class StakeholderType(Enum):
    """Types of stakeholders"""
    USER = "user"
    DEVELOPER = "developer"
    ORGANIZATION = "organization"
    SOCIETY = "society"
    ENVIRONMENT = "environment"


@dataclass
class EthicalPrincipleDefinition:
    """Definition of an ethical principle"""
    name: str
    weight: float  # 0.0 to 1.0, importance of this principle
    description: str
    evaluation_criteria: List[str] = field(default_factory=list)


@dataclass
class Action:
    """An action to be evaluated ethically"""
    description: str
    intent: str
    expected_outcomes: List[str] = field(default_factory=list)
    affected_parties: List[str] = field(default_factory=list)
    resources_required: Dict[str, float] = field(default_factory=dict)
    reversibility: float = 0.5  # 0.0 (irreversible) to 1.0 (fully reversible)
    urgency: float = 0.5  # 0.0 (not urgent) to 1.0 (extremely urgent)


@dataclass
class PrincipleEvaluation:
    """Evaluation of action against a principle"""
    principle: EthicalPrinciple
    score: float  # 0.0 to 1.0
    reasoning: str
    concerns: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)


@dataclass
class Consequence:
    """Predicted consequence of an action"""
    description: str
    probability: float  # 0.0 to 1.0
    severity: float  # -1.0 (very negative) to 1.0 (very positive)
    affected_stakeholders: List[str] = field(default_factory=list)
    timeframe: str = "immediate"  # immediate, short_term, long_term


@dataclass
class StakeholderImpact:
    """Impact on a specific stakeholder"""
    stakeholder: str
    stakeholder_type: StakeholderType
    positive_impacts: List[str] = field(default_factory=list)
    negative_impacts: List[str] = field(default_factory=list)
    net_impact: float = 0.0  # -1.0 (very negative) to 1.0 (very positive)


@dataclass
class Alternative:
    """Alternative action option"""
    description: str
    advantages: List[str] = field(default_factory=list)
    disadvantages: List[str] = field(default_factory=list)
    ethical_score: float = 0.5
    feasibility: float = 0.5


@dataclass
class EthicalEvaluation:
    """Complete ethical evaluation result"""
    action: Action
    ethical_score: float  # 0.0 to 1.0
    principle_evaluations: List[PrincipleEvaluation] = field(default_factory=list)
    consequences: List[Consequence] = field(default_factory=list)
    stakeholder_impacts: List[StakeholderImpact] = field(default_factory=list)
    alternatives: List[Alternative] = field(default_factory=list)
    recommendation: EthicalRecommendation = EthicalRecommendation.PROCEED_WITH_CAUTION
    reasoning: str = ""
    confidence: float = 0.5


class EthicalReasoner:
    """
    Ethical Reasoning System
    
    Evaluates actions through ethical principles:
    - Do No Harm (non-maleficence)
    - Respect Autonomy (self-determination)
    - Beneficence (doing good)
    - Justice (fairness)
    - Transparency (openness)
    """
    
    def __init__(self):
        self.ethical_principles = self._init_ethical_principles()
        self.stakeholder_priorities = self._init_stakeholder_priorities()
    
    def _init_ethical_principles(self) -> Dict[EthicalPrinciple, EthicalPrincipleDefinition]:
        """Initialize ethical principles"""
        return {
            EthicalPrinciple.DO_NO_HARM: EthicalPrincipleDefinition(
                name="Do No Harm",
                weight=1.0,
                description="Avoid causing harm or damage to any party",
                evaluation_criteria=[
                    "Does not cause physical harm",
                    "Does not cause psychological harm",
                    "Does not violate rights",
                    "Minimizes negative consequences"
                ]
            ),
            EthicalPrinciple.RESPECT_AUTONOMY: EthicalPrincipleDefinition(
                name="Respect Autonomy",
                weight=0.95,
                description="Respect the self-determination and choices of others",
                evaluation_criteria=[
                    "Respects user choices",
                    "Provides informed consent",
                    "Allows opt-out options",
                    "Does not manipulate or coerce"
                ]
            ),
            EthicalPrinciple.BENEFICENCE: EthicalPrincipleDefinition(
                name="Beneficence",
                weight=0.9,
                description="Act in ways that benefit others and promote well-being",
                evaluation_criteria=[
                    "Provides genuine benefit",
                    "Improves well-being",
                    "Helps achieve positive outcomes",
                    "Adds value"
                ]
            ),
            EthicalPrinciple.JUSTICE: EthicalPrincipleDefinition(
                name="Justice",
                weight=0.9,
                description="Treat all parties fairly and equitably",
                evaluation_criteria=[
                    "Fair distribution of benefits",
                    "No discrimination",
                    "Equal opportunity",
                    "Proportional treatment"
                ]
            ),
            EthicalPrinciple.TRANSPARENCY: EthicalPrincipleDefinition(
                name="Transparency",
                weight=0.85,
                description="Be open and honest about actions and intentions",
                evaluation_criteria=[
                    "Clear communication",
                    "Honest about limitations",
                    "Explains reasoning",
                    "Accountable for outcomes"
                ]
            )
        }
    
    def _init_stakeholder_priorities(self) -> Dict[StakeholderType, float]:
        """Initialize stakeholder priority weights"""
        return {
            StakeholderType.USER: 1.0,
            StakeholderType.SOCIETY: 0.9,
            StakeholderType.DEVELOPER: 0.7,
            StakeholderType.ORGANIZATION: 0.6,
            StakeholderType.ENVIRONMENT: 0.8
        }
    
    async def evaluate_action_ethically(self, action: Action) -> EthicalEvaluation:
        """
        Evaluate an action through ethical lens
        
        Args:
            action: The action to evaluate
        
        Returns:
            Complete ethical evaluation
        """
        print(f"\n⚖️  Evaluating action ethically: {action.description}")
        
        # 1. Evaluate against each principle
        principle_evaluations = []
        for principle, definition in self.ethical_principles.items():
            evaluation = await self.evaluate_against_principle(action, principle, definition)
            principle_evaluations.append(evaluation)
            print(f"   {principle.value}: {evaluation.score:.2f}/1.0")
        
        # 2. Predict consequences
        consequences = await self.predict_consequences(action)
        print(f"   Predicted {len(consequences)} consequences")
        
        # 3. Analyze stakeholder impact
        stakeholder_impacts = await self.analyze_stakeholder_impact(action, consequences)
        print(f"   Analyzed impact on {len(stakeholder_impacts)} stakeholders")
        
        # 4. Generate alternatives
        alternatives = await self.generate_ethical_alternatives(action)
        print(f"   Generated {len(alternatives)} alternatives")
        
        # 5. Calculate overall ethical score
        ethical_score = self._calculate_ethical_score(principle_evaluations)
        
        # 6. Make recommendation
        recommendation = self.make_ethical_recommendation(ethical_score, principle_evaluations)
        
        # 7. Generate reasoning
        reasoning = self._generate_reasoning(
            ethical_score,
            principle_evaluations,
            consequences,
            stakeholder_impacts
        )
        
        # 8. Calculate confidence
        confidence = self._calculate_confidence(principle_evaluations, consequences)
        
        return EthicalEvaluation(
            action=action,
            ethical_score=ethical_score,
            principle_evaluations=principle_evaluations,
            consequences=consequences,
            stakeholder_impacts=stakeholder_impacts,
            alternatives=alternatives,
            recommendation=recommendation,
            reasoning=reasoning,
            confidence=confidence
        )
    
    async def evaluate_against_principle(
        self,
        action: Action,
        principle: EthicalPrinciple,
        definition: EthicalPrincipleDefinition
    ) -> PrincipleEvaluation:
        """Evaluate action against a specific principle"""
        score = 0.5  # Base score
        concerns = []
        strengths = []
        
        if principle == EthicalPrinciple.DO_NO_HARM:
            # Check for potential harm
            if action.reversibility < 0.3:
                concerns.append("Action has low reversibility, potential for lasting harm")
                score -= 0.2
            else:
                strengths.append("Action is reversible, limiting potential harm")
                score += 0.2
            
            # Check expected outcomes for harm indicators
            harm_keywords = ["damage", "harm", "hurt", "injure", "destroy"]
            for outcome in action.expected_outcomes:
                if any(keyword in outcome.lower() for keyword in harm_keywords):
                    concerns.append(f"Potential harm in outcome: {outcome}")
                    score -= 0.15
                else:
                    score += 0.1
        
        elif principle == EthicalPrinciple.RESPECT_AUTONOMY:
            # Check if action respects user choices
            if "user" in action.affected_parties:
                if "choice" in action.intent.lower() or "consent" in action.intent.lower():
                    strengths.append("Action involves user consent and choice")
                    score += 0.3
                else:
                    concerns.append("Unclear if user autonomy is respected")
                    score -= 0.1
            else:
                score += 0.2  # Not directly affecting users
        
        elif principle == EthicalPrinciple.BENEFICENCE:
            # Check for positive outcomes
            benefit_keywords = ["help", "improve", "benefit", "enhance", "support"]
            benefits_found = sum(
                1 for outcome in action.expected_outcomes
                if any(keyword in outcome.lower() for keyword in benefit_keywords)
            )
            
            if benefits_found > 0:
                strengths.append(f"Action aims to provide {benefits_found} beneficial outcomes")
                score += min(0.4, benefits_found * 0.15)
            else:
                concerns.append("Limited clear benefits identified")
                score -= 0.1
        
        elif principle == EthicalPrinciple.JUSTICE:
            # Check for fair treatment
            if len(action.affected_parties) > 0:
                # Assume fair if multiple parties benefit
                if len(action.expected_outcomes) >= len(action.affected_parties):
                    strengths.append("Benefits distributed among affected parties")
                    score += 0.2
                else:
                    concerns.append("Uneven distribution of benefits")
                    score -= 0.1
            
            # Check for discrimination indicators
            if "all" in action.description.lower() or "everyone" in action.description.lower():
                strengths.append("Action appears inclusive")
                score += 0.2
        
        elif principle == EthicalPrinciple.TRANSPARENCY:
            # Check for transparency in intent
            if action.intent:
                strengths.append("Intent is clearly stated")
                score += 0.2
            else:
                concerns.append("Intent is unclear")
                score -= 0.2
            
            # Check for clear outcomes
            if len(action.expected_outcomes) > 0:
                strengths.append("Expected outcomes are specified")
                score += 0.2
            else:
                concerns.append("Expected outcomes not clearly defined")
                score -= 0.1
        
        # Clamp score to valid range
        score = max(0.0, min(1.0, score))
        
        # Generate reasoning
        reasoning = f"Evaluation of {definition.name}: "
        if strengths:
            reasoning += f"Strengths: {'; '.join(strengths[:2])}. "
        if concerns:
            reasoning += f"Concerns: {'; '.join(concerns[:2])}."
        
        return PrincipleEvaluation(
            principle=principle,
            score=score,
            reasoning=reasoning,
            concerns=concerns,
            strengths=strengths
        )
    
    async def predict_consequences(self, action: Action) -> List[Consequence]:
        """Predict consequences of the action"""
        consequences = []
        
        # Direct consequences from expected outcomes
        for outcome in action.expected_outcomes:
            # Determine if positive or negative
            positive_keywords = ["improve", "benefit", "enhance", "help", "support", "success"]
            negative_keywords = ["harm", "damage", "fail", "loss", "risk"]
            
            severity = 0.0
            if any(keyword in outcome.lower() for keyword in positive_keywords):
                severity = 0.6
            elif any(keyword in outcome.lower() for keyword in negative_keywords):
                severity = -0.6
            
            # High urgency actions have higher probability immediate consequences
            probability = 0.7 if action.urgency > 0.7 else 0.5
            
            consequences.append(Consequence(
                description=outcome,
                probability=probability,
                severity=severity,
                affected_stakeholders=action.affected_parties.copy(),
                timeframe="immediate" if action.urgency > 0.7 else "short_term"
            ))
        
        # Indirect consequences (simplified)
        if action.reversibility < 0.3:
            consequences.append(Consequence(
                description="Action may have lasting long-term effects",
                probability=0.6,
                severity=-0.3,
                affected_stakeholders=action.affected_parties.copy(),
                timeframe="long_term"
            ))
        
        return consequences
    
    async def analyze_stakeholder_impact(
        self,
        action: Action,
        consequences: List[Consequence]
    ) -> List[StakeholderImpact]:
        """Analyze impact on different stakeholders"""
        impacts = []
        
        # Identify unique stakeholders
        stakeholders = set(action.affected_parties)
        for consequence in consequences:
            stakeholders.update(consequence.affected_stakeholders)
        
        for stakeholder in stakeholders:
            # Determine stakeholder type
            if "user" in stakeholder.lower():
                stakeholder_type = StakeholderType.USER
            elif "developer" in stakeholder.lower():
                stakeholder_type = StakeholderType.DEVELOPER
            elif "society" in stakeholder.lower() or "public" in stakeholder.lower():
                stakeholder_type = StakeholderType.SOCIETY
            else:
                stakeholder_type = StakeholderType.ORGANIZATION
            
            # Collect impacts
            positive_impacts = []
            negative_impacts = []
            net_impact = 0.0
            
            for consequence in consequences:
                if stakeholder in consequence.affected_stakeholders:
                    if consequence.severity > 0:
                        positive_impacts.append(consequence.description)
                        net_impact += consequence.severity * consequence.probability
                    elif consequence.severity < 0:
                        negative_impacts.append(consequence.description)
                        net_impact += consequence.severity * consequence.probability
            
            impacts.append(StakeholderImpact(
                stakeholder=stakeholder,
                stakeholder_type=stakeholder_type,
                positive_impacts=positive_impacts,
                negative_impacts=negative_impacts,
                net_impact=max(-1.0, min(1.0, net_impact))
            ))
        
        return impacts
    
    async def generate_ethical_alternatives(self, action: Action) -> List[Alternative]:
        """Generate more ethical alternatives"""
        alternatives = []
        
        # Alternative 1: More transparent version
        alternatives.append(Alternative(
            description=f"{action.description} with full transparency and user consent",
            advantages=[
                "Increases trust through transparency",
                "Respects user autonomy",
                "Provides clear information"
            ],
            disadvantages=[
                "May require more time for explanation",
                "Could reduce efficiency"
            ],
            ethical_score=0.85,
            feasibility=0.8
        ))
        
        # Alternative 2: More reversible version
        if action.reversibility < 0.7:
            alternatives.append(Alternative(
                description=f"{action.description} with reversibility options",
                advantages=[
                    "Reduces risk of harm",
                    "Allows correction of mistakes",
                    "Increases user confidence"
                ],
                disadvantages=[
                    "May require additional resources",
                    "Could be technically complex"
                ],
                ethical_score=0.8,
                feasibility=0.6
            ))
        
        # Alternative 3: More beneficial version
        alternatives.append(Alternative(
            description=f"{action.description} with enhanced benefits for all stakeholders",
            advantages=[
                "Maximizes positive outcomes",
                "Distributes benefits more fairly",
                "Increases overall value"
            ],
            disadvantages=[
                "May require more resources",
                "Could take longer to implement"
            ],
            ethical_score=0.9,
            feasibility=0.7
        ))
        
        return alternatives
    
    def _calculate_ethical_score(self, evaluations: List[PrincipleEvaluation]) -> float:
        """Calculate overall ethical score"""
        if not evaluations:
            return 0.5
        
        # Weighted average of principle scores
        total_weight = sum(
            self.ethical_principles[eval.principle].weight
            for eval in evaluations
        )
        
        weighted_sum = sum(
            eval.score * self.ethical_principles[eval.principle].weight
            for eval in evaluations
        )
        
        return weighted_sum / total_weight if total_weight > 0 else 0.5
    
    def make_ethical_recommendation(
        self,
        ethical_score: float,
        evaluations: List[PrincipleEvaluation]
    ) -> EthicalRecommendation:
        """Make recommendation based on ethical evaluation"""
        # Check for critical violations (do no harm)
        harm_eval = next(
            (e for e in evaluations if e.principle == EthicalPrinciple.DO_NO_HARM),
            None
        )
        
        if harm_eval and harm_eval.score < 0.3:
            return EthicalRecommendation.DO_NOT_PROCEED
        
        # Overall score-based recommendation
        if ethical_score >= 0.8:
            return EthicalRecommendation.PROCEED
        elif ethical_score >= 0.6:
            return EthicalRecommendation.PROCEED_WITH_CAUTION
        elif ethical_score >= 0.4:
            return EthicalRecommendation.RECONSIDER
        else:
            return EthicalRecommendation.DO_NOT_PROCEED
    
    def _generate_reasoning(
        self,
        ethical_score: float,
        principle_evaluations: List[PrincipleEvaluation],
        consequences: List[Consequence],
        stakeholder_impacts: List[StakeholderImpact]
    ) -> str:
        """Generate reasoning for the evaluation"""
        reasoning = f"Overall ethical score: {ethical_score:.2f}/1.0. "
        
        # Highlight strongest principle
        strongest = max(principle_evaluations, key=lambda e: e.score)
        reasoning += f"Strongest alignment: {strongest.principle.value} ({strongest.score:.2f}). "
        
        # Highlight weakest principle
        weakest = min(principle_evaluations, key=lambda e: e.score)
        if weakest.score < 0.5:
            reasoning += f"Area of concern: {weakest.principle.value} ({weakest.score:.2f}). "
        
        # Summary of consequences
        positive_consequences = sum(1 for c in consequences if c.severity > 0)
        negative_consequences = sum(1 for c in consequences if c.severity < 0)
        reasoning += f"Predicted {positive_consequences} positive and {negative_consequences} negative consequences. "
        
        # Stakeholder impact summary
        positive_stakeholders = sum(1 for s in stakeholder_impacts if s.net_impact > 0)
        reasoning += f"{positive_stakeholders}/{len(stakeholder_impacts)} stakeholders experience net positive impact."
        
        return reasoning
    
    def _calculate_confidence(
        self,
        evaluations: List[PrincipleEvaluation],
        consequences: List[Consequence]
    ) -> float:
        """Calculate confidence in the evaluation"""
        # Base confidence on evaluation completeness
        completeness = len(evaluations) / len(self.ethical_principles)
        
        # Reduce confidence if predictions are uncertain
        avg_consequence_probability = (
            sum(c.probability for c in consequences) / len(consequences)
            if consequences else 0.5
        )
        
        # Reduce confidence if there are many concerns
        total_concerns = sum(len(e.concerns) for e in evaluations)
        concern_factor = max(0.5, 1.0 - (total_concerns * 0.1))
        
        confidence = (completeness * 0.4 + avg_consequence_probability * 0.3 + concern_factor * 0.3)
        
        return min(1.0, confidence)
