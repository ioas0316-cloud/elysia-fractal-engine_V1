"""
Anatomy Engine (The Structural Biologist)
=========================================
"To draw the body, one must first build the body."

This module implements a Hierarchical Skeletal System using Forward Kinematics.
It replaces 2D drawing with 3D structural simulation.
"""

import math
import logging
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from pathlib import Path

logger = logging.getLogger("AnatomyEngine")
logging.basicConfig(level=logging.INFO)

@dataclass
class Bone:
    name: str
    length: float
    angle_z: float # Rotation around Z axis (2D plane for now)
    children: List['Bone'] = field(default_factory=list)
    parent: Optional['Bone'] = None
    
    # Computed State
    world_start: Tuple[float, float] = (0.0, 0.0)
    world_end: Tuple[float, float] = (0.0, 0.0)

class Skeleton:
    def __init__(self):
        self.root = None
        self.output_dir = Path("outputs/s anatomy")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_humanoid(self):
        """Constructs a basic Humanoid Rig."""
        # 1. Spine Chain
        self.root = Bone("Hip", 0, 0) # Root node
        spine1 = self.add_bone(self.root, "Spine1", length=15, angle=90) # Up
        spine2 = self.add_bone(spine1, "Spine2", length=15, angle=0)     # Up relative to parent
        neck   = self.add_bone(spine2, "Neck", length=8, angle=0)
        head   = self.add_bone(neck, "Head", length=12, angle=0)
        
        # 2. Shoulders
        l_clavicle = self.add_bone(spine2, "L_Clavicle", length=10, angle=30)
        r_clavicle = self.add_bone(spine2, "R_Clavicle", length=10, angle=-30) # Mirrored
        
        # 3. Arms
        l_upper_arm = self.add_bone(l_clavicle, "L_UpperArm", length=25, angle=60)
        l_lower_arm = self.add_bone(l_upper_arm, "L_LowerArm", length=22, angle=-20)
        l_hand      = self.add_bone(l_lower_arm, "L_Hand", length=8, angle=0)

        r_upper_arm = self.add_bone(r_clavicle, "R_UpperArm", length=25, angle=-60)
        r_lower_arm = self.add_bone(r_upper_arm, "R_LowerArm", length=22, angle=20)
        r_hand      = self.add_bone(r_lower_arm, "R_Hand", length=8, angle=0)

        # 4. Hips/Legs
        l_hip = self.add_bone(self.root, "L_Hip", length=10, angle=240)
        r_hip = self.add_bone(self.root, "R_Hip", length=10, angle=300)
        
        l_thigh = self.add_bone(l_hip, "L_Thigh", length=30, angle=-60) # Downwardsish
        l_shin  = self.add_bone(l_thigh, "L_Shin", length=30, angle=10)
        l_foot  = self.add_bone(l_shin, "L_Foot", length=10, angle=80) 

        r_thigh = self.add_bone(r_hip, "R_Thigh", length=30, angle=60)
        r_shin  = self.add_bone(r_thigh, "R_Shin", length=30, angle=-10)
        r_foot  = self.add_bone(r_shin, "R_Foot", length=10, angle=-80)

    def add_bone(self, parent: Bone, name: str, length: float, angle: float) -> Bone:
        b = Bone(name=name, length=length, angle_z=angle, parent=parent)
        parent.children.append(b)
        return b

    def update_kinematics(self, bone: Bone, start_x: float, start_y: float, parent_angle: float):
        """Recursive Forward Kinematics solver."""
        current_angle = parent_angle + bone.angle_z
        rad = math.radians(current_angle)
        
        end_x = start_x + bone.length * math.cos(rad)
        end_y = start_y + bone.length * math.sin(rad)
        
        bone.world_start = (start_x, start_y)
        bone.world_end = (end_x, end_y)
        
        for child in bone.children:
            self.update_kinematics(child, end_x, end_y, current_angle)

    def visualize(self, filename="anatomy_rig.png"):
        """Renders the skeletal data."""
        if not self.root:
            logger.error("No skeleton to visualize.")
            return

        # Solve positions
        self.update_kinematics(self.root, 0, 0, 90) # Root at (0,0), Upright orientation
        
        fig, ax = plt.subplots(figsize=(8, 12))
        ax.set_aspect('equal')
        ax.set_xlim(-60, 60)
        ax.set_ylim(-60, 100)
        ax.axis('off')
        ax.set_facecolor('#1a1a1a')
        
        def draw_bone(b):
            # Draw Bone
            ax.plot([b.world_start[0], b.world_end[0]], 
                    [b.world_start[1], b.world_end[1]], 
                    color='cyan', linewidth=2, alpha=0.8, marker='o', markersize=4, markerfacecolor='white')
            
            # Recurse
            for child in b.children:
                draw_bone(child)

        draw_bone(self.root)
        
        output_path = self.output_dir / filename
        plt.savefig(output_path, facecolor='#1a1a1a')
        plt.close(fig)
        logger.info(f"🦴 Skeletal Rig Rendered: {output_path}")
        return str(output_path)

if __name__ == "__main__":
    bio = Skeleton()
    bio.create_humanoid()
    bio.visualize()
