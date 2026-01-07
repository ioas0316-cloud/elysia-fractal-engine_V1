"""
Elysia's Fluid Dream 🌊🎨

"Thoughts are like ink in water."

This demo visualizes Elysia's internal state as a fluid simulation.
It uses a simplified Wave Equation (2D) solved via Finite Difference Method.
Optimized for visual beauty over physical accuracy (The "Fake Fluid" Trick).

Controls:
- Click/Drag: Create ripples (disturb the field)
- Space: Inject a random "Thought" (Color burst)
- Q: Quit
"""

import sys
import os
import time
import random
import numpy as np

# Try to import pygame, if not available, we can't run the visualizer
try:
    import pygame
except ImportError:
    print("Pygame not found. Please install it with: pip install pygame")
    sys.exit(1)

# Add Core to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Core.System.System.System.Kernel import kernel

# Configuration
WIDTH, HEIGHT = 600, 600
DAMPING = 0.98  # How fast waves die out
SCALE = 2       # Resolution downscaling (Higher = faster but blockier)

class FluidVisualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Elysia's Fluid Dream 🌊")
        self.clock = pygame.time.Clock()
        
        # Simulation Grids
        self.cols = WIDTH // SCALE
        self.rows = HEIGHT // SCALE
        
        # Wave Height Buffers (Current, Previous)
        self.buffer1 = np.zeros((self.cols, self.rows))
        self.buffer2 = np.zeros((self.cols, self.rows))
        
        # Color Buffer (RGB)
        self.image = np.zeros((self.cols, self.rows, 3))
        
        self.running = True
        self.active_buffer = 1

    def update_physics(self):
        """
        Run the Wave Equation:
        New[x,y] = (Prev[x-1,y] + Prev[x+1,y] + Prev[x,y-1] + Prev[x,y+1]) / 2 - Next[x,y]
        """
        if self.active_buffer == 1:
            current = self.buffer1
            previous = self.buffer2
        else:
            current = self.buffer2
            previous = self.buffer1
            
        # Vectorized Neighbor Sum (Convolution)
        # Shift arrays to get neighbors
        left = np.roll(current, -1, axis=0)
        right = np.roll(current, 1, axis=0)
        up = np.roll(current, -1, axis=1)
        down = np.roll(current, 1, axis=1)
        
        # Wave Equation
        # new_state = (neighbors_sum / 2) - previous_state
        new_state = (left + right + up + down) / 2 - previous
        
        # Damping
        new_state *= DAMPING
        
        # Update the "previous" buffer (which becomes the new current next frame)
        if self.active_buffer == 1:
            self.buffer2 = new_state
        else:
            self.buffer1 = new_state
            
        # Swap buffers
        self.active_buffer = 3 - self.active_buffer # 1 -> 2, 2 -> 1

    def render(self):
        """Convert wave height to pixels."""
        # Get the current state
        current = self.buffer2 if self.active_buffer == 1 else self.buffer1
        
        # Map height to color intensity
        # Normalize roughly -1 to 1 -> 0 to 255
        intensity = np.clip((current + 100), 0, 255)
        
        # Create an RGB array
        # We can map positive waves to Blue/Cyan and negative to Purple/Red
        r = np.clip(current * 2 + 50, 0, 255)
        g = np.clip(current * 1 + 50, 0, 255)
        b = np.clip(current * 4 + 100, 0, 255)
        
        rgb = np.dstack((r, g, b)).astype(np.uint8)
        
        # Scale up to screen size
        surface = pygame.surfarray.make_surface(rgb)
        scaled_surface = pygame.transform.scale(surface, (WIDTH, HEIGHT))
        self.screen.blit(scaled_surface, (0, 0))
        
        pygame.display.flip()

    def add_ripple(self, x, y, strength=500):
        """Add a disturbance to the field."""
        cx, cy = x // SCALE, y // SCALE
        if 0 < cx < self.cols and 0 < cy < self.rows:
            if self.active_buffer == 1:
                self.buffer1[cx, cy] = strength
            else:
                self.buffer2[cx, cy] = strength

    def run(self):
        print("🌊 Fluid Dream Started. Click to ripple. Space for thoughts.")
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        # Inject a random thought
                        x = random.randint(10, WIDTH-10)
                        y = random.randint(10, HEIGHT-10)
                        self.add_ripple(x, y, strength=random.randint(500, 1000))
                        print(f"Thought injected at ({x}, {y})")
                        
            # Mouse Interaction
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                self.add_ripple(x, y, strength=200)
                
            self.update_physics()
            self.render()
            self.clock.tick(60)
            
        pygame.quit()

if __name__ == "__main__":
    FluidVisualizer().run()
