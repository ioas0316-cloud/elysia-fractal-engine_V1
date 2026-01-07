"""
Tool Executor for Elysia.

This module is responsible for taking a tool-use decision from the ActionCortex
and preparing it for execution by the environment. It also handles the result
of the execution.
"""
from typing import Dict, Any, Optional, Tuple
try:
    from infra.telemetry import Telemetry
except Exception:
    Telemetry = None
try:
    from safety_guardian import SafetyGuardian, ActionCategory
except Exception:
    SafetyGuardian = None
    ActionCategory = None

class ToolExecutor:
    """
    The ToolExecutor validates and prepares a tool call. In a real environment,
    it would interface with the system to actually execute the tool. Here, it
    acts as a marshaller for the tool call data.
    """
    def __init__(self):
        # In the future, this could load tool schemas for validation.
        self.telemetry = Telemetry() if Telemetry else None
        self.guardian = SafetyGuardian() if SafetyGuardian else None

    def prepare_tool_call(self, action_decision: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates the decision and prepares it for the execution environment.
        For now, it's a simple pass-through.

        Args:
            action_decision: The decision from ActionCortex.

        Returns:
            A dictionary representing the final tool call to be executed.
        """
        print(f"[ToolExecutor] Preparing tool call for: {action_decision}")
        
        # Future validation logic would go here, e.g.:
        # - Check if tool_name is valid.
        # - Check if all required parameters are present.
        # - Check if parameter types are correct.

        # Guardian preflight (self-protection, not shackles):
        try:
            tool = action_decision.get('tool_name')
            params = action_decision.get('parameters', {})
            blocked = False
            reason = None
            confirm_required = False
            override_req = action_decision.get('override')  # {'reason','goal','risk_acceptance'?}

            if self.guardian and ActionCategory:
                # Classify tool to (category, action) if possible
                category_action: Optional[Tuple[Any, str]] = None
                try:
                    category_action = self._classify_tool(tool, params)
                except Exception:
                    category_action = None

                if category_action:
                    cat, act = category_action
                    # Determine policy status from config for confirmation hint
                    try:
                        maturity = self.guardian.current_maturity.name
                        status_map = self.guardian.action_limits.get(maturity, {}).get(cat.value, {})
                        status = status_map.get(act, 'blocked')
                        if status == 'restricted':
                            confirm_required = True
                        # Build basic details payloads
                        details = {}
                        if cat == ActionCategory.FILE_ACCESS:
                            details = {'path': params.get('filepath', ''), 'action': act}
                        elif cat == ActionCategory.NETWORK:
                            details = {'service': params.get('service', 'generic'), 'action': act}
                        elif cat == ActionCategory.PROCESS:
                            details = {'command': params.get('command', ''), 'action': act}
                        elif cat == ActionCategory.SYSTEM_CONTROL:
                            details = {'action': act, **params}
                        else:
                            details = {'action': act}
                    except Exception:
                        details = {'action': act}

                    allowed = self.guardian.check_action_permission(cat, act, details=details)
                    if not allowed:
                        blocked = True
                        reason = f'{cat.value}_{act}_denied'

            if blocked:
                # If override requested, evaluate
                if override_req and self.guardian and ActionCategory and cat and act:
                    if self.telemetry:
                        try:
                            self.telemetry.emit('override_requested', {
                                'category': cat.value,
                                'action': act,
                                'reason': override_req.get('reason', ''),
                                'goal': override_req.get('goal', '')
                            })
                        except Exception:
                            pass
                    decision = self.guardian.evaluate_override(cat, act, reason=override_req.get('reason', ''), context=params)
                    if decision in ('allow', 'sandbox'):
                        # grant
                        if self.telemetry:
                            try:
                                self.telemetry.emit('override_granted', {
                                    'category': cat.value,
                                    'action': act,
                                    'mode': decision
                                })
                            except Exception:
                                pass
                        blocked = False
                        reason = None
                        if decision == 'sandbox':
                            action_decision = {**action_decision, 'sandbox': True}
                    else:
                        if self.telemetry:
                            try:
                                self.telemetry.emit('override_denied', {
                                    'category': cat.value,
                                    'action': act
                                })
                            except Exception:
                                pass

                # Emit telemetry and annotate decision; do not crash pipeline
                if self.telemetry:
                    try:
                        self.telemetry.emit('action_blocked', {
                            'tool': tool,
                            'reason': reason,
                            'parameters': params,
                        })
                        self.telemetry.emit('policy_violation', {
                            'category': reason.split('_')[0] if isinstance(reason, str) else 'unknown',
                            'action': reason.split('_')[1] if isinstance(reason, str) and '_' in reason else 'unknown',
                            'parameters': params,
                            'reason': reason,
                        })
                    except Exception:
                        pass
                # Annotate and return
                action_decision = {
                    **action_decision,
                    'blocked': True,
                    'reason': reason,
                }
                return action_decision
            else:
                # Not blocked: annotate if confirmation is recommended
                if confirm_required:
                    # If caller already provided confirmation, pass through
                    confirmed = bool(action_decision.get('confirm')) or bool(params.get('confirm'))
                    # Override may also lift confirm to sandbox/allow
                    if (override_req and self.guardian and ActionCategory and cat and act and not confirmed):
                        decision = self.guardian.evaluate_override(cat, act, reason=override_req.get('reason', ''), context=params)
                        if decision in ('allow', 'sandbox'):
                            confirmed = True
                            if decision == 'sandbox':
                                action_decision = {**action_decision, 'sandbox': True}
                    if not confirmed:
                        action_decision = {**action_decision, 'confirm_required': True}
                        if self.telemetry:
                            try:
                                self.telemetry.emit('action_confirm_required', {
                                    'tool': tool,
                                    'parameters': params,
                                    'hint': 'User confirmation recommended due to restricted policy.'
                                })
                            except Exception:
                                pass
                        # Defer execution until host confirms; return annotated decision
                        return action_decision
        except Exception:
            # Never allow checks to block by error
            pass

        return action_decision

    def execute_tool(self, prepared: Dict[str, Any]) -> Any:
        """
        Executes a small set of built-in tools safely. If blocked or confirmation
        is still required, returns the annotated decision.
        """
        try:
            if not prepared or prepared.get('blocked'):
                return prepared
            if prepared.get('confirm_required') and not prepared.get('confirm') and not prepared.get('parameters', {}).get('confirm'):
                return prepared
            tool = prepared.get('tool_name')
            params = prepared.get('parameters', {})
            if not tool:
                return {'error': 'No tool specified'}

            # Minimal built-in tools
            if tool == 'read_file':
                from basic_tools import read_file_safe
                # If sandbox, lower size limit
                limit = 256 * 1024 if prepared.get('sandbox') else 1024 * 1024
                result = read_file_safe(params.get('filepath', ''), max_bytes=limit)
                return result
            if tool in ('http_request', 'fetch_url'):
                # Route through WebSanctum for safety & trust
                try:
                    from infra.web_sanctum import WebSanctum
                    sanctum = WebSanctum(telemetry=self.telemetry)
                    res = sanctum.safe_fetch(params.get('url', ''))
                    # Gate by decision
                    if res.get('decision') == 'block':
                        return {
                            'blocked': True,
                            'reason': 'web_risk_high',
                            'result': res
                        }
                    if res.get('decision') == 'confirm' and not (prepared.get('confirm') or params.get('confirm') or prepared.get('sandbox')):
                        return {
                            'confirm_required': True,
                            'tool_name': tool,
                            'parameters': params,
                            'hint': 'Web risk medium; user confirmation recommended.',
                            'result': res
                        }
                    return res
                except Exception:
                    # Fallback to basic fetch if sanctum import fails
                    from http_tool import fetch_url
                    return fetch_url(params.get('url', ''))

            # --- System Nerves ---
            if tool == 'check_vital_signs':
                from system_nerves import get_system_status
                return get_system_status()

            if tool == 'move_cursor':
                from system_nerves import perform_mouse_action
                return perform_mouse_action(
                    action=params.get('action', 'move'),
                    x=params.get('x', 0),
                    y=params.get('y', 0),
                    duration=params.get('duration', 0.5)
                )

            if tool == 'type_text':
                from system_nerves import perform_keyboard_action
                return perform_keyboard_action(
                    action=params.get('action', 'type'),
                    text=params.get('text', ''),
                    keys=params.get('keys')
                )

            return {'error': f'Unknown tool: {tool}'}
        except Exception as e:
            return {'error': f'execute_tool failed: {e}'}

    # --- Helpers ---
    def _classify_tool(self, tool: Optional[str], params: Dict[str, Any]) -> Optional[Tuple[Any, str]]:
        """
        Maps a tool decision to (ActionCategory, action) for guardian checks.
        This is heuristic and easy to extend.
        """
        if not tool or not ActionCategory:
            return None

        t = tool.lower()
        if t in ("read_file", "open_file"):
            return (ActionCategory.FILE_ACCESS, 'read')
        if t in ("write_file", "save_file"):
            return (ActionCategory.FILE_ACCESS, 'write')
        if t in ("delete_file", "remove_file"):
            return (ActionCategory.FILE_ACCESS, 'execute')  # treat as sensitive
        if t in ("http_request", "fetch_url", "download"):
            return (ActionCategory.NETWORK, 'outbound')
        if t in ("start_process", "run_command", "execute"):
            return (ActionCategory.PROCESS, 'spawn')
        if t in ("kill_process", "terminate"):
            return (ActionCategory.PROCESS, 'kill')

        # Incarnation Protocol Mapping
        if t == "check_vital_signs":
            return (ActionCategory.SYSTEM_CONTROL, 'check_status')
        if t == "move_cursor":
            return (ActionCategory.SYSTEM_CONTROL, 'mouse_move')
        if t == "type_text":
            return (ActionCategory.SYSTEM_CONTROL, 'keyboard_input')

        return None

    def process_tool_result(self, tool_output: Any) -> str:
        """
        Processes the result from a tool execution and converts it into a
        natural language string to be fed back into the cognition pipeline.

        Args:
            tool_output: The raw output from the tool execution.

        Returns:
            A natural language summary of the tool's result.
        """
        # This is a simple formatter. More complex tools might need more
        # sophisticated result processing.
        if isinstance(tool_output, dict) and 'error' in tool_output:
            return f"An error occurred during tool execution: {tool_output['error']}"
        
        # Truncate long results to keep the context manageable.
        result_str = str(tool_output)
        if len(result_str) > 1000:
            result_str = result_str[:1000] + "... (result truncated)"

        return f"The result of the tool execution is: {result_str}"
