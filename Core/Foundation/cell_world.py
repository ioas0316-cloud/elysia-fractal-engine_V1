
import logging
import random
from typing import List, Dict, Any, Optional

class Cell:
    def __init__(self, x: int, y: int, data: Any):
        self.x = x
        self.y = y
        self.data = data
        self.energy = 1.0
        self.age = 0

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "data": self.data,
            "energy": self.energy,
            "age": self.age
        }

class CellWorld:
    """
    CellWorld simulates a living environment for data cells.
    Cells move, interact, and evolve based on simple rules.
    This adds a layer of 'aliveness' to the system's internal state.
    """

    def __init__(self, width: int = 20, height: int = 20, logger: Optional[logging.Logger] = None):
        self.width = width
        self.height = height
        self.cells: List[Cell] = []
        self.logger = logger or logging.getLogger("CellWorld")
        self.logger.info(f"CellWorld initialized ({width}x{height}).")

    def spawn_cell(self, data: Any):
        """Creates a new cell at a random location."""
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        new_cell = Cell(x, y, data)
        self.cells.append(new_cell)
        self.logger.debug(f"Spawned cell at ({x}, {y}) with data: {data}")

    def step(self):
        """Advances the simulation by one step."""
        for cell in self.cells:
            # Move randomly
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            
            # Boundary checks
            new_x = max(0, min(self.width - 1, cell.x + dx))
            new_y = max(0, min(self.height - 1, cell.y + dy))
            
            cell.x = new_x
            cell.y = new_y
            
            # Aging and energy decay
            cell.age += 1
            cell.energy -= 0.01

        # Remove dead cells
        self.cells = [c for c in self.cells if c.energy > 0]

    def get_state(self) -> List[Dict[str, Any]]:
        """Returns the current state of all cells."""
        return [cell.to_dict() for cell in self.cells]
