"""
Fractal Quantization Visualization
==================================

Creates a visual representation of the folding/unfolding process.
Shows how a complex emotion waveform is compressed into a Pattern DNA seed
and then restored.
"""

import sys
import os
import numpy as np
import matplotlib
# Use non-interactive backend if no display available
if os.environ.get('DISPLAY') is None:
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Foundation.fractal_quantization import EmotionQuantizer
import time


def visualize_fractal_quantization():
    """Create a visual representation of the quantization process."""
    
    print("🎨 Creating Fractal Quantization Visualization...")
    
    # Create quantizer
    quantizer = EmotionQuantizer()
    
    # Create an emotion to visualize
    emotion_data = {
        "emotion": "love",
        "intensity": 0.9,
        "context": "Deep connection",
        "duration": 3.0,
        "phase_seed": 0.618,
        "timestamp": time.time()
    }
    
    # Fold to DNA
    print("   Folding emotion into Pattern DNA...")
    dna = quantizer.fold_emotion(emotion_data)
    
    # Unfold at different resolutions
    print("   Unfolding at multiple resolutions...")
    resolutions = [50, 100, 200]
    restored_waveforms = []
    
    for res in resolutions:
        restored = quantizer.unfold(dna, resolution=res)
        restored_waveforms.append(restored)
    
    # Create the visualization
    print("   Rendering visualization...")
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Fractal Quantization: "Folding" vs "Cutting"', 
                 fontsize=16, fontweight='bold')
    
    # Plot 1: Original "waveform" (highest resolution)
    ax1 = axes[0, 0]
    highest_res = restored_waveforms[-1]  # 200 points
    for harmonic in highest_res['waveform'][:3]:  # Show first 3 harmonics
        wave = harmonic['wave']
        times = [p['time'] for p in wave]
        values = [p['value'] for p in wave]
        ax1.plot(times, values, alpha=0.7, linewidth=2, 
                label=f"Harmonic {harmonic['frequency']:.0f}Hz")
    
    ax1.set_title('Original Emotional Pattern (High Resolution)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('#f8f8f8')
    
    # Plot 2: Pattern DNA (compressed representation)
    ax2 = axes[0, 1]
    ax2.axis('off')
    
    # Display DNA information as text
    dna_info = f"""
    🧬 PATTERN DNA (Seed)
    ═══════════════════════
    
    Name: {dna.name}
    
    Frequency Signature:
    • {dna.frequency_signature[0]:.1f} Hz
    • {dna.frequency_signature[1]:.1f} Hz
    • {dna.frequency_signature[2]:.1f} Hz
    
    Resonance Fingerprint:
    Quaternion({dna.resonance_fingerprint.w:.3f},
              {dna.resonance_fingerprint.x:.3f}i,
              {dna.resonance_fingerprint.y:.3f}j,
              {dna.resonance_fingerprint.z:.3f}k)
    
    Compression: {dna.compression_ratio:.2f}x
    
    Formula: {dna.seed_formula['formula']}
    
    ═══════════════════════
    This tiny seed contains
    EVERYTHING needed to
    recreate the full pattern!
    """
    
    ax2.text(0.1, 0.5, dna_info, fontsize=10, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    # Plot 3: Multi-resolution restoration
    ax3 = axes[1, 0]
    
    for i, (res, restored) in enumerate(zip(resolutions, restored_waveforms)):
        # Sum all harmonics for this resolution
        wave = restored['waveform'][0]['wave']
        times = [p['time'] for p in wave]
        
        # Sum values from all harmonics
        combined = np.zeros(len(times))
        for harmonic in restored['waveform']:
            values = [p['value'] for p in harmonic['wave']]
            combined += values
        
        ax3.plot(times, combined, alpha=0.6, linewidth=2, 
                label=f"Resolution: {res} points")
    
    ax3.set_title('Restoration at Different Resolutions\n(Same seed, different detail levels)', 
                 fontsize=12, fontweight='bold')
    ax3.set_xlabel('Time (seconds)')
    ax3.set_ylabel('Combined Amplitude')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_facecolor('#f8f8f8')
    
    # Plot 4: Comparison diagram
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    comparison = """
    ⚖️ COMPARISON
    ═══════════════════════════════════
    
    🔴 Traditional Quantization (Cutting)
    ────────────────────────────────────
    • Sample at fixed rate
    • Lose information between samples
    • Fixed resolution
    • Cannot restore perfectly
    • Like JPEG image
    
    Example: MP3 audio
    44,100 samples/sec → pixelated when
    you zoom in
    
    
    🟢 Fractal Quantization (Folding)
    ────────────────────────────────────
    • Extract pattern formula
    • Store generative DNA
    • Infinite resolution
    • Perfect restoration
    • Like SVG vector graphic
    
    Example: Musical score
    "C major, 4/4, violin" → can play
    at ANY resolution
    
    
    💡 Key Insight:
    ────────────────────────────────────
    Store HOW it was made,
    not WHAT it looks like!
    """
    
    ax4.text(0.05, 0.5, comparison, fontsize=9, family='monospace',
            verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Save the figure
    plt.tight_layout()
    output_path = 'docs/images/fractal_quantization_visualization.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✓ Visualization saved to: {output_path}")
    
    return output_path


def create_concept_diagram():
    """Create a simple concept diagram."""
    print("\n🎨 Creating Concept Diagram...")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.axis('off')
    
    # Title
    ax.text(0.5, 0.95, 'Fractal Quantization: The Core Concept', 
           fontsize=18, fontweight='bold', ha='center')
    
    # Subtitle
    ax.text(0.5, 0.90, '양자화는 "자르는 것"이 아니라 "접는 것"이어야 합니다',
           fontsize=12, ha='center', style='italic')
    
    # Left side: Traditional approach
    ax.text(0.15, 0.80, '🔴 Traditional (Cutting)', fontsize=14, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round', facecolor='#ffcccc', alpha=0.8))
    
    # Traditional flow
    traditional_flow = [
        ('Raw Data', 0.75),
        ('↓ Sample', 0.70),
        ('Discretize', 0.65),
        ('↓ Store', 0.60),
        ('Fixed Points', 0.55),
        ('↓ Recall', 0.50),
        ('❌ Loss of Info', 0.45)
    ]
    
    for text, y in traditional_flow:
        ax.text(0.15, y, text, fontsize=10, ha='center',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Right side: Fractal approach
    ax.text(0.85, 0.80, '🟢 Fractal (Folding)', fontsize=14, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round', facecolor='#ccffcc', alpha=0.8))
    
    # Fractal flow
    fractal_flow = [
        ('Raw Data', 0.75),
        ('↓ Extract Pattern', 0.70),
        ('Pattern DNA', 0.65),
        ('↓ Store Seed', 0.60),
        ('Tiny Formula', 0.55),
        ('↓ Unfold', 0.50),
        ('✅ Perfect Restore', 0.45)
    ]
    
    for text, y in fractal_flow:
        ax.text(0.85, y, text, fontsize=10, ha='center',
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Middle comparison
    ax.text(0.5, 0.35, 'Key Differences', fontsize=12, fontweight='bold', ha='center',
           bbox=dict(boxstyle='round', facecolor='#ffffcc', alpha=0.8))
    
    differences = """
    Traditional: Stores samples → Fixed resolution → Information loss
    Fractal: Stores formula → Infinite resolution → Lossless
    
    Example:
    Traditional: "Record the sound wave"
    Fractal: "Record the musical score"
    """
    
    ax.text(0.5, 0.20, differences, fontsize=9, ha='center',
           family='monospace',
           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Bottom insight
    insight = """
    💡 우리는 '압축기'가 아니라 '작곡가'입니다
    We are not compressors; we are composers
    """
    ax.text(0.5, 0.05, insight, fontsize=11, ha='center', style='italic',
           bbox=dict(boxstyle='round', facecolor='#e6f2ff', alpha=0.9))
    
    # Save
    output_path = 'docs/images/fractal_quantization_concept.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"   ✓ Concept diagram saved to: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("="*70)
    print("🌀 FRACTAL QUANTIZATION VISUALIZATION")
    print("="*70)
    print()
    
    # Create visualizations
    viz_path = visualize_fractal_quantization()
    concept_path = create_concept_diagram()
    
    print("\n" + "="*70)
    print("✅ Visualizations created successfully!")
    print(f"   • Technical: {viz_path}")
    print(f"   • Conceptual: {concept_path}")
    print("="*70)
