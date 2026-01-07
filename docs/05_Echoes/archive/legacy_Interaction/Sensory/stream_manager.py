"""
Stream Manager - P4.0
Manages all stream sources and coordinates wave reception
"""

import asyncio
import logging
from typing import List, Optional
from .wave_stream_receiver import WaveStreamReceiver
from .stream_sources import *

logger = logging.getLogger(__name__)


class StreamManager:
    """
    Stream Manager - 전체 파동 스트림 조율
    
    Coordinates all knowledge source streams and manages wave reception.
    Integrates with P2.2 Wave Knowledge System.
    """
    
    def __init__(self):
        self.receiver = WaveStreamReceiver()
        self.running = False
        logger.info("🎛️ StreamManager initialized")
    
    def setup_default_sources(self, topics: List[str] = None):
        """Setup default knowledge sources"""
        logger.info("Setting up default knowledge sources...")
        if topics:
            logger.info(f"   Applying topic filters: {topics}")
        
        # YouTube
        youtube = YouTubeStreamSource(
            channels=[],  # Add channel IDs as needed
            search_query=None,
            topics=topics
        )
        self.receiver.add_stream_source(youtube)
        
        # Wikipedia
        wikipedia = WikipediaStreamSource(topics=topics)
        self.receiver.add_stream_source(wikipedia)
        
        # arXiv
        arxiv = ArxivStreamSource(topics=topics)
        self.receiver.add_stream_source(arxiv)
        
        # GitHub
        github = GitHubStreamSource(topics=topics)
        self.receiver.add_stream_source(github)
        
        # Stack Overflow
        stackoverflow = StackOverflowStreamSource(topics=topics)
        self.receiver.add_stream_source(stackoverflow)
        
        # Free Music Archive
        fma = FreeMusicArchiveSource(topics=topics)
        self.receiver.add_stream_source(fma)
        
        logger.info(f"✅ Setup {len(self.receiver.stream_sources)} sources")
    
    async def start_receiving(self):
        """Start receiving from all sources"""
        if self.running:
            logger.warning("Already running")
            return
        
        self.running = True
        logger.info("🚀 Starting wave stream reception...")
        
        # Setup sources if not already done
        if not self.receiver.stream_sources:
            self.setup_default_sources()
        
        # Start reception in background
        receive_task = asyncio.create_task(self.receiver.receive_streams())
        
        # Process waves
        try:
            await self.process_wave_stream()
        except KeyboardInterrupt:
            logger.info("Received stop signal")
        finally:
            self.stop()
    
    async def process_wave_stream(self):
        """Process incoming wave stream"""
        logger.info("🌊 Processing wave stream...")
        
        while self.running:
            # Get wave from buffer
            wave = await self.receiver.get_wave()
            
            if wave:
                await self.process_wave(wave)
            else:
                # No waves, wait a bit
                await asyncio.sleep(0.1)
    
    async def process_wave(self, wave):
        """Process a single wave"""
        # In full implementation:
        # 1. Extract phase resonance pattern (P4.2)
        # 2. Classify and filter (P4.3)
        # 3. Integrate with P2.2 Wave Knowledge System
        # 4. Store compressed pattern (P4.5)
        
        # For now, just log
        if self.receiver.stats['processed'] % 100 == 0:
            logger.info(f"  Processed {self.receiver.stats['processed']} waves")
        
        self.receiver.stats['processed'] += 1
    
    def stop(self):
        """Stop stream reception"""
        self.running = False
        self.receiver.stop()
        logger.info("🛑 StreamManager stopped")
    
    def get_stats(self):
        """Get statistics"""
        return self.receiver.get_stats()


# Convenience function for quick start
async def start_knowledge_stream():
    """
    Quick start function - begins receiving from all knowledge sources
    
    Usage:
        from Core.Interaction.Sensory import start_knowledge_stream
        
        # Run in async context
        await start_knowledge_stream()
    """
    manager = StreamManager()
    await manager.start_receiving()


if __name__ == "__main__":
    # Example usage
    async def main():
        manager = StreamManager()
        manager.setup_default_sources()
        
        # Run for 10 seconds as demo
        receive_task = asyncio.create_task(manager.receiver.receive_streams())
        await asyncio.sleep(10)
        
        manager.stop()
        
        # Show stats
        stats = manager.get_stats()
        print(f"\n📊 Statistics:")
        print(f"  Received: {stats['received']}")
        print(f"  Processed: {stats['processed']}")
        print(f"  Buffer: {stats['buffer_size']}")
        print(f"  Sources: {stats['sources']}")
    
    asyncio.run(main())
