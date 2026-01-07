import ast
import sys
import time
import traceback
from typing import Any, Dict, Tuple
from dataclasses import dataclass
import multiprocessing
import logging

# Import our Genome types
from code_genome import CodeDNA, CodeChallenge

logger = logging.getLogger(__name__)

@dataclass
class TrialResult:
    success: bool
    output: Any = None
    error: str = ""
    execution_time: float = 0.0
    resonance_score: float = 0.0 # Accuracy/Alignment
    entropy_cost: float = 0.0 # Error penalty

class ElysiaForge:
    """
    The Blacksmith of Logic.
    Safely executes CodeDNA against CodeChallenges to determine fitness.
    Acts as the 'Physics Engine' for code execution.
    """

    def __init__(self):
        self.allowed_globals = {
            "range": range,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "set": set,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "round": round,
            "sorted": sorted,
            "map": map,
            "filter": filter,
            "enumerate": enumerate,
            "zip": zip,
            # Math constants if needed?
        }

    def run_trial(self, dna: CodeDNA, challenge: CodeChallenge) -> TrialResult:
        """
        Runs a single evolutionary trial.
        Biology Metaphor: The organism (DNA) attempts to survive the environment (Challenge).
        """

        # 1. Structural Integrity Check (Syntax)
        if not dna.is_valid_syntax():
            return TrialResult(
                success=False,
                error="Structural Failure (SyntaxError)",
                entropy_cost=50.0 # Heavy penalty for broken DNA
            )

        total_resonance = 0.0
        total_entropy = 0.0
        max_time = 0.0

        # 2. Compiling the organism (AST -> Bytecode)
        try:
            # Compile the function definition
            compiled_code = compile(dna.source_code, filename="<dna>", mode="exec")

            # Prepare the sandbox namespace
            sandbox = self.allowed_globals.copy()

            # Execute the definition to bind the function name in the sandbox
            exec(compiled_code, sandbox)

            func = sandbox.get(dna.function_name)
            if not callable(func):
                return TrialResult(success=False, error=f"Function '{dna.function_name}' not found.", entropy_cost=20.0)

        except Exception as e:
            return TrialResult(success=False, error=f"Gestation Failure (Compile Error): {e}", entropy_cost=30.0)

        # 3. The Trial (Running Test Cases)
        passed_tests = 0
        total_tests = len(challenge.test_cases)

        for case in challenge.test_cases:
            inputs = case['inputs']
            expected = case['expected']

            start_time = time.perf_counter()
            try:
                # --- Execution ---
                # NOTE: For a true robust sandbox, this should be in a separate process or restrictive environment.
                # For now, we rely on restricted globals and timeouts.
                # Basic timeout protection via simple checking logic isn't perfect but sufficient for "3GB Mode" experiments.

                result = func(**inputs)

                execution_time = time.perf_counter() - start_time
                max_time = max(max_time, execution_time)

                if execution_time > challenge.timeout_seconds:
                    total_entropy += 10.0
                    logger.debug(f"Trial timeout for {dna.id}")
                    # Treat as failure
                    pass

                # --- Verification ---
                if result == expected:
                    passed_tests += 1
                    total_resonance += 10.0 # Resonance reward
                else:
                    # Gentle entropy for wrong answers (learning opportunity)
                    total_entropy += 2.0
                    # Partial credit? For now, binary.

            except Exception as e:
                total_entropy += 5.0 # Runtime error cost
                # error_msg = str(e)

        # 4. Final Judgment
        accuracy = passed_tests / total_tests if total_tests > 0 else 0.0

        # Success = Passed all tests
        success = (passed_tests == total_tests)

        # Physics calculation
        # Energy cost increases with execution time (Efficiency pressure)
        energy_penalty = max_time * 100.0
        final_resonance = total_resonance - energy_penalty

        return TrialResult(
            success=success,
            resonance_score=final_resonance,
            entropy_cost=total_entropy,
            execution_time=max_time,
            output=f"Passed {passed_tests}/{total_tests}"
        )
