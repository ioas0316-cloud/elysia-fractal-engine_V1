"""
REDIRECT: ollama_bridge.py has moved to Core/Foundation/Network/
This stub provides backward compatibility.
"""
import warnings
warnings.warn(
    "Core.Foundation.ollama_bridge is deprecated. Use Core.Foundation.Network.ollama_bridge instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import everything from the new location
from Core.Foundation.Network.ollama_bridge import *

# Explicit imports for commonly used symbols
from Core.Foundation.Network.ollama_bridge import (
    OllamaBridge,
    ollama,
    get_ollama_bridge,
)

