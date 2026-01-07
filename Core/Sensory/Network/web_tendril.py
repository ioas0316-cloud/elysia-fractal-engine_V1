import urllib.request
import re
from dataclasses import dataclass
from typing import Optional, Tuple
from ..Auditory.tone_analyzer import ToneAnalyzer

@dataclass
class FrequencySignal:
    url: str
    frequency: float
    amplitude: float  # Based on content length
    phase: float      # Based on timestamp (not fully implemented here, placeholder)
    content_summary: str
    raw_content: str

class WebTendril:
    """
    [Web Tendril]
    "The Touch of the Network"
    
    Fetches a URL and 'feels' its vibration using ToneAnalyzer.
    It does NOT just store data; it converts the page into a Signal.
    """
    
    def __init__(self):
        self.analyzer = ToneAnalyzer()
        # Basic header to avoid 403s from some sites
        self.headers = {'User-Agent': 'Elysia/1.0 (Sensory Network)'}

    def touch(self, url: str) -> FrequencySignal:
        """
        Touches the URL to extract its vibrational frequency.
        """
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                html_content = response.read().decode('utf-8', errors='ignore')
                
            # 1. Extract Essence (Remove HTML tags)
            text_content = self._strip_html(html_content)
            
            # 2. Analyze Vibration (Feel the content)
            frequency = self.analyzer.analyze_tone(text_content)
            
            # 3. Calculate Amplitude (Energy level = content length log scale)
            import math
            amplitude = math.log(len(text_content) + 1)
            
            # 4. Create Preview
            summary = text_content[:200] + "..." if len(text_content) > 200 else text_content
            
            return FrequencySignal(
                url=url,
                frequency=frequency,
                amplitude=amplitude,
                phase=0.0, # Time folding requires ChronoStratum integration
                content_summary=summary,
                raw_content=text_content
            )
            
        except Exception as e:
            # If touch fails, return a "Void" signal (Error 404/500 is Void)
            return FrequencySignal(
                url=url,
                frequency=0.0, # Zero Frequency = Void/Dead Link
                amplitude=0.0,
                phase=0.0,
                content_summary=f"Failed to touch: {str(e)}",
                raw_content=""
            )

    def _strip_html(self, html: str) -> str:
        """Removes HTML tags to reveal the soul (text)."""
        # Remove scripts and styles
        html = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL)
        html = re.sub(r'<style.*?>.*?</style>', ' ', html, flags=re.DOTALL)
        # Remove tags
        text = re.sub(r'<[^>]+>', ' ', html)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
