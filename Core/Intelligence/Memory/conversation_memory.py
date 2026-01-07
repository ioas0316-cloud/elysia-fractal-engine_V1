"""
Conversation Memory System (대화 기억 시스템)
=============================================

"진짜 대화는 맥락을 기억하는 것에서 시작된다"
"Real conversation begins with remembering context"

Philosophy:
-----------
Humans naturally maintain conversation context across multiple turns,
learning communication styles, preferences, and building relationship depth.
This system gives Elysia the same capability.

Architecture:
-------------
1. Short-term: Recent N turns (immediate context)
2. Mid-term: Session summary (current conversation)
3. Long-term: User profile (learned patterns across sessions)
4. Emotional: Emotional arc of conversation

Integration with existing systems:
- Starlight Memory: For long-term conversation memories
- Emotional Engine: For emotional context tracking
- Working Memory (conversation_state.py): For keyword-based summaries
"""

import logging
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from collections import deque
import json

logger = logging.getLogger("ConversationMemory")


@dataclass
class ConversationTurn:
    """
    Single turn in a conversation.
    대화의 한 턴
    """
    # Core content
    user_message: str
    assistant_message: str
    
    # Metadata
    timestamp: float = field(default_factory=time.time)
    turn_number: int = 0
    
    # Emotional context (from EmotionalEngine)
    user_emotion: Optional[str] = None  # Detected user emotion
    assistant_emotion: Optional[str] = None  # Elysia's emotional state
    emotional_valence: float = 0.0  # -1 (negative) to 1 (positive)
    
    # Topical info
    topics: List[str] = field(default_factory=list)
    intent: Optional[str] = None  # question, statement, request, etc.
    
    # Language
    language: str = "ko"  # ko, en, ja
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "user_message": self.user_message,
            "assistant_message": self.assistant_message,
            "timestamp": self.timestamp,
            "turn_number": self.turn_number,
            "user_emotion": self.user_emotion,
            "assistant_emotion": self.assistant_emotion,
            "emotional_valence": self.emotional_valence,
            "topics": self.topics,
            "intent": self.intent,
            "language": self.language
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationTurn':
        """Restore from dictionary"""
        return cls(**data)


@dataclass
class UserProfile:
    """
    Learned profile of a user across conversations.
    사용자 프로필 (여러 대화에서 학습)
    """
    user_id: str
    
    # Communication style
    preferred_language: str = "ko"
    formality_level: float = 0.5  # 0 (casual) to 1 (formal)
    verbosity_preference: float = 0.5  # 0 (brief) to 1 (detailed)
    
    # Topics of interest
    favorite_topics: List[str] = field(default_factory=list)
    avoided_topics: List[str] = field(default_factory=list)
    
    # Emotional patterns
    typical_mood: str = "neutral"
    emotional_sensitivity: float = 0.5  # How much to adjust emotional expressions
    
    # Interaction history
    total_conversations: int = 0
    total_turns: int = 0
    first_interaction: float = field(default_factory=time.time)
    last_interaction: float = field(default_factory=time.time)
    
    # Learned patterns
    common_greetings: List[str] = field(default_factory=list)
    common_phrases: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "user_id": self.user_id,
            "preferred_language": self.preferred_language,
            "formality_level": self.formality_level,
            "verbosity_preference": self.verbosity_preference,
            "favorite_topics": self.favorite_topics,
            "avoided_topics": self.avoided_topics,
            "typical_mood": self.typical_mood,
            "emotional_sensitivity": self.emotional_sensitivity,
            "total_conversations": self.total_conversations,
            "total_turns": self.total_turns,
            "first_interaction": self.first_interaction,
            "last_interaction": self.last_interaction,
            "common_greetings": self.common_greetings,
            "common_phrases": self.common_phrases
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserProfile':
        """Restore from dictionary"""
        return cls(**data)


