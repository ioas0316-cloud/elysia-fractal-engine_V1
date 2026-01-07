"""
Domain Integration Layer
=========================

Integrates all 5 knowledge domains for multi-dimensional understanding.

Enables:
- Cross-domain wave resonance
- Multi-dimensional queries
- Holistic knowledge synthesis
"""

import logging
from typing import Dict, List, Any, Optional
from .linguistics import LinguisticsDomain
from .architecture import ArchitectureDomain
from .economics import EconomicsDomain
from .history import HistoryDomain
from .mythology import MythologyDomain
from .base_domain import BaseDomain, WavePattern

logger = logging.getLogger(__name__)


class DomainIntegration:
    """
    Integration layer for all knowledge domains.
    
    Provides:
    - Unified interface to all domains
    - Cross-domain resonance matching
    - Multi-dimensional query system
    """
    
    def __init__(self):
        self.domains = {
            'linguistics': LinguisticsDomain(),
            'architecture': ArchitectureDomain(),
            'economics': EconomicsDomain(),
            'history': HistoryDomain(),
            'mythology': MythologyDomain(),
        }
        
        logger.info("🌈 Domain Integration Layer initialized with 5 domains")
    
    def process_content(
        self,
        content: str,
        domains: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Dict[str, WavePattern]:
        """
        Process content through multiple domains.
        
        Args:
            content: Text content to process
            domains: List of domain names to use (None = all)
            metadata: Optional metadata
            
        Returns:
            Dictionary of domain_name -> WavePattern
        """
        if domains is None:
            domains = list(self.domains.keys())
        
        patterns = {}
        
        for domain_name in domains:
            if domain_name in self.domains:
                domain = self.domains[domain_name]
                pattern = domain.extract_pattern(content, metadata)
                patterns[domain_name] = pattern
                logger.debug(f"Processed through {domain_name}: {content[:50]}")
        
        return patterns
    
    def analyze_holistic(self, content: str) -> Dict[str, Any]:
        """
        Perform holistic analysis across all domains.
        
        Args:
            content: Content to analyze
            
        Returns:
            Comprehensive multi-domain analysis
        """
        analyses = {}
        
        for domain_name, domain in self.domains.items():
            try:
                analysis = domain.analyze(content)
                analyses[domain_name] = analysis
            except Exception as e:
                logger.warning(f"Error analyzing with {domain_name}: {e}")
                analyses[domain_name] = {'error': str(e)}
        
        # Aggregate insights
        total_patterns = sum(
            len(domain.patterns) for domain in self.domains.values()
        )
        
        return {
            'individual_analyses': analyses,
            'total_patterns_stored': total_patterns,
            'active_domains': len(self.domains),
            'synthesis': self._synthesize_insights(analyses),
        }
    
    def _synthesize_insights(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesize insights from multiple domain analyses.
        
        Returns:
            Unified insights
        """
        synthesis = {
            'dominant_themes': [],
            'cross_domain_resonance': 0.0,
            'depth_score': 0.0,
        }
        
        # Count domain activations
        active_domains = sum(
            1 for analysis in analyses.values() 
            if isinstance(analysis, dict) and 'error' not in analysis
        )
        
        synthesis['cross_domain_resonance'] = active_domains / len(analyses)
        
        # Calculate depth from multiple dimensions
        depth_factors = []
        
        if 'linguistics' in analyses and 'symbolic_depth' in analyses['linguistics']:
            depth_factors.append(analyses['linguistics']['symbolic_depth'])
        
        if 'architecture' in analyses and 'fractal_dim' in analyses['architecture']:
            depth_factors.append(analyses['architecture']['fractal_dim'])
        
        if 'mythology' in analyses and 'archetype_intensity' in analyses['mythology']:
            depth_factors.append(analyses['mythology']['archetype_intensity'])
        
        if depth_factors:
            synthesis['depth_score'] = sum(depth_factors) / len(depth_factors)
        
        return synthesis
    
    def query_multi_dimensional(
        self,
        query: str,
        domains: Optional[List[str]] = None,
        top_k: int = 5
    ) -> Dict[str, List[WavePattern]]:
        """
        Query across multiple domains.
        
        Args:
            query: Query string
            domains: Domains to query (None = all)
            top_k: Number of results per domain
            
        Returns:
            Dictionary of domain_name -> patterns
        """
        if domains is None:
            domains = list(self.domains.keys())
        
        results = {}
        
        for domain_name in domains:
            if domain_name in self.domains:
                domain = self.domains[domain_name]
                patterns = domain.query_patterns(query, top_k)
                results[domain_name] = patterns
        
        return results
    
    def get_domain(self, name: str) -> Optional[BaseDomain]:
        """Get specific domain by name"""
        return self.domains.get(name)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about all domains"""
        stats = {
            'total_domains': len(self.domains),
            'domains': {},
        }
        
        for domain_name, domain in self.domains.items():
            stats['domains'][domain_name] = {
                'name': domain.name,
                'patterns_stored': len(domain.patterns),
                'dimension': domain.get_domain_dimension(),
            }
        
        stats['total_patterns'] = sum(
            len(domain.patterns) for domain in self.domains.values()
        )
        
        return stats
    
    def clear_all(self):
        """Clear all stored patterns from all domains"""
        for domain in self.domains.values():
            domain.patterns.clear()
        
        logger.info("Cleared all patterns from all domains")


# Convenience function for quick integration
def analyze_with_all_domains(content: str) -> Dict[str, Any]:
    """
    Quick analysis with all domains.
    
    Args:
        content: Content to analyze
        
    Returns:
        Comprehensive analysis
    """
    integration = DomainIntegration()
    return integration.analyze_holistic(content)
