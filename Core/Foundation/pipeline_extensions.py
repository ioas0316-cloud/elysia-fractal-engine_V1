"""

Pipeline Extensions for CognitionPipeline



Adds helper functions that operate on a CognitionPipeline instance without

modifying the core pipeline code. This keeps integration minimal and safe.

"""

from __future__ import annotations



from Core.Foundation.math_cortex import MathCortex

from Project_Mirror.proof_renderer import ProofRenderer





def run_math_verification(pipeline, statement: str) -> dict:

    """

    Verifies a math equality, renders a proof image, and anchors it in KG.

    Returns a dict with validity, verdict, and image path.

    """

    math = MathCortex()

    proof = math.verify(statement)

    renderer = ProofRenderer()

    image_path = renderer.render(proof)



    try:

        pipeline.kg_manager.add_node(

            "math_proof", properties={"category": "artifact", "experience_visual": [image_path]}

        )

        pipeline.kg_manager.add_edge(

            "math_proof", statement, "verifies", properties={"experience_visual": image_path}

        )

        pipeline.kg_manager.save()

    except Exception:

        pass



    return {"valid": proof.valid, "verdict": proof.verdict, "image": image_path}



