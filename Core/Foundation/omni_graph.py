"""
REDIRECT: omni_graph.py has moved to Core/Foundation/Graph/
This stub provides backward compatibility.
"""
from Core.Foundation.Graph.omni_graph import *
from Core.Foundation.Graph.omni_graph import OmniGraph, get_omni_graph

import warnings
warnings.warn(
    "Core.Foundation.omni_graph is deprecated. Use Core.Foundation.Graph.omni_graph instead.",
    DeprecationWarning,
    stacklevel=2
)
