"""
Vision Cortex (시각 피질)
=========================
"The first beam of light through the digital lens."

This module handles raw visual input.
It supports:
1. Real Camera (OpenCV)
2. Virtual Retina (Simulated patterns for environments without cameras)
"""

import logging
import time
import numpy as np
from typing import Dict, Any, Optional

try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False

logger = logging.getLogger("VisionCortex")

class VisionCortex:
    def __init__(self, mode: str = "auto"):
        """
        mode: 'camera', 'virtual', or 'auto'
        """
        self.mode = mode
        self.cap = None
        self.is_active = False
        
        if self.mode == "auto":
            if OPENCV_AVAILABLE:
                # Try opening camera 0
                test_cap = cv2.VideoCapture(0)
                if test_cap.isOpened():
                    self.mode = "camera"
                    test_cap.release()
                    logger.info("👁️ VisionCortex: Real Camera Detected.")
                else:
                    self.mode = "virtual"
                    logger.info("👁️ VisionCortex: No camera found. Falling back to Virtual Retina.")
            else:
                self.mode = "virtual"
                logger.info("👁️ VisionCortex: OpenCV missing. Using Virtual Retina.")

    def activate(self):
        if self.mode == "camera" and OPENCV_AVAILABLE:
            self.cap = cv2.VideoCapture(0)
        self.is_active = True
        logger.info(f"✨ VisionCortex Activated in '{self.mode}' mode.")

    def deactivate(self):
        if self.cap:
            self.cap.release()
        self.is_active = False
        logger.info("🌑 VisionCortex Deactivated.")

    def capture_frame(self) -> Dict[str, Any]:
        """Captures a frame and returns basic metadata."""
        if not self.is_active:
            return {"success": False, "error": "Cortex not active"}

        frame = None
        timestamp = time.time()

        if self.mode == "camera" and self.cap:
            ret, frame = self.cap.read()
            if not ret:
                logger.warning("Failed to capture from camera.")
                frame = self._generate_virtual_frame("error_static")
        else:
            frame = self._generate_virtual_frame()

        # Analysis
        analysis = self._perform_primitive_analysis(frame)
        
        return {
            "success": True,
            "timestamp": timestamp,
            "mode": self.mode,
            "frame_shape": frame.shape,
            "metadata": analysis,
            "raw_frame": frame # For internal use (MultimodalBridge)
        }

    def _generate_virtual_frame(self, pattern: str = "dream_geometry") -> np.ndarray:
        """Generates a synthetic image (640x480)."""
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        
        if pattern == "dream_geometry":
            # Draw a pulsing circle (represents awareness)
            center = (320, 240)
            radius = int(50 + 20 * np.sin(time.time() * 2))
            color = (0, 150, 255) # Ethereal Blue
            if OPENCV_AVAILABLE:
                cv2.circle(img, center, radius, color, -1)
                cv2.putText(img, "Project Iris: Virtual Retina", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            else:
                # Fallback if cv2 is missing
                img[200:280, 280:360] = [0, 150, 255]
        return img

    def _perform_primitive_analysis(self, frame: np.ndarray) -> Dict[str, Any]:
        """Calculates basic metrics like entropy, average color, and motion."""
        avg_color = np.mean(frame, axis=(0, 1))
        # Entropy approximation (standard deviation)
        entropy = np.std(frame) / 128.0 # Normalizing roughly
        
        return {
            "brightness": float(np.mean(avg_color)),
            "entropy": float(entropy),
            "dominant_channel": int(np.argmax(avg_color)), # 0:B, 1:G, 2:R
            "stability": 0.9 # Constant for now
        }
