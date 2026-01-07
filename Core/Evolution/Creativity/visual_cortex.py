"""
DEPRECATED: This module has been consolidated.
Use Core.Visual.visual_cortex instead.

This file redirects imports for backward compatibility.
"""

from Core.Sensory.Visual.visual_cortex import VisualCortex, get_visual_cortex

__all__ = ["VisualCortex", "get_visual_cortex"]

# Log deprecation warning
import warnings
warnings.warn(
    "Core.Creativity.visual_cortex is deprecated. Use Core.Visual.visual_cortex instead.",
    DeprecationWarning,
    stacklevel=2
)
