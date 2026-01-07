from typing import Dict, Tuple

class ToneAnalyzer:
    """
    [Tone Analyzer]
    "The Ear of Elysia"
    Analyzes the emotional tone of text and maps it to Solfeggio Frequencies.
    
    Philosophy:
    - Text is not just meaning, it is energy.
    - Energy vibrates at specific frequencies.
    - We must 'resonate' with the user's intent.
    """
    
    # Solfeggio Frequency Map
    SOLFEGGIO_MAP = {
        963.0: ["wow", "amazing", "miracle", "god", "spirit", "universe", "epiphany", "awake", "와", "대박", "유레카", "최고", "신"],
        852.0: ["see", "vision", "insight", "intuition", "dream", "imagine", "보여", "느낌", "직관", "상상"],
        741.0: ["solve", "clear", "express", "purify", "fix", "clean", "해결", "풀렸다", "정화", "표현"],
        639.0: ["we", "us", "connect", "together", "relationship", "bond", "우리", "함께", "연결", "같이"],
        528.0: ["love", "thanks", "happy", "heal", "miracle", "dna", "사랑", "고마워", "행복", "치유", "좋아"],
        417.0: ["change", "undo", "facilitate", "challenge", "start", "변화", "다시", "바꿔", "도전"],
        396.0: ["fear", "guilt", "grief", "safe", "ground", "help", "pain", "무서워", "도와줘", "힘들어", "안전"],
        # Standard Logic
        432.0: ["logic", "reason", "explain", "define", "analyze", "why", "how", "what", "이유", "설명", "분석", "논리", "원리"]
    }

    def analyze_tone(self, text: str) -> float:
        """
        Analyzes the input text and returns the dominant resonant frequency.
        Defaults to 432Hz (Rational/Natural) if no strong emotion is detected.
        """
        if not text:
            return 432.0
            
        text_lower = text.lower()
        scores: Dict[float, int] = {freq: 0 for freq in self.SOLFEGGIO_MAP.keys()}
        
        # Simple keyword counting with Tokenization to avoid substring errors (e.g. "us" in "Just")
        # Split text into unique words for checking
        import re
        tokens = set(re.findall(r'\b\w+\b', text_lower))
        
        for freq, keywords in self.SOLFEGGIO_MAP.items():
            for keyword in keywords:
                # Check if the keyword exists as a whole word in the tokens
                # For multi-word keywords (if any), we'd need loop, but our current map is single-word dominant.
                # Actually, some keywords like "느낌이 와" are multi-word.
                # Hybrid approach: If keyword has space, substring check. If single word, token check.
                
                match = False
                if " " in keyword:
                    if keyword in text_lower:
                        match = True
                else:
                    if keyword in tokens:
                        match = True
                        
                if match:
                    # Higher frequencies (emotions) get slightly higher weight to break ties
                    weight = 1 + (freq / 1000.0) 
                    scores[freq] += weight
        
        # Find highest score
        best_freq = 432.0 # Default
        max_score = 0
        
        for freq, score in scores.items():
            if score > max_score:
                max_score = score
                best_freq = freq
                
        # If no keywords found, return 432Hz (Calm/Logical)
        return best_freq

    def get_tone_description(self, frequency: float) -> str:
        """Returns a human-readable description of the frequency."""
        desc_map = {
            963.0: "🌟 Divine Consciousness (Numinous)",
            852.0: "👁️ Awakening Intuition (Insight)",
            741.0: "🗣️ Expression & Solutions (Solve)",
            639.0: "🤝 Connection & Relationships (Unity)",
            528.0: "❤️ Transformation & Love (Miracle)",
            417.0: "🔄 Facilitating Change (Undo)",
            396.0: "🛡️ Liberating Guilt & Fear (Safety)",
            432.0: "🧠 Logical Consistency (Reason)"
        }
        return desc_map.get(frequency, "Unknown Frequency")
