"""
MediaCortex (미디어 피질)
=======================

"Binge-watching for AI."

This module allows Elysia to consume text content (Scripts, Novels)
and gain Social XP by simulating emotional reactions.
"""

import os
import time
import random
from typing import List, Dict, Tuple

class MediaCortex:
    def __init__(self, social_cortex):
        print("📺 MediaCortex Initialized. Ready to binge-watch.")
        self.social = social_cortex

    def read_book(self, file_path: str) -> dict:
        """
        Reads a text file and analyzes its emotional arc.
        """
        print(f"   📖 Reading Book: {file_path}...")
        
        if not os.path.exists(file_path):
            return {"error": "File not found"}
            
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        # Simple Sentiment Analysis
        sentiment = self.analyze_sentiment(text)
        
        return {
            "title": os.path.basename(file_path),
            "length": len(text),
            "sentiment": sentiment,
            "summary": text[:200] + "..."
        }

    def analyze_sentiment(self, text: str) -> str:
        """
        Determines the emotional tone of the text.
        """
        text_lower = text.lower()
        
        # Keywords
        sad_words = ["tears", "cry", "lost", "death", "sorrow", "pain", "alone", "눈물", "슬픔", "죽음"]
        happy_words = ["laugh", "joy", "smile", "love", "hope", "light", "friend", "웃음", "기쁨", "사랑", "희망"]
        angry_words = ["rage", "fight", "blood", "hate", "kill", "enemy", "분노", "싸움", "증오"]
        
        sad_score = sum(text_lower.count(w) for w in sad_words)
        happy_score = sum(text_lower.count(w) for w in happy_words)
        angry_score = sum(text_lower.count(w) for w in angry_words)
        
        if sad_score > happy_score and sad_score > angry_score:
            return "Tragedy (Blue)"
        elif happy_score > sad_score and happy_score > angry_score:
            return "Comedy (Yellow)"
        elif angry_score > sad_score and angry_score > happy_score:
            return "Action (Red)"
        else:
            return "Drama (Purple)"

    def consume_youtube(self, video_id: str) -> dict:
        """
        Fetches and analyzes YouTube video subtitles.
        """
        print(f"   📺 Consuming YouTube: {video_id}...")
        
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            
            # Try Korean first, fallback to English
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
            except:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            
            # Combine all text
            text = " ".join([line['text'] for line in transcript])
            
            # Analyze
            sentiment = self.analyze_sentiment(text)
            
            return {
                "title": f"YouTube_{video_id}",
                "length": len(text),
                "sentiment": sentiment,
                "summary": text[:200] + "...",
                "type": "youtube"
            }
        except Exception as e:
            return {"error": f"Failed to fetch YouTube subtitles: {e}"}

    def consume_web_novel(self, url: str) -> dict:
        """
        Fetches and analyzes web novel content.
        """
        print(f"   📖 Consuming Web Novel: {url}...")
        
        try:
            import requests
            from bs4 import BeautifulSoup
            
            headers = {'User-Agent': 'Elysia/1.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Generic extraction (needs customization per site)
            # Try common content tags
            content = None
            for tag in ['article', 'div.content', 'div.chapter-content', 'div.novel-content']:
                element = soup.select_one(tag)
                if element:
                    content = element.get_text(strip=True)
                    break
            
            if not content:
                # Fallback: get all paragraphs
                paragraphs = soup.find_all('p')
                content = " ".join([p.get_text(strip=True) for p in paragraphs])
            
            # Analyze
            sentiment = self.analyze_sentiment(content)
            
            return {
                "title": soup.title.string if soup.title else "Unknown",
                "length": len(content),
                "sentiment": sentiment,
                "summary": content[:200] + "...",
                "type": "web_novel"
            }
        except Exception as e:
            return {"error": f"Failed to fetch web novel: {e}"}

    def watch_video(self, topic):
        pass