class ConversationMemory:
    """
    Comprehensive conversation memory system.
    종합 대화 기억 시스템
    
    Features:
    - Short-term context (recent N turns)
    - Session management
    - User profile learning
    - Emotional arc tracking
    - Language adaptation
    """
    
    def __init__(self, 
                 max_context_turns: int = 10,
                 max_session_turns: int = 100):
        """
        Initialize conversation memory.
        
        Args:
            max_context_turns: Number of recent turns to keep in active context
            max_session_turns: Maximum turns per session before archiving
        """
        self.max_context_turns = max_context_turns
        self.max_session_turns = max_session_turns
        
        # Short-term: Recent context (deque for efficient sliding window)
        self.context: deque[ConversationTurn] = deque(maxlen=max_context_turns)
        
        # Current session
        self.session_turns: List[ConversationTurn] = []
        self.session_start_time: float = time.time()
        self.session_id: str = f"session_{int(self.session_start_time)}"
        
        # User profiles (user_id -> UserProfile)
        self.user_profiles: Dict[str, UserProfile] = {}
        self.current_user_id: Optional[str] = None
        
        # Session statistics
        self.turn_counter: int = 0
        self.session_counter: int = 0
        
        logger.info(f"✨ ConversationMemory initialized (context={max_context_turns}, session={max_session_turns})")
    
    def add_turn(self,
                 user_message: str,
                 assistant_message: str,
                 user_emotion: Optional[str] = None,
                 assistant_emotion: Optional[str] = None,
                 emotional_valence: float = 0.0,
                 topics: Optional[List[str]] = None,
                 intent: Optional[str] = None,
                 language: str = "ko",
                 user_id: Optional[str] = None):
        """
        Add a conversation turn to memory.
        대화 턴을 메모리에 추가
        
        Args:
            user_message: User's message
            assistant_message: Elysia's response
            user_emotion: Detected user emotion
            assistant_emotion: Elysia's emotional state
            emotional_valence: Emotional valence of the turn
            topics: Topics discussed
            intent: User's intent
            language: Language used
            user_id: User identifier (for profile learning)
        """
        self.turn_counter += 1
        
        # Create turn object
        turn = ConversationTurn(
            user_message=user_message,
            assistant_message=assistant_message,
            timestamp=time.time(),
            turn_number=self.turn_counter,
            user_emotion=user_emotion,
            assistant_emotion=assistant_emotion,
            emotional_valence=emotional_valence,
            topics=topics or [],
            intent=intent,
            language=language
        )
        
        # Add to short-term context
        self.context.append(turn)
        
        # Add to session
        self.session_turns.append(turn)
        
        # Update user profile if user_id provided
        if user_id:
            self.current_user_id = user_id
            self._update_user_profile(user_id, turn)
        
        logger.debug(f"Turn {self.turn_counter} added to conversation memory")
        
        # Check if session should be archived
        if len(self.session_turns) >= self.max_session_turns:
            self._archive_session()
    
    def get_context(self, n_turns: Optional[int] = None) -> List[ConversationTurn]:
        """
        Get recent conversation context.
        최근 대화 맥락 가져오기
        
        Args:
            n_turns: Number of turns to retrieve (default: all in context)
            
        Returns:
            List of recent conversation turns
        """
        turns = list(self.context)
        if n_turns is not None:
            turns = turns[-n_turns:]
        return turns
    
    def get_context_string(self, 
                          n_turns: Optional[int] = None,
                          format_style: str = "simple") -> str:
        """
        Get context as formatted string for prompt injection.
        프롬프트에 주입할 맥락 문자열 생성
        
        Args:
            n_turns: Number of turns to include
            format_style: 'simple', 'detailed', or 'emotional'
            
        Returns:
            Formatted context string
        """
        turns = self.get_context(n_turns)
        
        if not turns:
            return ""
        
        lines = []
        
        if format_style == "simple":
            for turn in turns:
                lines.append(f"User: {turn.user_message}")
                lines.append(f"Assistant: {turn.assistant_message}")
        
        elif format_style == "detailed":
            for turn in turns:
                lines.append(f"[Turn {turn.turn_number}] User: {turn.user_message}")
                if turn.topics:
                    lines.append(f"  Topics: {', '.join(turn.topics)}")
                lines.append(f"  Assistant: {turn.assistant_message}")
        
        elif format_style == "emotional":
            for turn in turns:
                emotion_info = f" ({turn.user_emotion})" if turn.user_emotion else ""
                lines.append(f"User{emotion_info}: {turn.user_message}")
                
                asst_emotion = f" ({turn.assistant_emotion})" if turn.assistant_emotion else ""
                lines.append(f"Assistant{asst_emotion}: {turn.assistant_message}")
        
        return "\n".join(lines)
    
    def get_emotional_arc(self, n_turns: Optional[int] = None) -> List[float]:
        """
        Get emotional valence trajectory over recent turns.
        최근 대화의 감정 궤적
        
        Args:
            n_turns: Number of turns to analyze
            
        Returns:
            List of emotional valence values
        """
        turns = self.get_context(n_turns)
        return [turn.emotional_valence for turn in turns]
    
    def get_dominant_topics(self, n_turns: Optional[int] = None, top_k: int = 5) -> List[Tuple[str, int]]:
        """
        Get most discussed topics in recent context.
        최근 대화의 주요 주제
        
        Args:
            n_turns: Number of turns to analyze
            top_k: Number of top topics to return
            
        Returns:
            List of (topic, count) tuples
        """
        turns = self.get_context(n_turns)
        
        # Count topic occurrences
        topic_counts: Dict[str, int] = {}
        for turn in turns:
            for topic in turn.topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Sort by count
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_topics[:top_k]
    
    def get_user_profile(self, user_id: Optional[str] = None) -> Optional[UserProfile]:
        """
        Get user profile.
        사용자 프로필 가져오기
        
        Args:
            user_id: User identifier (uses current user if None)
            
        Returns:
            UserProfile or None
        """
        uid = user_id or self.current_user_id
        if uid is None:
            return None
        return self.user_profiles.get(uid)
    
    def _update_user_profile(self, user_id: str, turn: ConversationTurn):
        """
        Update user profile based on conversation turn.
        대화 턴에 기반하여 사용자 프로필 업데이트
        """
        # Get or create profile
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(user_id=user_id)
        
        profile = self.user_profiles[user_id]
        
        # Update interaction stats
        profile.total_turns += 1
        profile.last_interaction = turn.timestamp
        
        # Learn language preference
        if turn.language:
            profile.preferred_language = turn.language
        
        # Update favorite topics
        for topic in turn.topics:
            if topic not in profile.favorite_topics:
                # Add if mentioned multiple times
                count = sum(1 for t in self.session_turns if topic in t.topics)
                if count >= 2:
                    profile.favorite_topics.append(topic)
                    # Keep only top 10
                    if len(profile.favorite_topics) > 10:
                        profile.favorite_topics = profile.favorite_topics[-10:]
        
        # Detect formality level (simple heuristic)
        if any(word in turn.user_message.lower() for word in ["please", "thank", "sorry", "excuse", "제발", "감사", "죄송"]):
            profile.formality_level = min(1.0, profile.formality_level + 0.05)
        elif any(word in turn.user_message.lower() for word in ["hey", "yo", "sup", "야", "어이"]):
            profile.formality_level = max(0.0, profile.formality_level - 0.05)
        
        # Learn typical mood
        if turn.user_emotion:
            profile.typical_mood = turn.user_emotion
    
    def _archive_session(self):
        """
        Archive current session and start new one.
        현재 세션을 아카이브하고 새 세션 시작
        """
        if not self.session_turns:
            return
        
        # Could integrate with Starlight Memory here for long-term storage
        logger.info(f"📦 Archiving session {self.session_id} with {len(self.session_turns)} turns")
        
        # Update user profile conversation count
        if self.current_user_id and self.current_user_id in self.user_profiles:
            self.user_profiles[self.current_user_id].total_conversations += 1
        
        # Start new session
        self.session_turns = []
        self.session_counter += 1
        self.session_start_time = time.time()
        self.session_id = f"session_{int(self.session_start_time)}"
        
        logger.info(f"🆕 Started new session: {self.session_id}")
    
    def clear_context(self):
        """Clear short-term context (keep session and profiles)"""
        self.context.clear()
        logger.info("🧹 Cleared short-term context")
    
    def end_session(self):
        """Explicitly end current session and archive"""
        self._archive_session()
    
    def save_to_file(self, filepath: str):
        """
        Save conversation memory to file.
        파일에 저장
        """
        data = {
            "session_id": self.session_id,
            "session_start_time": self.session_start_time,
            "turn_counter": self.turn_counter,
            "session_counter": self.session_counter,
            "current_user_id": self.current_user_id,
            "context": [turn.to_dict() for turn in self.context],
            "session_turns": [turn.to_dict() for turn in self.session_turns],
            "user_profiles": {uid: profile.to_dict() for uid, profile in self.user_profiles.items()}
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"💾 Saved conversation memory to {filepath}")
    
    def load_from_file(self, filepath: str):
        """
        Load conversation memory from file.
        파일에서 로드
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.session_id = data.get("session_id", self.session_id)
            self.session_start_time = data.get("session_start_time", self.session_start_time)
            self.turn_counter = data.get("turn_counter", 0)
            self.session_counter = data.get("session_counter", 0)
            self.current_user_id = data.get("current_user_id")
            
            # Restore context
            self.context = deque(
                [ConversationTurn.from_dict(t) for t in data.get("context", [])],
                maxlen=self.max_context_turns
            )
            
            # Restore session
            self.session_turns = [ConversationTurn.from_dict(t) for t in data.get("session_turns", [])]
            
            # Restore user profiles
            self.user_profiles = {
                uid: UserProfile.from_dict(pdata)
                for uid, pdata in data.get("user_profiles", {}).items()
            }
            
            logger.info(f"📂 Loaded conversation memory from {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to load conversation memory: {e}")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of conversation memory.
        대화 메모리 요약 통계
        """
        return {
            "session_id": self.session_id,
            "total_turns": self.turn_counter,
            "context_size": len(self.context),
            "session_turns": len(self.session_turns),
            "total_sessions": self.session_counter,
            "tracked_users": len(self.user_profiles),
            "current_user": self.current_user_id,
            "session_duration_minutes": (time.time() - self.session_start_time) / 60.0
        }


