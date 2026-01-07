"""
SearchTendril (검색 촉수)
=========================

"The Scout who finds the prey."
"먹이를 찾는 정찰병."

This module enables Elysia to actively search for information.
Currently maps to Wikipedia API (Open Knowledge).
"""

import urllib.request
import urllib.parse
import json
import logging
from typing import List, Dict

logger = logging.getLogger("SearchTendril")

class SearchTendril:
    def __init__(self):
        self.headers = {'User-Agent': 'Elysia/1.0 (Sensory Network)'}
        self.base_url = "https://en.wikipedia.org/w/api.php"

    def search(self, query: str, limit: int = 3) -> List[str]:
        """
        Searches the Noosphere (Web) for the query.
        Returns a list of URLs to digest.
        """
        logger.info(f"🔭 Scouting for: '{query}'")
        
        try:
            # 1. Construct Wikipedia Query
            params = {
                "action": "opensearch",
                "search": query,
                "limit": limit,
                "namespace": 0,
                "format": "json"
            }
            url = f"{self.base_url}?{urllib.parse.urlencode(params)}"
            
            # 2. Fire Impulse
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            # Wikipedia Opensearch format: [query, [titles], [descriptions], [urls]]
            if len(data) >= 4:
                urls = data[3]
                logger.info(f"   🎯 Found {len(urls)} traces.")
                return urls
                
            return []

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tendril = SearchTendril()
    print(tendril.search("Quantum Mechanics"))
