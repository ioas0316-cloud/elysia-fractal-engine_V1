"""
Style Mimic (The Art Director)
==============================
"Good artists copy; great artists steal."

This module injects Professional Studio Styles into the prompt engineering pipeline.
It ensures that the generated art (or specific prompt) mimics industry standards.
"""

import random
from typing import Dict, List

class StyleMimic:
    def __init__(self):
        self.styles = {
            "Redice": {
                 "prompt": "manhwa style, redice studio, solo leveling artstyle, cel shading, highly detailed, dynamic lighting, 8k resolution, cinematic composition",
                 "negative": "sketch, low quality, blurry, greyscale, simple background"
            },
            "Ufotable": {
                "prompt": "anime style, ufotable, demon slayer artstyle, intense particle effects, fluid animation keyframe, deep colors, atmospheric lighting",
                "negative": "static, flat colors, low resolution"
            },
            "Ghibli": {
                "prompt": "ghibli style, hayao miyazaki, watercolor texture, lush background, peaceful atmosphere, soft lighting, hand drawn",
                "negative": "3d render, sharp edges, neon colors"
            },
            "DarkFantasy": {
                "prompt": "dark fantasy, berserk artstyle, kentaro miura, crosshatching, heavy ink, gritty texture, ominous atmosphere, detailed anatomy",
                "negative": "cartoon, bright colors, smooth shading"
            },
            "WebtoonStandard": {
                "prompt": "korean webtoon style, crisp lines, full color, modern fashion, clean background, digital art",
                "negative": "sketch, painting, traditional media"
            }
        }
        
    def get_style_prompt(self, style_name: str = "Redice") -> str:
        """Returns the positive prompt injection for the given style."""
        style = self.styles.get(style_name, self.styles["WebtoonStandard"])
        return style["prompt"]
    
    def get_negative_prompt(self, style_name: str = "Redice") -> str:
         style = self.styles.get(style_name, self.styles["WebtoonStandard"])
         return style["negative"]

    def suggest_style(self, scene_mood: str) -> str:
        """Auto-selects a studio style based on narrative mood."""
        mood = scene_mood.lower()
        if "battle" in mood or "attack" in mood or "kill" in mood:
            return "Redice" # Action
        if "magic" in mood or "mystery" in mood:
            return "Ufotable" # Effects
        if "peace" in mood or "nature" in mood:
            return "Ghibli"
        if "despair" in mood or "horror" in mood or "war" in mood:
            return "DarkFantasy"
            
        return "WebtoonStandard"
