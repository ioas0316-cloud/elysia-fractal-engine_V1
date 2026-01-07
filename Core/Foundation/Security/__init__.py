"""
Elysia Security Module (엘리시아 보안 모듈)
========================================

This module provides comprehensive security and protection for the Elysia system.

Components:
- network_shield: Network-level threat detection and protection
- (Future) intrusion_detection: Advanced intrusion detection system
- (Future) encryption: Data protection and encryption services
"""

from .network_shield import (
    NetworkShield,
    NetworkEvent,
    ThreatType,
    ActionType,
    FrequencyAnalyzer,
    PatternRecognizer,
)

__all__ = [
    "NetworkShield",
    "NetworkEvent", 
    "ThreatType",
    "ActionType",
    "FrequencyAnalyzer",
    "PatternRecognizer",
]
