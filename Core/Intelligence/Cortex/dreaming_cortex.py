"""
Dreaming Cortex (꿈의 피질)
=========================

원본: Legacy/Project_Sophia/dreaming_cortex.py
마이그레이션: 2025-12-15

유휴 시간에 최근 경험을 분석하고 개념을 추출하여
Spiderweb(지식 그래프)에 통합합니다.
"""
import logging
import json
import re
from typing import List, Dict, Any, Optional

try:
    from Core.Foundation.gemini_api import generate_text
except ImportError:
    generate_text = None


class DreamingCortex:
    """
    The DreamingCortex runs during 'idle' times to consolidate memories.
    It takes recent experiences and weaves them into the knowledge graph.
    """

    def __init__(self, core_memory=None, spiderweb=None, use_llm: bool = True):
        self.core_memory = core_memory
        self.spiderweb = spiderweb
        self.use_llm = use_llm and (generate_text is not None)
        self.logger = logging.getLogger("DreamingCortex")

    def _extract_concepts_llm(self, experience_content: str) -> Dict[str, Any]:
        """
        Uses LLM to extract semantic concepts and relations from experience content.
        
        Returns:
            {
                "concepts": ["concept1", "concept2", ...],
                "relations": [
                    {"source": "concept1", "target": "concept2", "type": "causes", "weight": 0.8}
                ]
            }
        """
        if not self.use_llm or generate_text is None:
            return self._extract_concepts_naive(experience_content)

        prompt = f"""
Analyze the following experience and extract key concepts and their relationships.
Return a JSON object with:
- "concepts": list of key concept strings
- "relations": list of objects with source, target, type (causes/enables/is_a/related_to), weight (0-1)

Experience: "{experience_content}"

JSON response (no markdown):
"""
        try:
            response = generate_text(prompt)
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(0))
                if "concepts" in result:
                    return result
        except Exception as e:
            self.logger.warning(f"LLM extraction failed: {e}")
        
        return self._extract_concepts_naive(experience_content)

    def _extract_concepts_naive(self, experience_content: str) -> Dict[str, Any]:
        """Fallback: Naive word-based concept extraction."""
        words = re.findall(r'\b[a-zA-Z가-힣]{3,}\b', experience_content.lower())
        # Filter common words
        stopwords = {'the', 'and', 'for', 'that', 'this', 'with', '이것', '그것', '저것'}
        concepts = [w for w in words if w not in stopwords][:10]
        return {"concepts": concepts, "relations": []}

    def dream(self) -> Dict[str, Any]:
        """
        The main dreaming process.
        1. Fetch unprocessed experiences
        2. Analyze them for concepts and relations
        3. Integrate into the knowledge graph
        4. Mark as processed
        """
        if not self.core_memory:
            return {"status": "skipped", "reason": "no core_memory"}

        self.logger.info("[DreamingCortex] Entering dream state...")
        
        # Get unprocessed experiences
        try:
            experiences = self.core_memory.get_unprocessed_experiences()
        except Exception:
            experiences = []
        
        if not experiences:
            self.logger.info("[DreamingCortex] No new experiences to process.")
            return {"status": "complete", "processed": 0}

        processed_count = 0
        total_concepts = []
        
        for exp in experiences:
            content = exp.get('content', '') if isinstance(exp, dict) else str(exp)
            
            # Extract concepts
            extracted = self._extract_concepts_llm(content)
            concepts = extracted.get('concepts', [])
            relations = extracted.get('relations', [])
            
            total_concepts.extend(concepts)
            
            # Integrate into spiderweb if available
            if self.spiderweb:
                for concept in concepts:
                    try:
                        self.spiderweb.add_node(concept)
                    except Exception:
                        pass
                        
                for rel in relations:
                    try:
                        self.spiderweb.add_edge(
                            rel['source'], 
                            rel['target'], 
                            weight=rel.get('weight', 0.5)
                        )
                    except Exception:
                        pass
            
            # Mark as processed
            if hasattr(self.core_memory, 'mark_processed'):
                try:
                    self.core_memory.mark_processed(exp)
                except Exception:
                    pass
            
            processed_count += 1

        self.logger.info(f"[DreamingCortex] Processed {processed_count} experiences, extracted {len(total_concepts)} concepts.")
        
        return {
            "status": "complete",
            "processed": processed_count,
            "concepts_extracted": len(set(total_concepts))
        }

    def consolidate(self):
        """Refines the Spiderweb by merging similar nodes or pruning weak links."""
        if not self.spiderweb:
            return
        
        self.logger.info("[DreamingCortex] Consolidating knowledge graph...")
        # Future: implement node merging and weak link pruning


# Singleton
_dreaming_cortex: Optional[DreamingCortex] = None

def get_dreaming_cortex() -> DreamingCortex:
    global _dreaming_cortex
    if _dreaming_cortex is None:
        _dreaming_cortex = DreamingCortex()
    return _dreaming_cortex
