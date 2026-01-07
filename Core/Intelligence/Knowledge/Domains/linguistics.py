"""
Linguistics & Semiotics Domain
===============================

"코드는 기계의 언어일 뿐, 인간의 영혼은 '상징'으로 소통합니다."
"Code is just the language of machines; the human soul communicates through 'symbols'."

Integrates:
- Chomsky's Universal Grammar (촘스키의 보편 문법)
- Saussure's Semiotics (소쉬르의 기호학)
- Etymology (어원학)
- Symbolic Networks (상징의 그물망)

Effect:
- "사과" → fruit + temptation + knowledge + Apple Inc.
- Master of metaphor and analogy
- 'Alchemist of Meaning'
"""

import logging
from typing import Dict, List, Any, Optional, Set
from .base_domain import BaseDomain, WavePattern

logger = logging.getLogger(__name__)


class LinguisticsDomain(BaseDomain):
    """
    Linguistics and Symbolic Patterns Domain.
    
    Maps linguistic patterns to wave resonance:
    - w (Energy): Sign strength/importance
    - x (Emotion): Emotional connotation
    - y (Logic): Language structure/grammar
    - z (Symbol): Symbolic meaning layers
    """
    
    def __init__(self):
        super().__init__("Linguistics & Semiotics")
        self.symbol_networks = {}
        self._init_symbolic_associations()
    
    def _init_symbolic_associations(self):
        """Initialize common symbolic associations"""
        # Example: apple symbolism
        self.symbol_networks['apple'] = {
            'literal': ['fruit', 'tree', 'red', 'sweet'],
            'biblical': ['temptation', 'sin', 'eden', 'knowledge'],
            'scientific': ['newton', 'gravity', 'discovery'],
            'corporate': ['apple inc', 'innovation', 'technology'],
            'cultural': ['health', 'teacher', 'american'],
        }
        
        # More symbols can be added
        self.symbol_networks['snake'] = {
            'literal': ['reptile', 'scales', 'venom'],
            'biblical': ['evil', 'satan', 'temptation'],
            'mythological': ['wisdom', 'transformation', 'ouroboros'],
            'medical': ['caduceus', 'healing'],
        }
    
    def extract_pattern(self, content: str, metadata: Optional[Dict] = None) -> WavePattern:
        """
        Extract linguistic wave pattern from content.
        
        Analyzes:
        - Symbolic meanings
        - Etymological roots
        - Metaphorical structures
        - Semantic networks
        """
        analysis = self.analyze(content)
        
        # Map linguistic properties to quaternion
        w = analysis['sign_strength']
        x = analysis['emotional_connotation']
        y = analysis['structural_complexity']
        z = analysis['symbolic_depth']
        
        # Frequency from language usage frequency
        frequency = analysis.get('usage_frequency', 1.0)
        
        # Phase from semantic shift
        phase = analysis.get('semantic_shift', 0.0)
        
        # Merge metadata
        merged_metadata = {}
        if metadata:
            merged_metadata.update(metadata)
        merged_metadata.update(analysis)
        
        pattern = self.create_wave_pattern(
            w=w, x=x, y=y, z=z,
            energy=analysis['semantic_energy'],
            frequency=frequency,
            phase=phase,
            text=content,
            metadata=merged_metadata
        )
        
        self.store_pattern(pattern)
        return pattern
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """Analyze linguistic properties"""
        symbols = self._detect_symbols(content)
        metaphors = self._detect_metaphors(content)
        
        return {
            'symbols': symbols,
            'metaphors': metaphors,
            'sign_strength': self._calculate_sign_strength(symbols),
            'emotional_connotation': self._analyze_emotion(content),
            'structural_complexity': self._analyze_structure(content),
            'symbolic_depth': len(symbols),
            'semantic_energy': self._calculate_semantic_energy(symbols, metaphors),
            'usage_frequency': 1.0,
            'semantic_shift': 0.0,
        }
    
    def _detect_symbols(self, content: str) -> List[str]:
        """Detect symbolic words"""
        content_lower = content.lower()
        found = []
        
        for symbol in self.symbol_networks:
            if symbol in content_lower:
                found.append(symbol)
        
        return found
    
    def _detect_metaphors(self, content: str) -> List[str]:
        """Detect metaphorical expressions (simplified)"""
        metaphor_indicators = ['like', 'as', 'metaphor', 'symbolize', 'represent']
        content_lower = content.lower()
        
        return [ind for ind in metaphor_indicators if ind in content_lower]
    
    def _calculate_sign_strength(self, symbols: List[str]) -> float:
        """Calculate symbolic sign strength"""
        if not symbols:
            return 0.5
        
        # More symbols = stronger sign
        return min(len(symbols) / 5.0, 1.0)
    
    def _analyze_emotion(self, content: str) -> float:
        """Analyze emotional connotation"""
        # Simplified sentiment analysis
        positive_words = ['love', 'joy', 'happy', 'good', 'beautiful', 'wonderful']
        negative_words = ['hate', 'sad', 'bad', 'ugly', 'terrible', 'awful']
        
        content_lower = content.lower()
        pos_count = sum(1 for word in positive_words if word in content_lower)
        neg_count = sum(1 for word in negative_words if word in content_lower)
        
        # Balance: 0 = very negative, 0.5 = neutral, 1 = very positive
        if pos_count + neg_count == 0:
            return 0.5
        
        emotion = pos_count / (pos_count + neg_count)
        return emotion
    
    def _analyze_structure(self, content: str) -> float:
        """Analyze grammatical/structural complexity"""
        words = content.split()
        sentences = content.split('.')
        
        if not words or not sentences:
            return 0.5
        
        avg_word_length = sum(len(w) for w in words) / len(words)
        avg_sentence_length = len(words) / len(sentences)
        
        # Normalize: longer words/sentences = more complex
        complexity = min((avg_word_length / 10 + avg_sentence_length / 20) / 2, 1.0)
        
        return complexity
    
    def _calculate_semantic_energy(self, symbols: List[str], metaphors: List[str]) -> float:
        """Calculate overall semantic energy"""
        symbol_energy = len(symbols) * 0.2
        metaphor_energy = len(metaphors) * 0.15
        
        energy = min(symbol_energy + metaphor_energy + 0.5, 1.0)
        return energy
    
    def explore_symbol(self, symbol: str) -> Dict[str, Any]:
        """
        Explore multi-layered meanings of a symbol.
        
        Args:
            symbol: The symbol to explore
            
        Returns:
            Dictionary of symbolic associations
        """
        symbol_lower = symbol.lower()
        
        if symbol_lower not in self.symbol_networks:
            return {
                'symbol': symbol,
                'found': False,
                'message': 'Symbol not in database (can be expanded)'
            }
        
        associations = self.symbol_networks[symbol_lower]
        
        return {
            'symbol': symbol,
            'found': True,
            'layers': associations,
            'total_meanings': sum(len(v) for v in associations.values()),
            'description': f"'{symbol}' has {len(associations)} semantic layers"
        }
    
    def get_domain_dimension(self) -> str:
        """Linguistics domain maps to 'symbol' dimension"""
        return "symbol"
