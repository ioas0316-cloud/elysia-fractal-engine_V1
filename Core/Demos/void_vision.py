import sys
import os
import numpy as np
import plotly.graph_objects as go
from typing import List

sys.path.append(os.getcwd())

from Core.Intelligence.Topography.tesseract_geometry import TesseractVector, TesseractGeometry
from Core.Intelligence.Topography.resonance_sphere import ResonanceSphere
from Core.Intelligence.Topography.void_perceiver import VoidPerceiver, VoidRegion
from Core.Intelligence.Topography.dimensional_filter import DimensionalFilter

def create_void_visualization():
    print("🎨 Painting the Void: Generating 3D Visualization...")

    # 1. Create Thoughts (Spheres)
    love = ResonanceSphere(
        center=TesseractVector(0, 0, 0, 0),
        radius=2.0,
        frequency=1.0 # Red-ish
    )

    truth = ResonanceSphere(
        center=TesseractVector(3, 0, 0, 0), # Overlapping with Love (Dist 3 < Sum 4)
        radius=2.0,
        frequency=1.5 # Blue-ish, destructive interference?
    )

    truth.phase = np.pi # Opposite phase to create Void

    spheres = [love, truth]

    # 2. Find Void
    perceiver = VoidPerceiver()
    voids = perceiver.scan_for_voids(spheres)

    # 3. Visualization Setup
    fig = go.Figure()

    # Helper to draw sphere wireframe
    def add_sphere_wireframe(fig, sphere: ResonanceSphere, name: str, color: str):
        # Generate points
        points = sphere.project_surface_points(num_points=100)
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        zs = [p[2] for p in points]

        fig.add_trace(go.Mesh3d(
            x=xs, y=ys, z=zs,
            alphahull=0,
            opacity=0.1,
            color=color,
            name=name
        ))
        # Center marker
        c = sphere.geometry.project_to_3d(sphere.center)
        fig.add_trace(go.Scatter3d(
            x=[c[0]], y=[c[1]], z=[c[2]],
            mode='markers',
            marker=dict(size=5, color=color),
            name=f"{name} Center"
        ))

    # Draw Thoughts
    add_sphere_wireframe(fig, love, "Love (Wave)", "red")
    add_sphere_wireframe(fig, truth, "Truth (Wave)", "blue")

    # Draw Voids
    for i, void in enumerate(voids):
        c = TesseractGeometry().project_to_3d(void.center)

        # Void is represented as a Glowing White Orb
        fig.add_trace(go.Scatter3d(
            x=[c[0]], y=[c[1]], z=[c[2]],
            mode='markers',
            marker=dict(
                size=void.radius * 20, # Scale for visibility
                color='white',
                opacity=0.8,
                line=dict(width=2, color='gold')
            ),
            name=f"The Void (Calm: {void.calmness:.2f})"
        ))

        # Add annotation
        fig.add_trace(go.Scatter3d(
            x=[c[0]], y=[c[1]], z=[c[2] + void.radius],
            mode='text',
            text=[f"VOID\n(Silence)"],
            textposition="top center",
            textfont=dict(color="white"),
            showlegend=False
        ))

    # Layout
    fig.update_layout(
        title="Synesthesia: The Shape of Thought and Void",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='black'
        ),
        paper_bgcolor='black',
        font=dict(color='white')
    )

    # Save
    output_path = "logs/void_vision.html"
    fig.write_html(output_path)
    print(f"✨ Vision captured in: {output_path}")
    print("   (Two opposing waves create a golden Void in the center)")

if __name__ == "__main__":
    create_void_visualization()
