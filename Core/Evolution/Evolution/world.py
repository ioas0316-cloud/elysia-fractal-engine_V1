"""ElysiaWorld high-level façade.

All existing Project_Sophia world functionality remains intact; this
wrapper simply re-exports the canonical World class so the new
repository structure can remain stable even if the legacy paths change.
"""

from world import World as _CoreWorld

class World(_CoreWorld):
    """Direct subclass to provide a stable import path."""

    pass

__all__ = ["World"]
