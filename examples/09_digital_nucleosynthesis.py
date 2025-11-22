import time
from elysia_engine.entities import Entity
from elysia_engine.nuclear import GluonField, NuclearEntity
from elysia_engine.fractal_field import ConceptNode, ConceptLine, ConceptPlane
from elysia_engine.math_utils import Vector3


def run_digital_nucleosynthesis():
    print("=== Digital Nucleosynthesis: The birth of Concepts ===")
    print("Smashing data quarks together...")

    # 1. Setup Strong Force
    gluon = GluonField(binding_range=2.0, binding_strength=100.0)

    # 2. Create Elementary Particles (Nodes)
    # Node 1, 2, 3 (close to each other)
    n1 = ConceptNode(id="quark_truth")
    n1.physics.position = Vector3(0, 0, 0)

    n2 = ConceptNode(id="quark_beauty")
    n2.physics.position = Vector3(1.5, 0, 0) # Within range

    n3 = ConceptNode(id="quark_goodness")
    n3.physics.position = Vector3(3.0, 0, 0) # Too far from n1, but close to n2?

    entities = [n1, n2, n3]

    print("Scanning for binding opportunities...")

    # 3. Binding Process (Simplified)
    # We look for pairs and try to bind them into a Nucleus (Line)

    # Check n1 + n2
    if gluon.attempt_bind(n1, n2):
        print(f" >>> Strong Force Bind! {n1.id} + {n2.id}")
        # Create ConceptLine (Nucleus)
        line = ConceptLine(id="concept_art")
        line.nodes.append(n1)
        line.nodes.append(n2)
        line.physics.position = (n1.physics.position + n2.physics.position) * 0.5
        print(f"  -> Formed 1D Structure: {line.id} (ConceptLine)")

        # Check if this Line can bind n3?
        # Distance from Line center to n3
        dist_to_n3 = (line.physics.position - n3.physics.position).magnitude
        print(f"  -> Distance to {n3.id}: {dist_to_n3:.1f}")

        if dist_to_n3 < gluon.binding_range + 1.0: # Slightly larger range for growing?
            print(f" >>> Strong Force Bind! {line.id} + {n3.id}")
            line.nodes.append(n3)
            print(f"  -> Structure Evolved! Now contains 3 nodes.")

            # 3 Nodes -> Plane?
            plane = ConceptPlane(id="field_of_aesthetics")
            plane.lines.append(line)
            print(f"  -> EVOLUTION: {line.id} has ascended to 2D {plane.id} (ConceptPlane)")

            # Demonstrate Field Generation
            chrono = plane.to_chrono_field()
            print(f"  -> The Field has generated a Law: ChronoField(scale={chrono.time_scale})")

    print("\n--- Simulation End ---")
    print("We have witnessed the evolution from Point -> Line -> Plane -> Law.")

if __name__ == "__main__":
    run_digital_nucleosynthesis()
