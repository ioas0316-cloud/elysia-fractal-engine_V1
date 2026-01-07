'''
Proactive Assistance Engine

Detects opportunities and provides timely, context-aware assistance.
'''

import time
import json
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path


class AssistanceType(Enum):
    INFORMATION = "information"
    TASK = "task"
    REMINDER = "reminder"
    SUGGESTION = "suggestion"
    WARNING = "warning"
    CELEBRATION = "celebration"


@dataclass
class Opportunity:
    opportunity_id: str
    type: AssistanceType
    description: str
    priority: float
    context: Dict[str, Any]
    appropriateness_score: float
    timing_recommendation: str


class ProactiveAssistant:
    def __init__(self):
        self.opportunities_history: List[Opportunity] = []
        self.user_preferences: Dict[str, Any] = {"max_interruptions_per_hour": 3}
        self.data_dir = Path("data/social/assistance")
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    async def detect_opportunities(
        self,
        context: Dict[str, Any],
        user_state: Dict[str, Any]
    ) -> List[Opportunity]:
        opportunities = []
        
        # Detect reminder opportunities
        if context.get("upcoming_events"):
            for event in context["upcoming_events"]:
                opportunities.append(Opportunity(
                    opportunity_id=f"reminder_{int(time.time())}",
                    type=AssistanceType.REMINDER,
                    description=f"Reminder: {event['name']} in {event['time_until']}",
                    priority=0.9,
                    context=event,
                    appropriateness_score=0.85,
                    timing_recommendation="immediate"
                ))
        
        # Detect suggestion opportunities
        if context.get("current_task") == "writing code":
            if context.get("code_complexity", 0) > 0.7:
                opportunities.append(Opportunity(
                    opportunity_id=f"suggestion_{int(time.time())}",
                    type=AssistanceType.SUGGESTION,
                    description="Consider refactoring for better maintainability",
                    priority=0.6,
                    context={"task": "refactoring"},
                    appropriateness_score=0.70,
                    timing_recommendation="when_convenient"
                ))
        
        # Detect information opportunities
        if context.get("search_queries"):
            opportunities.append(Opportunity(
                opportunity_id=f"info_{int(time.time())}",
                type=AssistanceType.INFORMATION,
                description="Found relevant information for your query",
                priority=0.5,
                context={"info_type": "search_result"},
                appropriateness_score=0.65,
                timing_recommendation="when_convenient"
            ))
        
        # Filter by appropriateness
        focus_level = user_state.get("focus_level", 0.5)
        if focus_level > 0.8:
            # High focus, only show high priority
            opportunities = [o for o in opportunities if o.priority > 0.8]
        
        return sorted(opportunities, key=lambda x: x.priority, reverse=True)
    
    async def provide_assistance(
        self,
        opportunity_id: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        # Find opportunity
        opportunity = next(
            (o for o in self.opportunities_history if o.opportunity_id == opportunity_id),
            None
        )
        
        if not opportunity:
            return {"status": "not_found"}
        
        # Generate assistance based on type
        if opportunity.type == AssistanceType.REMINDER:
            assistance = {
                "type": "reminder",
                "message": opportunity.description,
                "action_required": True
            }
        elif opportunity.type == AssistanceType.SUGGESTION:
            assistance = {
                "type": "suggestion",
                "message": opportunity.description,
                "action_required": False,
                "details": "Consider this improvement when convenient"
            }
        else:
            assistance = {
                "type": opportunity.type.value,
                "message": opportunity.description
            }
        
        self._save_assistance(opportunity, assistance)
        
        return assistance
    
    def _save_assistance(self, opportunity: Opportunity, assistance: Dict[str, Any]):
        timestamp = int(time.time() * 1000)
        filename = self.data_dir / f"assistance_{timestamp}.json"
        
        data = {
            "opportunity": {
                "id": opportunity.opportunity_id,
                "type": opportunity.type.value,
                "priority": opportunity.priority
            },
            "assistance": assistance,
            "timestamp": time.time()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
