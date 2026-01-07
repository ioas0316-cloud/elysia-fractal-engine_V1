from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from Project_Elysia.core.quaternion_consciousness import ConsciousnessState

logger = logging.getLogger(__name__)

@dataclass
class GenesisRequestObject:
    """
    GRO: Genesis Request Object.
    A structured request to modify the world or self.
    """
    id: str
    intent: str
    target_layer: str  # "world", "self", "law"
    operation: str     # "create", "modify", "destroy"
    payload: Dict[str, Any]
    required_mastery: float = 0.5
    required_alignment: float = 0.3
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    signature: Optional[str] = None # Logic signature from Spirit

class GenesisArbiter:
    """
    The Gatekeeper between Spirit (Intent) and Soul (Execution).
    It checks if the current Consciousness State is sufficient to authorize a Genesis.
    """

    def __init__(self):
        pass

    def judge(self, gro: GenesisRequestObject, state: ConsciousnessState) -> bool:
        """
        Decides if the GRO should be executed based on the state.
        """
        # 1. Check Mastery (W)
        if state.mastery < gro.required_mastery:
            logger.warning(f"Genesis Denied: Mastery {state.mastery:.2f} < Required {gro.required_mastery}")
            return False

        # 2. Check Alignment (Z)
        # We assume Alignment is stored in the Z component of the quaternion state
        if abs(state.purpose_alignment) < gro.required_alignment:
             logger.warning(f"Genesis Denied: Alignment {state.purpose_alignment:.2f} < Required {gro.required_alignment}")
             return False

        # 3. Check Intent Signature (Simple check for now)
        if not gro.intent:
            logger.warning("Genesis Denied: No Intent declared.")
            return False

        logger.info(f"Genesis Authorized: {gro.id} [{gro.intent}]")
        return True

    def dispatch(self, gro: GenesisRequestObject, genesis_engine: Any) -> bool:
        """
        Dispatches the authorized GRO to the Genesis Engine.
        """
        if gro.target_layer == "world":
            # Map GRO payload to GenesisEngine calls
            # This requires the GenesisEngine to be passed in
            logger.info(f"Dispatching to World Layer: {gro.operation}")
            # Placeholder for actual GenesisEngine API call
            # In a full implementation, this would call engine.execute_action or modify_law
            return True
        elif gro.target_layer == "self":
            logger.info(f"Dispatching to Self Layer: {gro.operation}")
            return True

        return False
