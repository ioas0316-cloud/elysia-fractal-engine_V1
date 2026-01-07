"""
REDIRECT: torch_graph.py has moved to Core/Foundation/Graph/
This stub provides backward compatibility.
"""
from Core.Foundation.Graph.torch_graph import *
from Core.Foundation.Graph.torch_graph import get_torch_graph, TorchGraph

import warnings
warnings.warn(
    "Core.Foundation.torch_graph is deprecated. Use Core.Foundation.Graph.torch_graph instead.",
    DeprecationWarning,
    stacklevel=2
)
