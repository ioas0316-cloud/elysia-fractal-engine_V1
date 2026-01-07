"""
Math Cortex (수학 피질)
=====================

원본: Legacy/Project_Sophia/math_cortex.py
마이그레이션: 2025-12-15

기본 산술 등식에 대한 해석 가능한 증명 엔진을 제공합니다.
사람이 읽을 수 있는 단계별 증명을 생성합니다.
"""
from dataclasses import dataclass, asdict
import re
from typing import List, Optional, Dict, Any

try:
    import sympy as sp
except ImportError:
    sp = None


_SAFE_EXPR = re.compile(r"^[0-9\s\+\-\*\/\(\)\.]+$")


@dataclass
class ProofStep:
    index: int
    action: str
    detail: str
    result: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Proof:
    statement: str
    steps: List[ProofStep]
    valid: bool
    verdict: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "statement": self.statement,
            "steps": [s.to_dict() for s in self.steps],
            "valid": self.valid,
            "verdict": self.verdict,
        }


class MathCortex:
    """
    Provides basic math verification with explainable, human-readable steps.
    Supports both numeric evaluation and symbolic verification (with SymPy).
    """

    def _safe_eval(self, expr: str) -> float:
        expr = expr.strip()
        if not _SAFE_EXPR.match(expr):
            raise ValueError("Unsafe characters in expression")
        return float(eval(expr, {"__builtins__": {}}, {}))

    def _parse_equality(self, statement: str) -> Optional[tuple]:
        m = re.match(r"^\s*(.+?)\s*(?:=|==)\s*(.+?)\s*$", statement)
        if not m:
            return None
        return m.group(1), m.group(2)

    def prove_equality(self, lhs: str, rhs: str) -> Proof:
        """Proves a numeric equality with step-by-step explanation."""
        steps: List[ProofStep] = []
        idx = 1

        steps.append(ProofStep(idx, "parse", f"Left expression: {lhs}")); idx += 1
        steps.append(ProofStep(idx, "parse", f"Right expression: {rhs}")); idx += 1

        try:
            left_val = self._safe_eval(lhs)
            steps.append(ProofStep(idx, "evaluate", f"LHS = {lhs}", result=str(left_val)))
            idx += 1
        except Exception as e:
            steps.append(ProofStep(idx, "error", f"Failed to evaluate LHS: {e}"))
            return Proof(f"{lhs} = {rhs}", steps, False, "Failed to evaluate LHS")

        try:
            right_val = self._safe_eval(rhs)
            steps.append(ProofStep(idx, "evaluate", f"RHS = {rhs}", result=str(right_val)))
            idx += 1
        except Exception as e:
            steps.append(ProofStep(idx, "error", f"Failed to evaluate RHS: {e}"))
            return Proof(f"{lhs} = {rhs}", steps, False, "Failed to evaluate RHS")

        equal = abs(left_val - right_val) < 1e-9
        steps.append(ProofStep(idx, "compare", f"{left_val} vs {right_val}", result=str(equal)))
        verdict = "✓ Equality holds" if equal else "✗ Equality does not hold"
        return Proof(f"{lhs} = {rhs}", steps, equal, verdict)

    def verify(self, statement: str) -> Proof:
        """Verifies a mathematical equality statement."""
        parsed = self._parse_equality(statement)
        if not parsed:
            return Proof(statement, [ProofStep(1, "error", "Not an equality statement")], False, "Parse error")
        lhs, rhs = parsed
        return self.prove_equality(lhs, rhs)

    def symbolic_verify(self, statement: str) -> Proof:
        """Verifies equality using symbolic mathematics (requires SymPy)."""
        steps: List[ProofStep] = []
        
        if sp is None:
            steps.append(ProofStep(1, "error", "SymPy not available"))
            return Proof(statement, steps, False, "SymPy unavailable")

        parsed = self._parse_equality(statement)
        if not parsed:
            return Proof(statement, [ProofStep(1, "error", "Not an equality statement")], False, "Parse error")

        lhs_str, rhs_str = parsed
        idx = 1
        steps.append(ProofStep(idx, "parse", f"Equality: {lhs_str} = {rhs_str}")); idx += 1

        try:
            symbols = sorted(set(re.findall(r"[a-zA-Z]", statement)))
            sym_objs = sp.symbols(" ".join(symbols)) if symbols else ()
            sym_map = {str(s): s for s in (sym_objs if isinstance(sym_objs, (list, tuple)) else [sym_objs]) if s}

            lhs = sp.sympify(lhs_str, locals=sym_map)
            rhs = sp.sympify(rhs_str, locals=sym_map)
            steps.append(ProofStep(idx, "sympify", "Parsed symbolic expressions")); idx += 1

            lhs_s = sp.simplify(lhs)
            rhs_s = sp.simplify(rhs)
            steps.append(ProofStep(idx, "simplify", f"LHS → {lhs_s}")); idx += 1
            steps.append(ProofStep(idx, "simplify", f"RHS → {rhs_s}")); idx += 1

            diff = sp.simplify(lhs_s - rhs_s)
            is_zero = sp.simplify(diff) == 0
            steps.append(ProofStep(idx, "compare", f"LHS - RHS = {diff}")); idx += 1
            
            verdict = "✓ Symbolic equality holds" if is_zero else "✗ Symbolic equality does not hold"
            return Proof(f"{lhs_str} = {rhs_str}", steps, bool(is_zero), verdict)
        except Exception as e:
            steps.append(ProofStep(idx, "error", f"Symbolic verification failed: {e}"))
            return Proof(f"{lhs_str} = {rhs_str}", steps, False, "Symbolic error")


# Singleton
_math_cortex: Optional[MathCortex] = None

def get_math_cortex() -> MathCortex:
    global _math_cortex
    if _math_cortex is None:
        _math_cortex = MathCortex()
    return _math_cortex
