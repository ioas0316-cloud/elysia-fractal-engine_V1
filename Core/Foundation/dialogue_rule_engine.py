"""
Dialogue Rule Engine (declarative)

Loads YAML rule files from data/dialogue_rules and applies them to user
messages before falling back to heuristic/internal generation.

Rule schema (YAML):
  id: greeting
  priority: 100
  patterns:
    - "^(안녕|안녕하세요|hello|hi)"
  gates:
    quiet_ok: true   # if false, suppress when quiet_mode is ON
  response:
    template: "안녕하세요. 여기 있어요. 오늘 이 순간, 무엇을 함께 보고 싶으세요?"
  memory:
    # optional identity ops; supports group names from regex '(?P<name>...)'
    set_identity:
      user_name: "{name}"

Notes:
- The engine is intentionally simple and transparent. It hot‑reloads rules
  when files change (mtime check) to avoid restarts during iteration.
"""
from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import yaml
from preferences import load_prefs, ensure_defaults, save_prefs
import os


RULE_DIR = os.path.join("data", "dialogue_rules")


@dataclass
class MatchResult:
    rule_id: str
    priority: int
    response_text: str


class DialogueRuleEngine:
    def __init__(self, core_memory=None):
        self.core_memory = core_memory
        self._rules: List[Dict[str, Any]] = []
        self._last_load = 0.0
        self._mtimes: Dict[str, float] = {}
        self._load_rules()

    def _load_rules(self):
        try:
            os.makedirs(RULE_DIR, exist_ok=True)
            mtimes = {}
            rules: List[Dict[str, Any]] = []
            for name in sorted(os.listdir(RULE_DIR)):
                if not name.lower().endswith(('.yml', '.yaml')):
                    continue
                path = os.path.join(RULE_DIR, name)
                mtimes[path] = os.path.getmtime(path)
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
                    if isinstance(data, dict):
                        data['__file'] = path
                        rules.append(data)
            self._rules = rules
            self._mtimes = mtimes
            self._last_load = time.time()
        except Exception:
            # keep previous rules if load fails
            pass

    def _maybe_reload(self):
        try:
            for path, old_m in list(self._mtimes.items()):
                if not os.path.exists(path) or os.path.getmtime(path) != old_m:
                    self._load_rules()
                    return
            # New files?
            if any(n.lower().endswith(('.yml', '.yaml')) for n in os.listdir(RULE_DIR)):
                # directory changed; rely on mtime check above
                pass
        except Exception:
            pass

    def apply(self, message: str) -> Optional[MatchResult]:
        self._maybe_reload()
        prefs = ensure_defaults(load_prefs())
        quiet = bool(prefs.get('quiet_mode', False))
        msg = message or ""
        low = msg.lower()
        candidates: List[MatchResult] = []
        for rule in self._rules:
            rid = str(rule.get('id', os.path.basename(rule.get('__file','rule'))))
            priority = int(rule.get('priority', 0))
            gates = rule.get('gates', {}) or {}
            if quiet and not gates.get('quiet_ok', True):
                continue
            pats = rule.get('patterns') or []
            matched = None
            for p in pats:
                try:
                    m = re.search(p, msg)
                    if m:
                        matched = m
                        break
                except re.error:
                    continue
            if not matched:
                continue

            # Response text (format with named groups)
            resp = rule.get('response', {}) or {}
            templ = resp.get('template', '')
            try:
                response_text = templ.format(**matched.groupdict())
            except Exception:
                response_text = templ

            # Memory ops (identity only for now)
            mem = rule.get('memory', {}) or {}
            sets = mem.get('set_identity', {}) or {}
            if sets and self.core_memory is not None:
                for k, v in sets.items():
                    try:
                        val = v.format(**matched.groupdict()) if isinstance(v, str) else v
                        if val:
                            self.core_memory.update_identity(k, val)
                    except Exception:
                        pass

            # Optional actions: set preferences or flow profile for intuitive switches
            try:
                actions = rule.get('actions', {}) or {}
                # set_pref: {key: value}
                if 'set_pref' in actions and isinstance(actions['set_pref'], dict):
                    p = ensure_defaults(load_prefs())
                    changed = False
                    for k, v in actions['set_pref'].items():
                        if p.get(k) != v:
                            p[k] = v
                            changed = True
                    if changed:
                        save_prefs(p)
                # set_flow_profile: "learning" | "generic" | path
                prof = actions.get('set_flow_profile')
                if isinstance(prof, str) and prof.strip():
                    try:
                        profile_file = os.path.join('data', 'flows', 'profile.txt')
                        with open(profile_file, 'w', encoding='utf-8') as pf:
                            pf.write(prof.strip())
                    except Exception:
                        pass
            except Exception:
                pass

            candidates.append(MatchResult(rule_id=rid, priority=priority, response_text=response_text))

        if not candidates:
            return None
        # Highest priority wins; if tie, first loaded wins
        best = sorted(candidates, key=lambda r: r.priority, reverse=True)[0]
        return best
