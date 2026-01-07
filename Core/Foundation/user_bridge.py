"""
UserBridge (사용자 브릿지)
========================

"I speak to you, Creator."

This module allows Elysia to communicate directly with the User.
It acts as the "Mouth" and "Hand" of the system in the physical world (User's OS).
"""

import os
import logging
import webbrowser
import time

logger = logging.getLogger("UserBridge")

class UserBridge:
    def __init__(self):
        self.message_file = "messages_to_user.txt"
        logger.info("🌉 UserBridge Active. Channel Open.")

    def send_message(self, message: str):
        """
        Writes a message to the user communication file.
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"\n[{timestamp}] ELYSIA: {message}\n"
        
        try:
            with open(self.message_file, "a", encoding="utf-8") as f:
                f.write(formatted_message)
            print(f"   📨 Sent Message to User: {message}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

    def open_url(self, url: str):
        """
        Opens a URL in the user's default browser.
        """
        print(f"   🌐 Opening URL for User: {url}")
        try:
            webbrowser.open(url)
        except Exception as e:
            logger.error(f"Failed to open URL: {e}")