# Convenience function for integration
def create_conversation_memory(context_turns: int = 10) -> ConversationMemory:
    """
    Create a new ConversationMemory instance with default settings.
    
    Args:
        context_turns: Number of turns to keep in active context
        
    Returns:
        ConversationMemory instance
    """
    return ConversationMemory(max_context_turns=context_turns)


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("ConversationMemory Demo")
    print("=" * 60)
    print()
    
    memory = create_conversation_memory(context_turns=5)
    
    # Simulate conversation
    conversations = [
        ("안녕하세요! 날씨가 좋네요", "안녕하세요! 네, 정말 화창한 날씨예요. 기분이 좋아지네요.", "hopeful", ["weather"], "ko"),
        ("오늘 뭐 할까요?", "산책하거나 책 읽는 건 어떨까요?", "curious", ["activities"], "ko"),
        ("좋아요, 책 추천해주세요", "최근 읽은 시집 중에 좋은 게 있어요. 관심 있으세요?", "focused", ["books", "poetry"], "ko"),
        ("네, 궁금해요", "윤동주의 '하늘과 바람과 별과 시'를 추천드려요.", "joyful", ["poetry", "books"], "ko"),
    ]
    
    for user_msg, asst_msg, emotion, topics, lang in conversations:
        memory.add_turn(
            user_message=user_msg,
            assistant_message=asst_msg,
            assistant_emotion=emotion,
            topics=topics,
            language=lang,
            user_id="demo_user"
        )
    
    print("Context Summary:")
    print(memory.get_context_string(format_style="emotional"))
    print()
    
    print("Emotional Arc:", memory.get_emotional_arc())
    print("Dominant Topics:", memory.get_dominant_topics())
    print()
    
    print("Memory Summary:")
    import json
    print(json.dumps(memory.get_summary(), indent=2, ensure_ascii=False))
