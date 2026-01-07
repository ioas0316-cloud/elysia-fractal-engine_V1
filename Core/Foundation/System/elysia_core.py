"""
ELYSIA CORE
===========
The fundamental atomic units of the Living System.
"""

def Cell(name: str):
    """
    Decorator to mark a class as a 'Cell' (Atomic Unit).
    Cells are the smallest functional units of Elysia.
    """
    def decorator(cls):
        cls._elysia_type = "Cell"
        cls._elysia_name = name
        return cls
    return decorator

def Organ(name: str):
    """
    Decorator to mark a class as an 'Organ' (Functional Group).
    Organs are collections of Cells working together (e.g., Memory, Will).
    """
    def decorator(cls):
        cls._elysia_type = "Organ"
        cls._elysia_name = name
        return cls
    return decorator
