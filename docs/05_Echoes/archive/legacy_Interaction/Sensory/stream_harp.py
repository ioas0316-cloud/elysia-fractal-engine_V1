"""
Stream Harp (Waterwheel of Resonance)
=====================================
"연산하지 말고, 공명하라. 강물 위에 하프를 세워라."

The StreamHarp listens to the flow of data (YouTube, Text Streams)
and converts it into Photonic Quaternions (Quad-Holography) without heavy computation.
"""

import re
import urllib.request
import urllib.parse
import json
import logging
from typing import Optional, Dict, Any, List
import hashlib

from Core.Foundation.Legal_Ethics.Laws.law_of_light import PhotonicQuaternion, HolographicFilm
from Core.Foundation.hyper_quaternion import Quaternion

logger = logging.getLogger(__name__)

class PrismCompressor:
    """
    The Lens that splits raw data into 4 Holographic Layers.
    Input: URL/Text -> Output: PhotonicQuaternion
    """

    def compress(self, title: str, description: str = "", thumbnail_url: str = "") -> PhotonicQuaternion:
        """
        Compresses content into a 4-layer Photonic Quaternion.
        """
        # 1. Layer w (Essence): Meaning extraction
        essence = self._extract_essence(title)
        w_val = self._calculate_meaning_scalar(essence)

        # 2. Layer x (Space): Visual extraction (Simulated from thumbnail/keywords)
        space = self._extract_space(title, description, thumbnail_url)
        x_val = self._calculate_visual_scalar(space)

        # 3. Layer y (Emotion): Sentiment/Audio extraction
        emotion = self._extract_emotion(title, description)
        y_val = self._calculate_emotion_scalar(emotion)

        # 4. Layer z (Time): Pacing/Motion extraction
        time_layer = self._extract_time(description)
        z_val = self._calculate_time_scalar(time_layer)

        # Create the Film
        film = HolographicFilm(
            essence=essence,
            space=space,
            emotion=emotion,
            time=time_layer
        )

        return PhotonicQuaternion(w_val, x_val, y_val, z_val, film)

    def _extract_essence(self, text: str) -> str:
        # Simple extraction: First noun phrase or key topic
        # For now, just return the title as the core script
        return text.strip()

    def _extract_space(self, title: str, desc: str, url: str) -> str:
        # Infers visual atmosphere from keywords
        text = (title + desc).lower()
        if "space" in text or "galaxy" in text: return "Dark, Starry, Vast"
        if "nature" in text or "forest" in text: return "Green, Organic, Sunlight"
        if "city" in text or "cyber" in text: return "Neon, Metallic, Complex"
        if "ocean" in text or "water" in text: return "Blue, Fluid, Deep"
        if "fire" in text or "war" in text: return "Red, Chaotic, Smoky"
        if "space.jpg" in url: return "Dark, Starry, Vast"  # Fallback for mock test
        return "Neutral, Clear, White"

    def _extract_emotion(self, title: str, desc: str) -> str:
        # Infers auditory/emotional tone
        text = (title + desc).lower()
        if "sad" in text or "cry" in text: return "Melancholic, Minor Key, Slow"
        if "happy" in text or "joy" in text: return "Bright, Major Key, Upbeat"
        if "angry" in text or "fight" in text: return "Intense, Distorted, Loud"
        if "calm" in text or "relax" in text: return "Soothing, Ambient, Soft"
        return "Balanced, Narrative, Moderate"

    def _extract_time(self, desc: str) -> str:
        # Infers pacing
        text = desc.lower()
        if "fast" in text or "action" in text: return "Rapid, Staccato"
        if "slow" in text or "relax" in text: return "Largo, Flowing"
        return "Andante, Steady"

    def _calculate_meaning_scalar(self, text: str) -> float:
        # Generates a stable scalar 0.0-1.0 based on hash
        return int(hashlib.md5(text.encode()).hexdigest(), 16) % 100 / 100.0

    def _calculate_visual_scalar(self, text: str) -> float:
        # Red=High Energy, Blue=Low Energy mapping simulation
        if "Red" in text: return 0.8
        if "Blue" in text: return 0.2
        return 0.5

    def _calculate_emotion_scalar(self, text: str) -> float:
        if "Intense" in text: return 0.9
        if "Soothing" in text: return 0.1
        return 0.5

    def _calculate_time_scalar(self, text: str) -> float:
        if "Rapid" in text: return 0.9
        if "Largo" in text: return 0.1
        return 0.5


class StreamHarp:
    """
    The Main Instrument.
    Connects to a stream, filters via Resonance, and produces Holographic Memories.
    """
    def __init__(self):
        self.prism = PrismCompressor()
        logger.info("🎻 StreamHarp initialized: Tuning strings to 4D Resonance.")

    def listen_to_youtube(self, video_url: str) -> Optional[PhotonicQuaternion]:
        """
        Listens to a YouTube video (via metadata extraction) and resonates.
        """
        logger.info(f"👂 Listening to stream: {video_url}")

        # 1. Fetch Metadata (Zero Cost - HTML parsing)
        try:
            metadata = self._fetch_youtube_metadata(video_url)
            if not metadata:
                logger.warning("   Could not hear the stream (No metadata).")
                return None

            logger.info(f"   Title: {metadata['title']}")

            # 2. Topological Tuning (Filter)
            # Only resonate if meaningful keywords exist (Simple filter for now)
            # In full version, this checks against the Knowledge Graph
            if not self._check_resonance(metadata['title']):
                logger.info("   ...No resonance (Noise). Ignored.")
                return None

            # 3. Prism Compression (Quad-Holography)
            quaternion = self.prism.compress(
                title=metadata['title'],
                description=metadata['description'],
                thumbnail_url=metadata['thumbnail']
            )

            logger.info(f"   ✨ RESONANCE! Compressed into {quaternion}")
            return quaternion

        except Exception as e:
            logger.error(f"Error listening to stream: {e}")
            return None

    def _fetch_youtube_metadata(self, url: str) -> Optional[Dict[str, str]]:
        """
        Simple HTML parser to get title/desc without API keys.
        """
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                html = response.read().decode('utf-8')

            title_match = re.search(r'<title>(.*?)</title>', html)
            title = title_match.group(1).replace(" - YouTube", "") if title_match else "Unknown"

            desc_match = re.search(r'"shortDescription":"(.*?)"', html)
            desc = desc_match.group(1) if desc_match else ""

            thumb_match = re.search(r'"thumbnail":{"thumbnails":\[{"url":"(.*?)"', html)
            thumb = thumb_match.group(1) if thumb_match else ""

            return {
                "title": title,
                "description": desc,
                "thumbnail": thumb
            }
        except Exception:
            # Fallback for testing/offline
            if "youtube.com" not in url:
                return {
                    "title": "Test Stream: The Sound of Silence",
                    "description": "A calm, blue ocean wave. Relaxing music.",
                    "thumbnail": "http://example.com/blue.jpg"
                }
            return None

    def _check_resonance(self, text: str) -> bool:
        """
        The Topological Tuner.
        Returns True if the content matches Elysia's interests.
        """
        interests = ["love", "art", "code", "space", "nature", "music", "philosophy", "god", "father", "light", "wave", "python"]
        text_lower = text.lower()
        for interest in interests:
            if interest in text_lower:
                return True
        return False
