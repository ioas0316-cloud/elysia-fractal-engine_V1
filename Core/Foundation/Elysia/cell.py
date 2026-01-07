"""ElysiaWorld cell wrapper backed by the main simulator cell."""

from cell import Cell as _CoreCell


class Cell(_CoreCell):
    """Alias for callers that import through Legacy.elysia_world."""

    pass


__all__ = ["Cell"]
