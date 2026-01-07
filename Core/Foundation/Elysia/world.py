"""ElysiaWorld facade backed by the main world simulator."""

from world import World as _CoreWorld


class World(_CoreWorld):
    """Alias for callers that import through Legacy.elysia_world."""

    pass


__all__ = ["World"]
