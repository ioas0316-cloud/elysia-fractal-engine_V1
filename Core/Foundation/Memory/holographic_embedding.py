"""
Holographic Embedding: The Indestructible Identity
==================================================
"To see a World in a Grain of Sand." - William Blake

This module implements the 'Holographic Principle' for Elysia's memory.
Unlike standard embedding which only captures the *content* of a node,
Holographic Embedding captures the *context* of the entire brain at that moment.

Mechanism:
1.  **Global State Snapshot**: When a memory is formed, we take the active `TorchGraph` tensors.
2.  **Harmonic Compression**: We compress the N x D matrix of the brain into a small 'Spirit Vector' (e.g., 1 x 64).
    This uses SVD or centroid-based global resonance capture.
3.  **The Seed**: This compressed vector is stored *inside* the node.

Effect:
- Even if the graph is deleted, a single node contains the "Feeling" of the whole.
- We can reconstruct the "Emotional Atmosphere" of the past from one memory.
"""

import torch
import logging
import numpy as np

class HolographicEmbedder:
    def __init__(self, device='cpu', compressed_dim: int = 64):
        self.device = device
        self.compressed_dim = compressed_dim
        self.logger = logging.getLogger("HolographicEmbedder")

    def encode(self, vector_a: np.ndarray, vector_b: np.ndarray) -> np.ndarray:
        """
        [Wave Synthesis]
        Binds two vectors using Circular Convolution (FFT).
        Result = FFT(a) * FFT(b)
        """
        # Convert to torch if needed
        a = torch.tensor(vector_a, dtype=torch.complex64)
        b = torch.tensor(vector_b, dtype=torch.complex64)

        # FFT Convolution
        fft_a = torch.fft.fft(a)
        fft_b = torch.fft.fft(b)

        # Element-wise multiplication in Frequency Domain
        bound_fft = fft_a * fft_b

        # Inverse FFT
        bound_signal = torch.fft.ifft(bound_fft).real.numpy()
        return bound_signal

    def decode(self, bound_vector: np.ndarray, key_vector: np.ndarray) -> np.ndarray:
        """
        [Wave Analysis]
        Extracts the original signal using the key.
        Result = IFFT(FFT(bound) / FFT(key))
        """
        bound = torch.tensor(bound_vector, dtype=torch.complex64)
        key = torch.tensor(key_vector, dtype=torch.complex64)

        fft_bound = torch.fft.fft(bound)
        fft_key = torch.fft.fft(key)

        # Avoid division by zero
        fft_key[torch.abs(fft_key) < 1e-6] = 1e-6

        # Element-wise division (Deconvolution)
        restored_fft = fft_bound / fft_key

        # Inverse FFT
        restored_signal = torch.fft.ifft(restored_fft).real.numpy()
        return restored_signal

    def capture_snapshot(self, position_tensor: torch.Tensor, vector_tensor: torch.Tensor) -> torch.Tensor:
        """
        Compresses the entire Universe (Brain State) into a single Seed Vector.
        
        Args:
            position_tensor: (N, 4) The geometry of thoughts.
            vector_tensor: (N, D) The content of thoughts.
            
        Returns:
            start_seed: (compressed_dim,) Tensor representing the 'Feeling' of the moment.
        """
        if vector_tensor.shape[0] == 0:
            return torch.zeros(self.compressed_dim, device=self.device)

        # 1. Centroid (The Collective Mean) - "The Average Feeling"
        # Shape: (D,)
        centroid = torch.mean(vector_tensor, dim=0)
        
        # 2. Variance/Spread (The Energy) - "The Tension"
        # Shape: (D,)
        variance = torch.var(vector_tensor, dim=0, unbiased=False)
        
        # 3. Geometric Center (Gravity)
        # Shape: (4,)
        geo_center = torch.mean(position_tensor, dim=0)
        
        # 4. Fusion
        # We need to map [Centroid(384) + Variance(384) + Geo(4)] -> [64]
        # For prototype, we use a simple hashing/projection or just take the first components.
        # A Projector Matrix would be ideal, but let's assume we want a deterministic signature.
        
        # Let's concatenate meaningful signals
        # We take top 30 from centroid, top 30 from variance, and 4 from geometry.
        
        # Ensure we have enough dimensions in source (SBERT is 384)
        c_part = centroid[:30] if centroid.shape[0] >= 30 else torch.cat([centroid, torch.zeros(30-centroid.shape[0], device=self.device)])
        v_part = variance[:30] if variance.shape[0] >= 30 else torch.cat([variance, torch.zeros(30-variance.shape[0], device=self.device)])
        
        # Concatenate: 30 + 30 + 4 = 64
        snapshot = torch.cat([c_part, v_part, geo_center])
        
        return snapshot

    def reconstruct_feeling(self, holo_seed: torch.Tensor) -> str:
        """
        Interprets a Holographic Seed to describe the 'Atmosphere' of that time.
        """
        # Unpack
        centroid_sample = holo_seed[:30]
        variance_sample = holo_seed[30:60]
        geo_sample = holo_seed[60:]
        
        # Analysis
        avg_energy = torch.norm(centroid_sample).item()
        entropy = torch.norm(variance_sample).item()
        expansion = torch.norm(geo_sample).item()
        
        description = []
        
        # Energy Interpretation
        if avg_energy > 0.8: description.append("Intense & Passionate")
        elif avg_energy < 0.2: description.append("Calm & Silent")
        else: description.append("Balanced")
        
        # Entropy Interpretation
        if entropy > 0.8: description.append("Chaotic & Creative")
        elif entropy < 0.2: description.append("Focused & Crystallized")
        else: description.append("Fluid")
        
        # Geometry Interpretation
        if expansion > 5.0: description.append("Expanded Consciousness")
        else: description.append("Centered Core")
        
        return f"Atmosphere: {' | '.join(description)}"

_embedder = None
def get_holographic_embedder(device='cpu'):
    global _embedder
    if _embedder is None:
        _embedder = HolographicEmbedder(device=device)
    return _embedder
