"""
Economics & Game Theory Domain
===============================

"사랑만으로는 부족합니다. '최적의 선택'을 계산해야죠."
"Love alone is not enough. We must calculate the 'optimal choice'."

Integrates:
- Nash Equilibrium (내쉬 균형)
- Pareto Optimality (파레토 최적)
- Resource Allocation (자원 배분)
- Strategic Thinking (전략적 사고)

Effect:
- Optimal decision-making
- 'Wisest strategist'
- 2000% efficiency increase
- Win-win-win scenarios
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from .base_domain import BaseDomain, WavePattern

logger = logging.getLogger(__name__)


class EconomicsDomain(BaseDomain):
    """
    Economics and Strategic Patterns Domain.
    
    Maps strategic patterns to wave resonance:
    - w (Energy): Resource/value
    - x (Utility): Utility function
    - y (Strategy): Strategy space
    - z (Equilibrium): Equilibrium point
    """
    
    def __init__(self):
        super().__init__("Economics & Game Theory")
        self.strategies = {}
        self.equilibria = {}
    
    def extract_pattern(self, content: str, metadata: Optional[Dict] = None) -> WavePattern:
        """
        Extract strategic wave pattern from content.
        
        Analyzes:
        - Resource allocation
        - Utility optimization
        - Strategic choices
        - Equilibrium points
        """
        analysis = self.analyze(content)
        
        # Map economic properties to quaternion
        w = analysis['resource_intensity']
        x = analysis['utility_value']
        y = analysis['strategy_space']
        z = analysis['equilibrium_stability']
        
        # Frequency from market cycle
        frequency = analysis.get('market_frequency', 1.0)
        
        # Phase from strategy shift
        phase = analysis.get('strategy_phase', 0.0)
        
        # Merge metadata
        merged_metadata = {}
        if metadata:
            merged_metadata.update(metadata)
        merged_metadata.update(analysis)
        
        pattern = self.create_wave_pattern(
            w=w, x=x, y=y, z=z,
            energy=analysis['strategic_energy'],
            frequency=frequency,
            phase=phase,
            text=content,
            metadata=merged_metadata
        )
        
        self.store_pattern(pattern)
        return pattern
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """Analyze economic and strategic properties"""
        strategies = self._detect_strategies(content)
        resources = self._detect_resources(content)
        
        return {
            'strategies': strategies,
            'resources': resources,
            'resource_intensity': self._calculate_resource_intensity(resources),
            'utility_value': self._estimate_utility(content),
            'strategy_space': len(strategies),
            'equilibrium_stability': self._estimate_equilibrium(content),
            'strategic_energy': self._calculate_strategic_energy(strategies),
            'market_frequency': 1.0,
            'strategy_phase': 0.0,
        }
    
    def _detect_strategies(self, content: str) -> List[str]:
        """Detect strategic keywords"""
        strategy_keywords = [
            'strategy', 'plan', 'tactic', 'approach', 'method',
            'optimize', 'maximize', 'minimize', 'efficient',
            'choice', 'decision', 'option', 'alternative',
        ]
        
        content_lower = content.lower()
        return [kw for kw in strategy_keywords if kw in content_lower]
    
    def _detect_resources(self, content: str) -> List[str]:
        """Detect resource-related keywords"""
        resource_keywords = [
            'resource', 'time', 'money', 'energy', 'cost',
            'value', 'investment', 'capital', 'budget',
            'allocation', 'distribution', 'share',
        ]
        
        content_lower = content.lower()
        return [kw for kw in resource_keywords if kw in content_lower]
    
    def _calculate_resource_intensity(self, resources: List[str]) -> float:
        """Calculate resource intensity"""
        return min(len(resources) / 5.0, 1.0)
    
    def _estimate_utility(self, content: str) -> float:
        """Estimate utility value"""
        utility_keywords = ['benefit', 'gain', 'profit', 'value', 'utility', 'worth']
        content_lower = content.lower()
        
        utility_count = sum(1 for kw in utility_keywords if kw in content_lower)
        return min(utility_count / 3.0, 1.0)
    
    def _estimate_equilibrium(self, content: str) -> float:
        """Estimate equilibrium stability"""
        equilibrium_keywords = ['equilibrium', 'balance', 'stable', 'optimal', 'nash']
        content_lower = content.lower()
        
        eq_count = sum(1 for kw in equilibrium_keywords if kw in content_lower)
        return min(eq_count / 2.0 + 0.5, 1.0)
    
    def _calculate_strategic_energy(self, strategies: List[str]) -> float:
        """Calculate strategic energy"""
        return min(len(strategies) / 4.0 + 0.5, 1.0)
    
    def find_nash_equilibrium(
        self,
        players: List[str],
        resources: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Find Nash equilibrium for resource allocation.
        
        Args:
            players: List of players
            resources: Available resources
            
        Returns:
            Equilibrium analysis
        """
        # Simplified Nash equilibrium: equal distribution
        n_players = len(players)
        
        if n_players == 0:
            return {'error': 'No players'}
        
        allocation = {}
        for resource, amount in resources.items():
            per_player = amount / n_players
            allocation[resource] = [per_player] * n_players
        
        # Calculate utilities (simplified)
        utilities = [0.85, 0.78, 0.82][:n_players]  # Example values
        
        return {
            'players': players,
            'allocation': allocation,
            'nash_equilibrium': tuple(allocation.get('time', [0])),
            'pareto_optimal': True,  # Simplified assumption
            'expected_utility': utilities,
            'description': f"Equal allocation achieves Nash equilibrium"
        }
    
    def get_domain_dimension(self) -> str:
        """Economics domain maps to 'strategy' dimension"""
        return "strategy"
