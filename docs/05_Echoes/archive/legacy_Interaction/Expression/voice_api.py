"""
Voice API Integration for Web Server
====================================

Adds voice conversation endpoints to the visualizer server.
This connects the IntegratedVoiceSystem to the web interface.
"""

import json
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Core.Interaction.Expression.voice_of_elysia import VoiceOfElysia

logger = logging.getLogger("VoiceAPI")

# Global reference to voice system (set by server)
_voice_system: 'VoiceOfElysia' = None

def set_voice_system(voice: 'VoiceOfElysia'):
    """Set the voice system reference"""
    global _voice_system
    _voice_system = voice
    logger.info("✅ Voice system connected to API")

def handle_voice_request(request_data: dict) -> dict:
    """
    Handle voice conversation request.
    
    Args:
        request_data: {
            "text": "user input text"
        }
    
    Returns:
        {
            "response": "elysia response",
            "status": "ok/error",
            "voice_status": {...}
        }
    """
    if not _voice_system:
        return {
            "response": "Voice system not initialized",
            "status": "error"
        }
    
    try:
        user_text = request_data.get("text", "")
        if not user_text:
            return {
                "response": "No input provided",
                "status": "error"
            }
        
        # Process through full cognitive cycle
        logger.info(f"📥 Voice input: {user_text}")
        response = _voice_system.process_text_input(user_text)
        logger.info(f"📤 Voice output: {response}")
        
        return {
            "response": response,
            "status": "ok",
            "voice_status": _voice_system.get_voice_status()
        }
    
    except Exception as e:
        logger.error(f"Voice request error: {e}")
        return {
            "response": f"Error: {str(e)}",
            "status": "error"
        }

def get_voice_status() -> dict:
    """Get current voice system status"""
    if not _voice_system:
        return {"available": False}
    
    return {
        "available": True,
        **_voice_system.get_voice_status()
    }
