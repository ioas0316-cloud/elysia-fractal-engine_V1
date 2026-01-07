from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ConversationContext:
    """Holds the state of a conversation."""
    pending_hypothesis: Any = None
    guiding_intention: Any = None
    # Future additions:
    # emotional_state: EmotionalState = field(default_factory=EmotionalState)
    # conversation_history: List[str] = field(default_factory=list)
    # custom_data: Dict[str, Any] = field(default_factory=dict)
