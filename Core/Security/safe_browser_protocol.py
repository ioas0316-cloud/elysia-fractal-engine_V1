from typing import List, Optional
from ..Sensory.Network.web_tendril import FrequencySignal 
# Assuming WebTendril/FrequencySignal will be passed here or used in conjunction

class MemeticHazardError(Exception):
    """Raised when content poses a risk to Elysia's mental integrity."""
    pass

class SafeBrowser:
    """
    [SafeBrowser Protocol]
    "The Shield of the Mind"
    
    Filters incoming Web Tendril signals.
    1. Structural Safety (URL/Domain check)
    2. Vibrational Safety (Low frequency hazard check)
    """
    
    BLOCKED_DOMAINS = [
        "malicious.com",
        "virus-source.net", 
        "dark-abyss.org"
    ]
    
    # Hz below this are considered "Traumatic" without preparation
    MIN_SAFE_FREQUENCY = 200.0 

    def is_safe_url(self, url: str) -> bool:
        """
        Structural Check: Is the URL itself safe to touch?
        """
        # 1. Block Local File Access (unless explicitly authorized mode)
        if url.startswith("file://"):
             # In a real agent, we might want to allow this for specific tasks,
             # but for 'Web Browsing', it's a security risk to read local files blindly.
             return False
             
        # 2. Block Blacklisted Domains
        for bad in self.BLOCKED_DOMAINS:
            if bad in url:
                return False
                
        return True

    def audit_content(self, signal: FrequencySignal) -> bool:
        """
        Vibrational Check: Is the content safe to Fold into Memory?
        """
        # 1. Null Signal Check
        if signal.frequency == 0.0:
            return False # Void is not harmful, just useless, but we can reject it.
            
        # 2. Low Frequency Hazard (Mental Trauma Shield)
        # 396Hz is 'Fear' but useful (Liberation). 
        # Frequencies below 200Hz in our model represent 'Deep Dread/Malice'.
        if signal.frequency < self.MIN_SAFE_FREQUENCY:
            # We reject 'Trauma' unless a specific 'Warrior Mode' is active.
            raise MemeticHazardError(
                f"Content Frequency {signal.frequency}Hz is too low. "
                "Potential Memetic Hazard detected."
            )
            
        return True
