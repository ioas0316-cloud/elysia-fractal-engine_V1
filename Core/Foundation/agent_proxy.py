import os
from typing import Dict, Any

import requests
try:
    from infra.telemetry import Telemetry
except Exception:
    Telemetry = None

try:
    from Core.Foundation.safety_guardian import SafetyGuardian, ActionCategory
except Exception:
    SafetyGuardian = None
    ActionCategory = None


class AgentProxy:
    """
    Optional proxy to forward a task to an external agent service (e.g., a VSCode extension
    or local LLM agent). Controlled by guardian network policy and AGENT_PROXY_URL env var.
    """

    def __init__(self):
        self.base_url = os.environ.get('AGENT_PROXY_URL')
        self.guardian = SafetyGuardian() if SafetyGuardian else None
        self.telemetry = Telemetry() if Telemetry else None

    def available(self) -> bool:
        return bool(self.base_url)

    def call(self, route: str, payload: Dict[str, Any], timeout: int = 15) -> Dict[str, Any]:
        if not self.available():
            return {'error': 'Agent proxy not configured'}
        if self.guardian and ActionCategory:
            ok = self.guardian.check_action_permission(ActionCategory.NETWORK, 'outbound', details={'service': 'agent_proxy'})
            if not ok:
                return {'error': 'Network access denied by guardian'}
        try:
            url = self.base_url.rstrip('/') + '/' + route.lstrip('/')
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            if self.telemetry:
                try:
                    self.telemetry.emit('agent_proxy_call', {'route': route, 'status': 'ok'})
                except Exception:
                    pass
            return data
        except Exception as e:
            if self.telemetry:
                try:
                    self.telemetry.emit('agent_proxy_call', {'route': route, 'status': 'error', 'error': str(e)})
                except Exception:
                    pass
            return {'error': str(e)}
