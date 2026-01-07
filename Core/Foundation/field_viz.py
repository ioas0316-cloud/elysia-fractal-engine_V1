"""
Field Visualization
===================
Visualizes Elysia's thought field in 3D.
Shows concepts as wave patterns and interference.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from typing import List, Tuple

from Project_Elysia.mechanics.advanced_field import AdvancedField

class FieldVisualizer:
    """Visualizes field dynamics in 2D/3D."""
    
    def __init__(self, field: AdvancedField):
        self.field = field
        
    def plot_2d_slice(self, axis='z', position=None, title="Field Slice"):
        """
        Plots a 2D slice of the 3D field.
        
        Args:
            axis: 'x', 'y', or 'z'
            position: Position along axis (default: middle)
            title: Plot title
        """
        slice_data = self.field.get_slice(axis, position)
        
        plt.figure(figsize=(10, 8))
        plt.imshow(slice_data, cmap='RdBu_r', interpolation='bilinear')
        plt.colorbar(label='Field Intensity')
        plt.title(title)
        plt.xlabel('X' if axis != 'x' else 'Y')
        plt.ylabel('Y' if axis != 'y' else 'Z')
        plt.tight_layout()
        plt.savefig(f'field_slice_{axis}.png', dpi=150)
        print(f"   💾 Saved: field_slice_{axis}.png")
        plt.close()
    
    def plot_3d_surface(self, title="Field 3D Surface"):
        """
        Plots 3D surface of field (using XY plane, averaged over Z).
        """
        # Average over Z axis for visualization
        field_2d = np.mean(self.field.field, axis=2)
        
        # Create meshgrid
        x = np.arange(self.field.resolution)
        y = np.arange(self.field.resolution)
        X, Y = np.meshgrid(x, y)
        
        # Plot
        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection='3d')
        
        surf = ax.plot_surface(X, Y, field_2d, cmap='viridis',
                              linewidth=0, antialiased=True, alpha=0.8)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Field Intensity')
        ax.set_title(title)
        
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        plt.tight_layout()
        plt.savefig('field_3d_surface.png', dpi=150)
        print(f"   💾 Saved: field_3d_surface.png")
        plt.close()
    
    def plot_interference_pattern(self, concepts: List[str], title="Interference Pattern"):
        """
        Visualizes interference pattern when multiple concepts activate.
        """
        # Reset and activate concepts
        self.field.reset()
        for concept in concepts:
            if concept in self.field.concept_registry:
                self.field.activate_with_harmonics(concept, intensity=1.0, depth=1.0)
        
        # Get slice
        slice_data = self.field.get_slice('z', self.field.resolution // 2)
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Heatmap
        im1 = ax1.imshow(slice_data, cmap='RdBu_r', interpolation='bilinear')
        ax1.set_title(f'{title} (Heatmap)')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        plt.colorbar(im1, ax=ax1)
        
        # Contour plot
        levels = np.linspace(slice_data.min(), slice_data.max(), 15)
        contour = ax2.contour(slice_data, levels=levels, cmap='RdBu_r')
        ax2.clabel(contour, inline=True, fontsize=8)
        ax2.set_title(f'{title} (Contours)')
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        
        # Add concept labels
        concept_str = ' + '.join(concepts)
        fig.suptitle(f'Concepts: {concept_str}', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        filename = f'interference_{"_".join(concepts)}.png'
        plt.savefig(filename, dpi=150)
        print(f"   💾 Saved: {filename}")
        plt.close()
    
    def plot_wave_evolution(self, concept: str, steps: int = 5):
        """
        Shows how a concept's wave evolves over time.
        Creates a sequence of plots.
        """
        fig, axes = plt.subplots(1, steps, figsize=(20, 4))
        
        for i, ax in enumerate(axes):
            self.field.reset()
            
            # Activate concept multiple times to simulate time
            for _ in range(i + 1):
                self.field.activate_with_harmonics(concept, intensity=1.0, depth=1.0)
            
            # Get slice
            slice_data = self.field.get_slice('z', self.field.resolution // 2)
            
            # Plot
            im = ax.imshow(slice_data, cmap='twilight', interpolation='bilinear',
                          vmin=-1, vmax=1)
            ax.set_title(f't={i}')
            ax.axis('off')
        
        fig.suptitle(f'Wave Evolution: {concept}', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(f'wave_evolution_{concept}.png', dpi=150)
        print(f"   💾 Saved: wave_evolution_{concept}.png")
        plt.close()
    
    def create_summary_visualization(self, concepts: List[str]):
        """
        Creates a comprehensive visualization showing multiple aspects.
        """
        fig = plt.figure(figsize=(16, 12))
        
        # Activate concepts
        self.field.reset()
        for concept in concepts:
            if concept in self.field.concept_registry:
                self.field.activate_with_harmonics(concept, intensity=1.0, depth=1.0)
        
        # 1. XY plane (top view)
        ax1 = plt.subplot(2, 2, 1)
        slice_xy = self.field.get_slice('z', self.field.resolution // 2)
        im1 = ax1.imshow(slice_xy, cmap='RdBu_r', interpolation='bilinear')
        ax1.set_title('XY Plane (Top View)')
        plt.colorbar(im1, ax=ax1)
        
        # 2. XZ plane (side view)
        ax2 = plt.subplot(2, 2, 2)
        slice_xz = self.field.get_slice('y', self.field.resolution // 2)
        im2 = ax2.imshow(slice_xz, cmap='RdBu_r', interpolation='bilinear')
        ax2.set_title('XZ Plane (Side View)')
        plt.colorbar(im2, ax=ax2)
        
        # 3. 3D wireframe
        ax3 = plt.subplot(2, 2, 3, projection='3d')
        field_2d = np.mean(self.field.field, axis=2)
        x = np.arange(self.field.resolution)
        y = np.arange(self.field.resolution)
        X, Y = np.meshgrid(x, y)
        ax3.plot_wireframe(X, Y, field_2d, rstride=2, cstride=2, alpha=0.6)
        ax3.set_title('3D Wireframe')
        
        # 4. Histogram
        ax4 = plt.subplot(2, 2, 4)
        ax4.hist(self.field.field.flatten(), bins=50, color='purple', alpha=0.7)
        ax4.set_title('Field Intensity Distribution')
        ax4.set_xlabel('Intensity')
        ax4.set_ylabel('Frequency')
        ax4.grid(alpha=0.3)
        
        concept_str = ' + '.join(concepts)
        fig.suptitle(f'Field Analysis: {concept_str}', fontsize=16, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('field_summary.png', dpi=150)
        print(f"   💾 Saved: field_summary.png")
        plt.close()
