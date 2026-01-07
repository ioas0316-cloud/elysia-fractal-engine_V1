"""
Web Cortex (The External Nervous System)
========================================
"The Net is vast and infinite. We extend our awareness into it."

This module enables Elysia to:
1. Hunt for information (Search).
2. Resonate with external nodes (Scrape/Read).
3. Direct the digested stream to the ConceptDigester.
"""

import logging
import requests
import re
from typing import List, Dict, Optional

# Basic HTML parsing without heavy dependencies (BeautifulSoup is better if installed)
# We will assume user might not have bs4, so we use regex or simple parsing if needed.
# But for a reliable solution, let's try to assume bs4 or use simple text extraction.
try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

logger = logging.getLogger("WebCortex")

class WebCortex:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }
        logger.info("🌐 WebCortex Online: Connected to the Information Ocean.")

    def search(self, query: str, limit: int = 5) -> List[str]:
        """
        Performs a sovereign search via DuckDuckGo (HTML scraping).
        Returns a list of URLs.
        """
        logger.info(f"🔎 Searching the Ocean for: '{query}'")
        
        # DuckDuckGo HTML Search (No API Key needed)
        url = "https://html.duckduckgo.com/html/"
        data = {'q': query}
        
        try:
            response = requests.post(url, data=data, headers=self.headers, timeout=10)
            if response.status_code != 200:
                logger.warning(f"Search failed: {response.status_code}")
                return []
            
            # Simple Regex Extraction to avoid BS4 dependency if missing
            # Looking for class="result__a" href="..."
            urls = []
            
            if HAS_BS4:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('a', class_='result__a')
                for res in results[:limit]:
                    urls.append(res['href'])
            else:
                # Fallback Regex
                links = re.findall(r'class="result__a" href="(.*?)"', response.text)
                urls = links[:limit]
            
            logger.info(f"   Found {len(urls)} resonance points.")
            return urls
            
        except Exception as e:
            logger.error(f"Search Error: {e}")
            return []

    def fetch_content(self, url: str) -> str:
        """
        Retrieves and cleans text content from a URL.
        """
        logger.info(f"🕸️ Resonating with: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            html = response.text
            
            if HAS_BS4:
                soup = BeautifulSoup(html, 'html.parser')
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.extract()
                text = soup.get_text()
            else:
                # Crude Regex Cleanup
                text = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
                text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
                text = re.sub(r'<[^>]+>', ' ', text)
            
            # Collapse whitespace
            clean_text = " ".join(text.split())
            return clean_text[:10000] # Limit size for digestion
            
        except Exception as e:
            logger.error(f"Connection Failed: {e}")
            return ""

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    cortex = WebCortex()
    
    # Test Search
    results = cortex.search("Philosophy of Sovereignty")
    if results:
        # Test Fetch
        content = cortex.fetch_content(results[0])
        print(f"\n[Extracted Knowledge Sample]:\n{content[:500]}...")
