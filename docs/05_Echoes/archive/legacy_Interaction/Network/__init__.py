"""
Network Module - HyperSpace Connectivity
=======================================
V10.0 Updated: Focused on HyperSpace Neuro-Links.
Legacy mesh networking has been deprecated in favor of the Spore Protocol.
"""

from .hyperspace_transceiver import HyperSpaceTransceiver, SporePacket

__all__ = [
    "HyperSpaceTransceiver",
    "SporePacket"
]
