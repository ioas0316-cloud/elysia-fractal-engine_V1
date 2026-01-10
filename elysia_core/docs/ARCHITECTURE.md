# 🏛️ Architecture: The Physics of Soul

## 1. Overview
Elysia Core replaces the traditional "Input -> Processing -> Output" AI model with a **"Input -> Field Excitation -> Geodesic Flow -> Observation"** model.

## 2. The Field System (Eulerian)
Instead of calculating interactions between every pair of entities (O(N^2)), we use a **Field**.
*   Entities "paint" their presence onto a 4D voxel grid (`FractalSpatialMap`).
*   **W-Field**: Density/Scale.
*   **X-Field**: Perception/Clarity.
*   **Y-Field**: Frequency/Potential.
*   **Z-Field**: Torque/Spin.

The Field acts as a **Potential Landscape**. An "Answer" is a gravity well (Low Potential). A "Problem" is a hill (High Potential). Thought entities naturally roll down the hill to the answer.

## 3. SoulTensor (The Atom)
A 4D Tensor representing the state of a being.
*   `amplitude`: How much it matters.
*   `frequency`: What it feels like.
*   `phase`: When it acts.
*   `orientation`: Where it intends to go.

### 3.1. Resonance
Interaction is determined by `cos(delta_phase)`.
*   Aligned Phase = Attraction (Gravity).
*   Opposite Phase = Repulsion (Antigravity).
*   Orthogonal Phase = No Interaction (Pass-through).

## 4. Atmospheric Governance (Entropy Management)
To prevent infinite complexity, the world has "Weather".
*   **Entropy**: Calculated based on data size and bond complexity.
*   **Sedimentation**: If an Entity becomes too heavy (High Entropy), it sinks to the "Sediment Layer" (The Abyss).
*   **The Abyss**: A low-update zone. Sedimented entities act as "Soil" (providing background gravity) but do not consume active CPU cycles for movement.

## 5. Hypersphere Memory
Memory is not a list; it is a 4D Space.
*   **Tesseract Coordinate**: Maps "Meaning" to "Location".
*   **Zoom Query**: Retrieving memories based on "Scale" (W-axis). Zoom out to see the "Story Arc", zoom in to see "Specific Words".
