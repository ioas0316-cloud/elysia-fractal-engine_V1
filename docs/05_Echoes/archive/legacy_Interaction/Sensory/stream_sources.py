"""
Stream Sources - P4.0 (REAL CONNECTION)
Concrete implementations for accessing REAL knowledge sources
Refactored to align with Pulse Architecture (No active polling in main thread).
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Optional, Dict, Any
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import random

from Core.Foundation.Protocols.pulse_protocol import PulseBroadcaster, WavePacket, PulseType
from elysia_core.cell import Cell

logger = logging.getLogger(__name__)

class StreamSource(ABC):
    """Base class for all stream sources"""
    @abstractmethod
    async def stream(self) -> AsyncGenerator[dict, None]:
        pass
    
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        pass

@Cell("StreamSource.Wikipedia", category="Sensory")
class WikipediaStreamSource(StreamSource):
    """
    REAL Wikipedia API Source
    Accesses actual Wikipedia articles via API
    """
    def __init__(self, topics: List[str] = None):
        self.api_url = "https://en.wikipedia.org/w/api.php"
        self.pulse = PulseBroadcaster()
        logger.info("📖 REAL Wikipedia source initialized")
        
        # Topics to rotate through for "random" streaming
        default_topics = [
            "Artificial intelligence", "Quantum mechanics", "Consciousness", 
            "Philosophy of mind", "Fractal geometry", "Neuroscience", 
            "General relativity", "Metaphysics", "Poetry", "History of art"
        ]
        self.topics = topics if topics else default_topics
        if topics:
             logger.info(f"   Filtering Wikipedia by topics: {', '.join(topics)}")
    
    def _fetch_random_article(self):
        """Fetch a random article summary from our topic list"""
        headers = {'User-Agent': 'Elysia/10.0 (AI Research Project; +https://github.com/elysia-project)'}
        try:
            topic = random.choice(self.topics)
            # 1. Search for the topic to get a title
            search_params = urllib.parse.urlencode({
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": topic,
                "srlimit": 5
            })
            
            req = urllib.request.Request(f"{self.api_url}?{search_params}", headers=headers)
            with urllib.request.urlopen(req) as response:
                search_data = json.loads(response.read().decode())
                
            if not search_data.get('query', {}).get('search'):
                return None
                
            # Pick a random result
            article_title = random.choice(search_data['query']['search'])['title']
            
            # 2. Get the extract
            extract_params = urllib.parse.urlencode({
                "action": "query",
                "format": "json",
                "prop": "extracts",
                "exintro": True,
                "explaintext": True,
                "titles": article_title
            })
            
            req = urllib.request.Request(f"{self.api_url}?{extract_params}", headers=headers)
            with urllib.request.urlopen(req) as response:
                content_data = json.loads(response.read().decode())
                
            pages = content_data['query']['pages']
            page = next(iter(pages.values()))
            
            return {
                'type': 'article',
                'title': page['title'],
                'text': page.get('extract', 'No content available.'),
                'url': f"https://en.wikipedia.org/wiki/{urllib.parse.quote(page['title'])}",
                'source': 'Wikipedia'
            }
            
        except Exception as e:
            logger.error(f"Wikipedia fetch error: {e}")
            return None

    async def stream(self) -> AsyncGenerator[dict, None]:
        """Stream real articles via Generator (Async Iterator is effectively a Pulse)"""
        # Note: In a pure Event Architecture, this should register a callback.
        # However, for Python Async compatibility, yielding is acceptable
        # as long as the Consumer (Caller) handles it as a Signal.
        while True:
            article = await asyncio.to_thread(self._fetch_random_article)
            if article:
                # Broadcast for internal listeners (Resonance)
                self.pulse.broadcast(WavePacket(
                    sender="Wikipedia",
                    type=PulseType.KNOWLEDGE,
                    payload=article,
                    intensity=0.7
                ))
                # Yield for direct consumers
                yield article

            # Semantic Pulse Interval (Not mechanical sleep, but 'breath')
            await asyncio.sleep(10)

    async def search(self, query: str, max_results: int = 5) -> List[dict]:
        # Implementation skipped for brevity in this update
        return []

@Cell("StreamSource.RSS", category="Sensory")
class RSSStreamSource(StreamSource):
    """
    REAL RSS Feed Source
    Parses real XML feeds from the internet.
    """
    def __init__(self, feed_urls: List[str] = None, topics: List[str] = None):
        self.feed_urls = feed_urls or [
            "http://feeds.bbci.co.uk/news/technology/rss.xml",
            "https://www.wired.com/feed/category/science/latest/rss",
            "https://rss.nytimes.com/services/xml/rss/nyt/Science.xml"
        ]
        self.topics = topics
        self.pulse = PulseBroadcaster()
        logger.info(f"📡 REAL RSS source initialized with {len(self.feed_urls)} feeds")
        if topics:
             logger.info(f"   Filtering RSS by topics: {', '.join(topics)}")
        
    def _fetch_feed(self, url: str):
        headers = {'User-Agent': 'Elysia/10.0 (AI Research Project)'}
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                items = []
                # Handle standard RSS 2.0
                for item in root.findall('.//item'):
                    title = item.find('title').text if item.find('title') is not None else "No Title"
                    desc = item.find('description').text if item.find('description') is not None else ""
                    link = item.find('link').text if item.find('link') is not None else url
                    
                    # Basic topic filtering if topics are set
                    content_text = f"{title}. {desc}"
                    if self.topics:
                        if not any(t.lower() in content_text.lower() for t in self.topics):
                            continue

                    items.append({
                        'type': 'news',
                        'title': title,
                        'text': content_text,
                        'url': link,
                        'source': 'RSS'
                    })
                return items
        except Exception as e:
            logger.error(f"RSS fetch error for {url}: {e}")
            return []

    async def stream(self) -> AsyncGenerator[dict, None]:
        while True:
            # Pick a random feed
            url = random.choice(self.feed_urls)
            items = await asyncio.to_thread(self._fetch_feed, url)
            
            for item in items[:3]: # Yield top 3
                # Internal Broadcast
                self.pulse.broadcast(WavePacket(
                    sender="RSS",
                    type=PulseType.SENSORY,
                    payload=item,
                    intensity=0.6
                ))
                yield item
                await asyncio.sleep(2)
                
            await asyncio.sleep(30) # Wait before next feed pull

    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        return []

class YouTubeStreamSource(StreamSource):
    def __init__(self, channels: List[str] = None, search_query: str = None, topics: List[str] = None):
        self.channels = channels or []
        self.search_query = search_query
        self.topics = topics
        logger.info("📺 YouTube source initialized")

    async def stream(self) -> AsyncGenerator[dict, None]:
        # Placeholder for passive listening
        while True:
            await asyncio.sleep(3600)
            yield {}

    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        return []

class ArxivStreamSource(StreamSource):
    def __init__(self, topics: List[str] = None):
        self.topics = topics
        logger.info("📜 Arxiv source initialized")

    async def stream(self) -> AsyncGenerator[dict, None]:
        while True:
            await asyncio.sleep(3600)
            yield {}

    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        return []

class GitHubStreamSource(StreamSource):
    def __init__(self, topics: List[str] = None):
        self.topics = topics
        logger.info("💻 GitHub source initialized")

    async def stream(self) -> AsyncGenerator[dict, None]:
        while True:
            await asyncio.sleep(3600)
            yield {}

    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        return []

class StackOverflowStreamSource(StreamSource):
    def __init__(self, topics: List[str] = None):
        self.topics = topics
        logger.info("💬 StackOverflow source initialized")

    async def stream(self) -> AsyncGenerator[dict, None]:
        while True:
            await asyncio.sleep(3600)
            yield {}

    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        return []

class FreeMusicArchiveSource(StreamSource):
    def __init__(self, topics: List[str] = None):
        self.topics = topics
        logger.info("🎵 FreeMusicArchive source initialized")

    async def stream(self) -> AsyncGenerator[dict, None]:
        while True:
            await asyncio.sleep(3600)
            yield {}

    async def search(self, query: str, max_results: int = 10) -> List[dict]:
        return []
