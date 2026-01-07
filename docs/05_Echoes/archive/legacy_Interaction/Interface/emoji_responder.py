# Emoji Responder Plugin
"""
Example plugin that adds emojis to responses based on detected emotions.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.System.System.System.Plugin.plugin_base import PluginBase
from typing import Dict, Any

class EmojiResponderPlugin(PluginBase):
    """Add emojis to responses based on emotional keywords."""
    
    def __init__(self):
        super().__init__("EmojiResponder")
        self.emoji_map = {
            'love': '💖', 'light': '✨', 'dream': '💫', 'hope': '🌟',
            'pain': '💔', 'sad': '😢', 'tear': '😭',
            'happy': '😊', 'joy': '🎉',
            '사랑': '💖', '빛': '✨', '꿈': '💫', '희망': '🌟',
            '고통': '💔', '슬픔': '😢', '눈물': '😭',
            '행복': '😊', '기쁨': '🎉',
        }
    
    def process(self, user_input: str, response: str, context: Dict[str, Any]) -> str:
        """Add emojis to the response if emotional keywords are detected."""
        if not self.enabled:
            return response
        
        detected_emojis = set()
        for keyword, emoji in self.emoji_map.items():
            if keyword in user_input.lower() or keyword in response.lower():
                detected_emojis.add(emoji)
        
        if detected_emojis:
            return response + " " + "".join(list(detected_emojis)[:2])
        return response
