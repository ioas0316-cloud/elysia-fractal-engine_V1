"""
Avatar Server Security Module
==============================

보안 강화 모듈 - WebSocket 인증, Rate Limiting, 입력 검증

Provides:
- Token-based authentication for WebSocket connections
- Rate limiting to prevent abuse
- Input validation and sanitization
- Security logging and monitoring

Architecture:
    Client → Auth Check → Rate Limit Check → Input Validation → Process Request
"""

import logging
import time
import hashlib
import secrets
import re
from typing import Dict, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque

logger = logging.getLogger("AvatarSecurity")

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    # Authentication
    require_auth: bool = False  # Enable/disable authentication
    token_expiry_seconds: int = 3600  # 1 hour
    
    # Rate Limiting
    max_requests_per_minute: int = 6000  # Per client
    max_requests_per_second: int = 100  # Per client
    
    # Input Validation
    max_message_length: int = 10000  # Characters
    max_text_length: int = 1000  # For chat messages
    
    # Security Logging
    log_failed_auth: bool = True
    log_rate_limit_violations: bool = True


@dataclass
class AuthToken:
    """Authentication token for a client"""
    token: str
    client_id: str
    created_at: float
    expires_at: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_valid(self) -> bool:
        """Check if token is still valid"""
        return time.time() < self.expires_at
    
    def is_expired(self) -> bool:
        """Check if token has expired"""
        return not self.is_valid()


