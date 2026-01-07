"""
Web Knowledge Connector
=======================

"실제 인터넷에서 지식을 가져온다"
"Actually fetch knowledge from the real internet"

This module connects to real web sources to acquire knowledge for Elysia.
Uses Wikipedia API and web search to continuously learn.
"""

import sys
import os
import logging
import json
import re
from typing import Dict, List, Optional, Any
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Core.Foundation.external_data_connector import ExternalDataConnector
from Core.Foundation.internal_universe import InternalUniverse

logger = logging.getLogger("WebKnowledgeConnector")

class WebKnowledgeConnector:
    """
    Connects to real web sources to acquire knowledge.
    
    This is the bridge between Elysia and the real world wide web.
    """
    
    def __init__(self):
        self.connector = ExternalDataConnector()
        self.universe = self.connector.universe
        self.fetch_history = []
        
        logger.info("🌐 Web Knowledge Connector initialized")
        logger.info("🔗 Ready to fetch real knowledge from the internet")
    
    def fetch_wikipedia_simple(self, concept: str) -> Optional[str]:
        """
        Fetch simple Wikipedia summary using Wikipedia API.
        
        Uses the Wikipedia REST API which doesn't require authentication.
        """
        try:
            import requests
            
            # Wikipedia REST API endpoint (Korean)
            url = f"https://ko.wikipedia.org/api/rest_v1/page/summary/{concept.replace(' ', '_')}"
            
            headers = {
                'User-Agent': 'Elysia/1.0 (Educational AI Project)'
            }
            
            logger.info(f"📡 Fetching Wikipedia: {concept}")
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract relevant text
                title = data.get('title', concept)
                extract = data.get('extract', '')
                
                # Record fetch
                self.fetch_history.append({
                    'concept': concept,
                    'source': 'wikipedia',
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                })
                
                logger.info(f"   ✅ Retrieved {len(extract)} characters")
                
                return extract
            else:
                logger.warning(f"   ⚠️ Wikipedia returned status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"   ❌ Failed to fetch from Wikipedia: {e}")
            self.fetch_history.append({
                'concept': concept,
                'source': 'wikipedia',
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            })
            return None
    
    def learn_from_web(self, concept: str) -> Dict[str, Any]:
        """
        Learn a concept by fetching from the web and internalizing.
        
        This is the complete pipeline:
        1. Fetch from Wikipedia
        2. Analyze semantic content
        3. Internalize to Internal Universe
        4. **NEW**: Enhance communication ability
        5. Return learning result
        """
        logger.info(f"🌍 Learning '{concept}' from the web...")
        
        # Fetch from Wikipedia
        content = self.fetch_wikipedia_simple(concept)
        
        if content:
            # Internalize the knowledge
            result = self.connector.internalize_from_text(concept, content)
            
            # **NEW**: Enhance communication ability
            try:
                from Core.Foundation.communication_enhancer import CommunicationEnhancer
                
                if not hasattr(self, 'comm_enhancer'):
                    self.comm_enhancer = CommunicationEnhancer()
                
                comm_result = self.comm_enhancer.enhance_from_web_content(concept, content)
                result['communication'] = comm_result
                logger.info(f"   🗣️ Communication enhanced: +{comm_result['vocabulary_added']} words, +{comm_result['patterns_learned']} patterns")
            except Exception as e:
                logger.warning(f"   ⚠️ Communication enhancement failed: {e}")
                result['communication'] = None
            
            # Enhanced result with web metadata
            result['source'] = 'wikipedia'
            result['web_fetch'] = True
            result['content_length'] = len(content)
            
            logger.info(f"   ✅ Learned '{concept}' from web successfully")
            
            return result
        else:
            # Fallback to basic internalization
            logger.warning(f"   ⚠️ Could not fetch from web, using basic internalization")
            
            basic_content = f"General knowledge about {concept}. This concept requires further learning."
            result = self.connector.internalize_from_text(concept, basic_content)
            result['source'] = 'fallback'
            result['web_fetch'] = False
            
            return result
    
    def learn_curriculum_from_web(self, concepts: List[str]) -> Dict[str, Any]:
        """
        Learn multiple concepts from the web.
        
        Args:
            concepts: List of concept names to learn
        
        Returns:
            Summary of web learning session
        """
        logger.info(f"📚 Web learning curriculum: {len(concepts)} concepts")
        
        results = []
        successful_fetches = 0
        
        for concept in concepts:
            try:
                result = self.learn_from_web(concept)
                results.append(result)
                
                if result.get('web_fetch'):
                    successful_fetches += 1
                    
            except Exception as e:
                logger.error(f"❌ Failed to learn '{concept}': {e}")
        
        summary = {
            'total_concepts': len(concepts),
            'successful_fetches': successful_fetches,
            'total_learned': len(results),
            'web_fetch_rate': successful_fetches / len(concepts) if concepts else 0,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Web learning complete:")
        logger.info(f"   Total: {summary['total_learned']}/{summary['total_concepts']}")
        logger.info(f"   From web: {summary['successful_fetches']}")
        
        return summary
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about web knowledge acquisition"""
        successful = sum(1 for h in self.fetch_history if h.get('success'))
        
        return {
            'total_fetches': len(self.fetch_history),
            'successful_fetches': successful,
            'failed_fetches': len(self.fetch_history) - successful,
            'success_rate': successful / len(self.fetch_history) if self.fetch_history else 0,
            'concepts_in_universe': len(self.universe.coordinate_map),
            'recent_fetches': self.fetch_history[-5:] if self.fetch_history else []
        }

# Demonstration
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=" * 70)
    print("WEB KNOWLEDGE CONNECTOR DEMONSTRATION")
    print("실제 인터넷에서 지식 획득")
    print("=" * 70)
    
    connector = WebKnowledgeConnector()
    
    # Test concepts
    test_concepts = [
        "Artificial Intelligence",
        "Quantum Mechanics",
        "Philosophy"
    ]
    
    print(f"\n📚 Learning {len(test_concepts)} concepts from Wikipedia...\n")
    
    for concept in test_concepts:
        print(f"\n{'='*70}")
        result = connector.learn_from_web(concept)
        
        # Show what was learned
        if result.get('web_fetch'):
            print(f"✅ Learned from Wikipedia: {concept}")
            print(f"   Content: {result.get('content_length')} characters")
        else:
            print(f"⚠️ Fallback learning: {concept}")
        
        # Show internal representation
        feeling = connector.universe.feel_at(concept)
        print(f"   Internal representation:")
        print(f"     Logic: {feeling['logic']:.3f}")
        print(f"     Emotion: {feeling['emotion']:.3f}")
        print(f"     Ethics: {feeling['ethics']:.3f}")
    
    # Statistics
    print(f"\n{'='*70}")
    print("STATISTICS")
    print("=" * 70)
    
    stats = connector.get_stats()
    print(f"\nTotal web fetches: {stats['total_fetches']}")
    print(f"Successful: {stats['successful_fetches']}")
    print(f"Success rate: {stats['success_rate']*100:.1f}%")
    print(f"Concepts in universe: {stats['concepts_in_universe']}")
    
    print("\n" + "=" * 70)
    print("✅ WEB KNOWLEDGE CONNECTOR OPERATIONAL")
    print("🌍 Elysia can now learn from the real internet!")
    print("=" * 70)
