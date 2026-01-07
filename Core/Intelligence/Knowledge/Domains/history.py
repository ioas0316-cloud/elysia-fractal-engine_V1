"""
History & Anthropology Domain
==============================

"과거를 모르는 지성은 미래를 예측할 수 없습니다."
"An intelligence that doesn't know the past cannot predict the future."

Integrates:
- Causal Patterns (인과율의 빅데이터)
- Civilizational Cycles (문명의 흥망성쇠)
- Human Behavioral Patterns (인간 행동 패턴)
- Socio-cultural Context (사회문화적 맥락)

Effect:
- Statistical prophecy
- Pattern recognition from history
- "90% fail here, but this path leads to hero status"
- Future prediction accuracy
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from .base_domain import BaseDomain, WavePattern

logger = logging.getLogger(__name__)


class HistoryDomain(BaseDomain):
    """
    History and Anthropological Patterns Domain.
    
    Maps historical patterns to wave resonance:
    - w (Energy): Event impact/influence
    - x (Emotion): Zeitgeist (spirit of the age)
    - y (Logic): Causal relationships
    - z (Pattern): Recurring patterns
    """
    
    def __init__(self):
        super().__init__("History & Anthropology")
        self.historical_patterns = {}
        self._init_civilization_cycles()
    
    def _init_civilization_cycles(self):
        """Initialize known civilization cycles"""
        self.historical_patterns = {
            'industrial_revolution': {
                'period': '1760-1840',
                'impact': 0.9,
                'pattern': 'technological disruption',
                'outcome': '90% social disruption, massive change',
            },
            'printing_press': {
                'period': '1440+',
                'impact': 0.85,
                'pattern': 'knowledge democratization',
                'outcome': '85% literacy increase, information revolution',
            },
            'internet': {
                'period': '1990s+',
                'impact': 0.95,
                'pattern': 'connectivity revolution',
                'outcome': '95% global connectivity, digital transformation',
            },
        }
    
    def extract_pattern(self, content: str, metadata: Optional[Dict] = None) -> WavePattern:
        """
        Extract historical wave pattern from content.
        
        Analyzes:
        - Historical significance
        - Causal chains
        - Recurring patterns
        - Zeitgeist
        """
        analysis = self.analyze(content)
        
        # Map historical properties to quaternion
        w = analysis['event_impact']
        x = analysis['zeitgeist']
        y = analysis['causality']
        z = analysis['pattern_recognition']
        
        # Frequency from historical cycle
        frequency = analysis.get('cycle_frequency', 1.0)
        
        # Phase from temporal position
        phase = analysis.get('temporal_phase', 0.0)
        
        # Merge metadata
        merged_metadata = {}
        if metadata:
            merged_metadata.update(metadata)
        merged_metadata.update(analysis)
        
        pattern = self.create_wave_pattern(
            w=w, x=x, y=y, z=z,
            energy=analysis['historical_energy'],
            frequency=frequency,
            phase=phase,
            text=content,
            metadata=merged_metadata
        )
        
        self.store_pattern(pattern)
        return pattern
    
    def analyze(self, content: str) -> Dict[str, Any]:
        """Analyze historical properties"""
        patterns = self._detect_patterns(content)
        
        return {
            'patterns': patterns,
            'event_impact': self._calculate_impact(content),
            'zeitgeist': self._analyze_zeitgeist(content),
            'causality': self._analyze_causality(content),
            'pattern_recognition': len(patterns),
            'historical_energy': self._calculate_historical_energy(content),
            'cycle_frequency': 1.0,
            'temporal_phase': 0.0,
        }
    
    def _detect_patterns(self, content: str) -> List[str]:
        """Detect historical patterns"""
        content_lower = content.lower()
        detected = []
        
        for pattern_name in self.historical_patterns:
            if pattern_name.replace('_', ' ') in content_lower:
                detected.append(pattern_name)
        
        return detected
    
    def _calculate_impact(self, content: str) -> float:
        """Calculate event impact"""
        impact_keywords = [
            'revolution', 'transformation', 'change', 'impact',
            'significant', 'major', 'critical', 'pivotal',
        ]
        
        content_lower = content.lower()
        impact_count = sum(1 for kw in impact_keywords if kw in content_lower)
        
        return min(impact_count / 4.0 + 0.5, 1.0)
    
    def _analyze_zeitgeist(self, content: str) -> float:
        """Analyze spirit of the age"""
        zeitgeist_keywords = [
            'era', 'age', 'period', 'time', 'epoch',
            'culture', 'society', 'spirit', 'mood',
        ]
        
        content_lower = content.lower()
        zeit_count = sum(1 for kw in zeitgeist_keywords if kw in content_lower)
        
        return min(zeit_count / 3.0 + 0.4, 1.0)
    
    def _analyze_causality(self, content: str) -> float:
        """Analyze causal relationships"""
        causal_keywords = [
            'cause', 'effect', 'result', 'consequence',
            'because', 'therefore', 'thus', 'hence',
            'led to', 'resulted in', 'triggered',
        ]
        
        content_lower = content.lower()
        causal_count = sum(1 for kw in causal_keywords if kw in content_lower)
        
        return min(causal_count / 3.0 + 0.5, 1.0)
    
    def _calculate_historical_energy(self, content: str) -> float:
        """Calculate historical energy"""
        # Based on impact and pattern recognition
        impact = self._calculate_impact(content)
        causality = self._analyze_causality(content)
        
        energy = (impact + causality) / 2
        return min(energy, 1.0)
    
    def analyze_current_situation(self, context: str) -> Dict[str, Any]:
        """
        Analyze current situation against historical patterns.
        
        Args:
            context: Description of current situation
            
        Returns:
            Historical analysis with prediction
        """
        # Detect similar historical events
        similar_events = []
        
        for pattern_name, pattern_data in self.historical_patterns.items():
            # Simple keyword matching
            if any(word in context.lower() for word in pattern_name.split('_')):
                similar_events.append({
                    'event': pattern_name.replace('_', ' ').title(),
                    'period': pattern_data['period'],
                    'impact': pattern_data['impact'],
                    'pattern': pattern_data['pattern'],
                    'outcome': pattern_data['outcome'],
                })
        
        if not similar_events:
            similar_events.append({
                'event': 'General Historical Pattern',
                'impact': 0.7,
                'outcome': 'Change and adaptation required',
            })
        
        # Calculate confidence
        avg_impact = sum(e['impact'] for e in similar_events) / len(similar_events)
        confidence = min(avg_impact, 0.95)
        
        prediction = self._make_prediction(similar_events, confidence)
        
        return {
            'context': context,
            'similar_events': similar_events,
            'prediction': prediction,
            'confidence': confidence,
            'advice': self._generate_advice(similar_events),
        }
    
    def _make_prediction(self, events: List[Dict], confidence: float) -> str:
        """Make prediction based on historical events"""
        if confidence > 0.8:
            return "This path leads to hero status"
        elif confidence > 0.6:
            return "Significant transformation likely"
        else:
            return "Uncertain path, adaptability key"
    
    def _generate_advice(self, events: List[Dict]) -> str:
        """Generate advice based on historical patterns"""
        avg_impact = sum(e.get('impact', 0.5) for e in events) / len(events)
        
        if avg_impact > 0.85:
            return "역사적으로 이런 상황에서는 90%가 실패했습니다. 하지만 이 길로 가면 영웅이 되었죠."
        else:
            return "과거의 패턴을 배우고, 새로운 길을 만드세요."
    
    def get_domain_dimension(self) -> str:
        """History domain maps to 'pattern' dimension"""
        return "pattern"
