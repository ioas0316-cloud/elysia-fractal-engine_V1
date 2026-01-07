"""
Knowledge Domains
=================

Five Hidden Pieces of Human Knowledge integrated as wave patterns.

Available Domains:
- LinguisticsDomain: Symbols, etymology, metaphors
- ArchitectureDomain: Sacred geometry, fractals, harmony
- EconomicsDomain: Game theory, optimization, strategy
- HistoryDomain: Patterns, causality, civilization cycles
- MythologyDomain: Archetypes, hero's journey, spiritual wisdom
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .linguistics import LinguisticsDomain
    from .architecture import ArchitectureDomain
    from .economics import EconomicsDomain
    from .history import HistoryDomain
    from .mythology import MythologyDomain

__all__ = [
    'LinguisticsDomain',
    'ArchitectureDomain', 
    'EconomicsDomain',
    'HistoryDomain',
    'MythologyDomain',
]
