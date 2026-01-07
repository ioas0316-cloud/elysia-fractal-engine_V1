import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
import os
import sys

# Ensure the Core directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.System.System.System.Kernel import kernel
from Core.Intelligence.Intelligence.Consciousness.wave import WaveInput

# --- Visualization Parameters ---
OUTPUT_DIR = "aurora_frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)
FRAME_DELAY = 0.1  # seconds between frames
SIMULATION_DURATION = 5  # seconds
STEPS_PER_FRAME = 2

def main():
    """
    Main function to run the Aurora visualization.
    """
    print("--- 🌌 Initializing Aurora Viewer ---")
    print(f"This will simulate the consciousness field for {SIMULATION_DURATION} seconds.")

    # Get the resonance engine from the kernel
    resonance_engine = kernel.resonance_engine

    # 1. Inject an initial thought to start the Aurora
    print("\n[1] Injecting initial thought wave: '사랑과 빛'...")
    initial_wave = WaveInput(source_text="사랑과 빛", intensity=2.0)

    # Calculate the initial resonance and immediately apply it as energy
    initial_pattern = resonance_engine.calculate_global_resonance(initial_wave)
    for node_id, resonance_score in initial_pattern.items():
        qubit = resonance_engine.nodes.get(node_id)
        if qubit:
            # Boost the amplitude based on resonance
            qubit.state.adjust_amplitude(resonance_score * 0.5)

    # 2. Set up the 3D plot
    fig = plt.figure(figsize=(12, 12), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    ax.grid(False)
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.xaxis.line.set_color("gray")
    ax.yaxis.line.set_color("gray")
    ax.zaxis.line.set_color("gray")

    # Set plot limits
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel("X (Body)", color='white')
    ax.set_ylabel("Y (Mind)", color='white')
    ax.set_zlabel("Z (Soul)", color='white')

    # 3. Simulation and Rendering Loop
    total_steps = int(SIMULATION_DURATION / (FRAME_DELAY * STEPS_PER_FRAME))
    print(f"\n[2] Starting simulation loop for {total_steps} frames...")

    for i in range(total_steps):
        start_time = time.time()

        # --- Run simulation steps ---
        for _ in range(STEPS_PER_FRAME):
            kernel.tick() # This now also calls resonance_engine.step()

        # --- Prepare data for plotting ---
        positions = []
        amplitudes = []
        colors = []

        # Use a colormap to map 'w' (dimension) to color
        # 0 (Point) -> Blue, 1 (Line) -> Green, 2 (Space) -> Yellow, 3 (God) -> Red
        cmap = plt.get_cmap('viridis')

        for qubit in resonance_engine.nodes.values():
            pos = [qubit.state.x, qubit.state.y, qubit.state.z]

            # Normalize position to be within [-1, 1] cube if not already
            norm = np.linalg.norm(pos)
            if norm > 1:
                pos = [p / norm for p in pos]

            positions.append(pos)

            amp = qubit.state.total_amplitude()
            amplitudes.append(amp)

            # Map w (dimensional scale) to color. w ranges from 0 to 3+
            color_val = min(qubit.state.w / 3.0, 1.0)
            colors.append(cmap(color_val))

        # --- Update the plot ---
        ax.clear()
        ax.set_facecolor('black')
        ax.grid(False)
        ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
        ax.set_xlim([-1, 1]); ax.set_ylim([-1, 1]); ax.set_zlim([-1, 1])
        ax.set_xlabel("X", color='white'); ax.set_ylabel("Y", color='white'); ax.set_zlabel("Z", color='white')

        if positions:
            positions = np.array(positions)
            # Size is proportional to amplitude, with a minimum size
            sizes = (np.array(amplitudes) * 200) + 10

            scatter = ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2],
                                 c=colors, s=sizes, alpha=0.8, edgecolors='w', linewidth=0.5)

        # Add a title to the plot
        current_time = i * FRAME_DELAY * STEPS_PER_FRAME
        ax.set_title(f"Aurora of Consciousness\nTime: {current_time:.2f}s", color='white', fontsize=16)

        # Save the frame
        frame_path = os.path.join(OUTPUT_DIR, f"frame_{i:04d}.png")
        plt.savefig(frame_path, dpi=100, bbox_inches='tight', facecolor='black')

        # --- Print progress and sleep ---
        elapsed = time.time() - start_time
        print(f"Rendered frame {i+1}/{total_steps} to {frame_path} (took {elapsed:.2f}s)")

        sleep_time = max(0, FRAME_DELAY - elapsed)
        time.sleep(sleep_time)

    print("\n[3] Aurora simulation complete.")
    print(f"Frames saved in: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
