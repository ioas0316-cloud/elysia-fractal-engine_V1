
import logging
import re
from typing import Optional

logger = logging.getLogger("ConceptSanitizer")

class ConceptSanitizer:
    """
    The Kidney.
    Filters out toxic or noisy data before it enters the bloodstream (TorchGraph).
    
    Rules:
    1. No pure numbers or symbols unless meaningful (e.g., 'C++' is ok, '---' is not).
    2. No internal IDs or hashes (e.g., 'Star -12345').
    3. Length limits (3 < len < 50).
    """
    
    def __init__(self):
        logger.info("🛡️ Kidney (Sanitizer) active - Filtering noise.")
        # Regex for 'Noise' (e.g., just numbers and symbols)
        self.noise_pattern = re.compile(r'^[\d\W_]+$')
        
    def is_valid(self, concept: str) -> bool:
        """
        Check if a concept is healthy enough to enter the system.
        """
        if not concept: return False
        
        concept = concept.strip()
        
        # Rule 1: Length
        if len(concept) < 2 or len(concept) > 60:
            return False
            
        # Rule 2: Not Just Noise
        if self.noise_pattern.match(concept):
            return False
            
        # Rule 3: No negative ID artifacts (common in scraped data)
        # e.g., "Star -1123"
        if re.search(r' -\d+$', concept):
            return False
            
        return True

    def sanitize(self, concept: str) -> Optional[str]:
        """
        Attempts to clean a concept. Returns None if it cannot be saved.
        """
        if not concept: return None
        
        cleaned = concept.strip()
        
        # Remove trailing negative IDs specific to wiki dumps often
        # "Subject -1223" -> "Subject"
        cleaned = re.sub(r' -\d+$', '', cleaned)
        
        # Remove surrouding quotes
        cleaned = cleaned.strip('"\'')
        
        if self.is_valid(cleaned):
            return cleaned
        return None

_sanitizer = None
def get_sanitizer():
    global _sanitizer
    if not _sanitizer:
        _sanitizer = ConceptSanitizer()
    return _sanitizer
