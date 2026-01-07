import ast
import random
import logging
from typing import Optional
from code_genome import CodeDNA

logger = logging.getLogger(__name__)

class CodeMutator(ast.NodeTransformer):
    """
    The Biological Engine of Evolution.
    Uses AST transformations to apply 'genetic mutations' to Python code.
    """
    def __init__(self, intensity: float = 0.1):
        self.intensity = intensity
        self.mutations_log = []

    def visit_BinOp(self, node):
        """
        Mutation: Swap Operator (+, -, *, /)
        """
        if random.random() < self.intensity:
            ops = [ast.Add, ast.Sub, ast.Mult, ast.Div] # , ast.FloorDiv, ast.Mod]
            # Filter out the current op type to ensure a change
            current_type = type(node.op)
            choices = [op() for op in ops if op != current_type]

            if choices:
                new_op = random.choice(choices)
                self.mutations_log.append(f"Swapped operator {current_type.__name__} -> {type(new_op).__name__}")
                return ast.copy_location(ast.BinOp(left=node.left, op=new_op, right=node.right), node)

        return self.generic_visit(node)

    def visit_Constant(self, node):
        """
        Mutation: Drift Constants (Numbers)
        """
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            if random.random() < self.intensity:
                # Mutation: Small drift or random replacement
                if random.random() < 0.5:
                    # Drift: +/- 1
                    delta = 1 if random.random() < 0.5 else -1
                    new_val = node.value + delta
                    self.mutations_log.append(f"Drifted constant {node.value} -> {new_val}")
                    return ast.copy_location(ast.Constant(value=new_val), node)
                else:
                    # Random small integer
                    new_val = random.randint(0, 10)
                    self.mutations_log.append(f"Replaced constant {node.value} -> {new_val}")
                    return ast.copy_location(ast.Constant(value=new_val), node)
        return self.generic_visit(node)

    def visit_Name(self, node):
        """
        Mutation: Variable Swapping (e.g., swap 'a' with 'b')
        NOTE: Requires context of available variables.
        For basic AST transform, we might just swap if we track scope.
        For MVP, skipping intricate variable swapping to avoid scope errors.
        """
        return self.generic_visit(node)


def evolve_code(dna: CodeDNA, mutation_rate: float = 0.2) -> CodeDNA:
    """
    Applies evolutionary pressure to the DNA.
    Returns a NEW, mutated child CodeDNA.
    """
    child = dna.clone()

    try:
        tree = ast.parse(child.source_code)
        mutator = CodeMutator(intensity=mutation_rate)
        new_tree = mutator.visit(tree)
        ast.fix_missing_locations(new_tree)

        new_source = ast.unparse(new_tree)

        # Verify syntax of the mutation
        try:
            ast.parse(new_source)
            child.source_code = new_source
            child.mutation_history.extend(mutator.mutations_log)
        except SyntaxError:
            # Failed mutation (lethal), revert to parent code but mark as failed mutation?
            # Or just return parent as-is (stagnation).
            # Let's return parent for stability.
            pass

    except Exception as e:
        logger.warning(f"Mutation failed: {e}")
        pass

    return child