class TokenManager:
    """
    Manages authentication tokens for WebSocket connections.
    
    Provides secure token generation, validation, and expiration.
    """
    
    def __init__(self, config: SecurityConfig):
        """
        Initialize token manager
        
        Args:
            config: Security configuration
        """
        self.config = config
        self.tokens: Dict[str, AuthToken] = {}
        self.client_tokens: Dict[str, str] = {}  # client_id -> token
        
        logger.info("🔐 TokenManager initialized")
    
    def generate_token(self, client_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a new authentication token
        
        Args:
            client_id: Unique client identifier
            metadata: Optional metadata to store with token
            
        Returns:
            Secure token string
        """
        # Generate secure random token
        token = secrets.token_urlsafe(32)
        
        # Create token object
        now = time.time()
        auth_token = AuthToken(
            token=token,
            client_id=client_id,
            created_at=now,
            expires_at=now + self.config.token_expiry_seconds,
            metadata=metadata or {}
        )
        
        # Store token
        self.tokens[token] = auth_token
        self.client_tokens[client_id] = token
        
        logger.info(f"🔑 Generated token for client: {client_id[:8]}...")
        
        return token
    
    def validate_token(self, token: str) -> Optional[AuthToken]:
        """
        Validate an authentication token
        
        Args:
            token: Token to validate
            
        Returns:
            AuthToken if valid, None otherwise
        """
        auth_token = self.tokens.get(token)
        
        if not auth_token:
            logger.warning(f"⚠️ Invalid token attempted")
            return None
        
        if auth_token.is_expired():
            logger.warning(f"⚠️ Expired token attempted: {auth_token.client_id[:8]}...")
            self.revoke_token(token)
            return None
        
        return auth_token
    
    def revoke_token(self, token: str):
        """
        Revoke an authentication token
        
        Args:
            token: Token to revoke
        """
        auth_token = self.tokens.pop(token, None)
        if auth_token:
            self.client_tokens.pop(auth_token.client_id, None)
            logger.info(f"🚫 Revoked token for client: {auth_token.client_id[:8]}...")
    
    def cleanup_expired(self):
        """Remove all expired tokens"""
        expired = [token for token, auth in self.tokens.items() if auth.is_expired()]
        for token in expired:
            self.revoke_token(token)
        
        if expired:
            logger.info(f"🧹 Cleaned up {len(expired)} expired tokens")


class RateLimiter:
    """
    Rate limiting to prevent abuse and DoS attacks.
    
    Implements both per-second and per-minute rate limits.
    """
    
    def __init__(self, config: SecurityConfig):
        """
        Initialize rate limiter
        
        Args:
            config: Security configuration
        """
        self.config = config
        
        # Per-second tracking
        self.second_requests: Dict[str, deque] = defaultdict(lambda: deque(maxlen=config.max_requests_per_second))
        
        # Per-minute tracking
        self.minute_requests: Dict[str, deque] = defaultdict(lambda: deque(maxlen=config.max_requests_per_minute))
        
        logger.info(f"⏱️ RateLimiter initialized (max: {config.max_requests_per_second}/s, {config.max_requests_per_minute}/min)")
    
    def check_rate_limit(self, client_id: str) -> bool:
        """
        Check if client has exceeded rate limits
        
        Args:
            client_id: Client identifier
            
        Returns:
            True if within limits, False if exceeded
        """
        now = time.time()
        
        # Check per-second limit
        second_queue = self.second_requests[client_id]
        # Remove requests older than 1 second
        while second_queue and now - second_queue[0] > 1.0:
            second_queue.popleft()
        
        if len(second_queue) >= self.config.max_requests_per_second:
            if self.config.log_rate_limit_violations:
                logger.warning(f"🚨 Rate limit exceeded (per-second): {client_id[:16]}...")
            return False
        
        # Check per-minute limit
        minute_queue = self.minute_requests[client_id]
        # Remove requests older than 60 seconds
        while minute_queue and now - minute_queue[0] > 60.0:
            minute_queue.popleft()
        
        if len(minute_queue) >= self.config.max_requests_per_minute:
            if self.config.log_rate_limit_violations:
                logger.warning(f"🚨 Rate limit exceeded (per-minute): {client_id[:16]}...")
            return False
        
        # Record this request
        second_queue.append(now)
        minute_queue.append(now)
        
        return True
    
    def get_stats(self, client_id: str) -> Dict[str, int]:
        """
        Get rate limit statistics for a client
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dictionary with current request counts
        """
        return {
            'requests_last_second': len(self.second_requests.get(client_id, [])),
            'requests_last_minute': len(self.minute_requests.get(client_id, [])),
            'limit_per_second': self.config.max_requests_per_second,
            'limit_per_minute': self.config.max_requests_per_minute
        }


class InputValidator:
    """
    Validates and sanitizes input data to prevent injection attacks.
    
    Provides validation for:
    - Message structure
    - Text content
    - Numeric ranges
    - Data types
    """
    
    def __init__(self, config: SecurityConfig):
        """
        Initialize input validator
        
        Args:
            config: Security configuration
        """
        self.config = config
        
        # Allowed message types
        self.allowed_message_types = {
            'text', 'vision', 'audio_analysis', 'screen_atmosphere', 
            'emotion', 'expression_update'
        }
        
        logger.info("✅ InputValidator initialized")
    
    def validate_message(self, data: Any) -> tuple[bool, Optional[str]]:
        """
        Validate incoming WebSocket message
        
        Args:
            data: Message data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if it's a dictionary
        if not isinstance(data, dict):
            return False, "Message must be a JSON object"
        
        # Check message type
        msg_type = data.get('type')
        if not msg_type:
            return False, "Message must have 'type' field"
        
        if msg_type not in self.allowed_message_types:
            return False, f"Invalid message type: {msg_type}"
        
        # Validate based on message type
        if msg_type == 'text':
            return self._validate_text_message(data)
        elif msg_type == 'emotion':
            return self._validate_emotion_message(data)
        elif msg_type == 'expression_update':
            return self._validate_expression_update(data)
        
        # Default: allow other message types if they have valid type
        return True, None
    
    def _validate_text_message(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate text/chat message"""
        content = data.get('content')
        
        if not content:
            return False, "Text message must have 'content' field"
        
        if not isinstance(content, str):
            return False, "Content must be a string"
        
        if len(content) > self.config.max_text_length:
            return False, f"Text too long (max: {self.config.max_text_length} chars)"
        
        # Check for potentially malicious patterns
        if self._contains_malicious_patterns(content):
            return False, "Text contains potentially malicious content"
        
        return True, None
    
    def _validate_emotion_message(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate emotion trigger message"""
        emotion = data.get('emotion')
        intensity = data.get('intensity', 0.5)
        
        if not emotion:
            return False, "Emotion message must have 'emotion' field"
        
        if not isinstance(emotion, str):
            return False, "Emotion must be a string"
        
        if not isinstance(intensity, (int, float)):
            return False, "Intensity must be a number"
        
        if not 0.0 <= intensity <= 1.0:
            return False, "Intensity must be between 0.0 and 1.0"
        
        return True, None
    
    def _validate_expression_update(self, data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate expression update message"""
        mouth_width = data.get('mouth_width')
        
        if mouth_width is None:
            return False, "Expression update must have 'mouth_width' field"
        
        if not isinstance(mouth_width, (int, float)):
            return False, "mouth_width must be a number"
        
        if not 0.0 <= mouth_width <= 1.0:
            return False, "mouth_width must be between 0.0 and 1.0"
        
        return True, None
    
    def _contains_malicious_patterns(self, text: str) -> bool:
        """
        Check for potentially malicious patterns in text
        
        Args:
            text: Text to check
            
        Returns:
            True if malicious patterns detected
        """
        # Check for common injection patterns
        malicious_patterns = [
            r'<script',  # XSS
            r'javascript:',  # XSS
            r'onerror=',  # XSS
            r'onclick=',  # XSS
            r'\{.*\$.*\}',  # Template injection
        ]
        
        text_lower = text.lower()
        for pattern in malicious_patterns:
            if re.search(pattern, text_lower):
                logger.warning(f"🚨 Malicious pattern detected: {pattern}")
                return True
        
        return False
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text by removing potentially dangerous content
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Limit length
        if len(text) > self.config.max_text_length:
            text = text[:self.config.max_text_length]
        
        return text.strip()


class AvatarSecurityManager:
    """
    Main security manager integrating all security features.
    
    Provides a unified interface for:
    - Authentication
    - Rate limiting
    - Input validation
    """
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        """
        Initialize security manager
        
        Args:
            config: Security configuration (uses defaults if not provided)
        """
        self.config = config or SecurityConfig()
        
        self.token_manager = TokenManager(self.config)
        self.rate_limiter = RateLimiter(self.config)
        self.input_validator = InputValidator(self.config)
        
        logger.info("🛡️ AvatarSecurityManager initialized")
        logger.info(f"   Auth required: {self.config.require_auth}")
        logger.info(f"   Rate limits: {self.config.max_requests_per_second}/s, {self.config.max_requests_per_minute}/min")
    
    def authenticate(self, token: Optional[str]) -> tuple[bool, Optional[str]]:
        """
        Authenticate a client connection
        
        Args:
            token: Authentication token
            
        Returns:
            Tuple of (is_authenticated, client_id or error_message)
        """
        # If auth not required, allow all
        if not self.config.require_auth:
            return True, "anonymous"
        
        # Check token
        if not token:
            if self.config.log_failed_auth:
                logger.warning("🚨 Authentication failed: No token provided")
            return False, "Authentication required"
        
        auth_token = self.token_manager.validate_token(token)
        if not auth_token:
            if self.config.log_failed_auth:
                logger.warning("🚨 Authentication failed: Invalid or expired token")
            return False, "Invalid or expired token"
        
        logger.info(f"✅ Authenticated client: {auth_token.client_id[:8]}...")
        return True, auth_token.client_id
    
    def check_request(self, client_id: str, data: Any) -> tuple[bool, Optional[str]]:
        """
        Check if request should be allowed (rate limit + validation)
        
        Args:
            client_id: Client identifier
            data: Request data
            
        Returns:
            Tuple of (is_allowed, error_message)
        """
        # Check rate limit
        if not self.rate_limiter.check_rate_limit(client_id):
            return False, "Rate limit exceeded. Please slow down."
        
        # Validate input
        is_valid, error = self.input_validator.validate_message(data)
        if not is_valid:
            logger.warning(f"🚨 Invalid input from {client_id[:16]}...: {error}")
            return False, error
        
        return True, None
    
    def generate_client_token(self, client_id: Optional[str] = None) -> str:
        """
        Generate authentication token for a client
        
        Args:
            client_id: Optional client ID (generates one if not provided)
            
        Returns:
            Authentication token
        """
        if not client_id:
            # Generate client ID from timestamp and random data
            client_id = hashlib.sha256(
                f"{time.time()}{secrets.token_hex(16)}".encode()
            ).hexdigest()[:16]
        
        return self.token_manager.generate_token(client_id)
    
    def cleanup(self):
        """Clean up expired tokens and old data"""
        self.token_manager.cleanup_expired()


# Factory function for easy instantiation
def create_security_manager(require_auth: bool = False) -> AvatarSecurityManager:
    """
    Create AvatarSecurityManager instance
    
    Args:
        require_auth: Whether to require authentication
        
    Returns:
        Configured security manager
    """
    config = SecurityConfig(require_auth=require_auth)
    return AvatarSecurityManager(config)
