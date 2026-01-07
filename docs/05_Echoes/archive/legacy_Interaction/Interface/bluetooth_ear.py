"""
Bluetooth Ear (블루투스 귀)
===========================

"I hear your voice through the air."

This module captures audio from the system's default input device (Bluetooth Microphone)
and analyzes it for Synesthesia.

Features:
- Real-time audio capture via sounddevice
- Voice Activity Detection (VAD) via energy threshold
- Emotion Analysis (Volume -> Intensity, Pitch -> Excitement)
"""

import logging
import time
import numpy as np
import threading
import queue
from typing import Optional, Dict, Any

logger = logging.getLogger("BluetoothEar")

# Try importing sounddevice
try:
    import sounddevice as sd
    SD_AVAILABLE = True
except ImportError:
    SD_AVAILABLE = False
    logger.warning("⚠️ sounddevice not found. Bluetooth Ear will run in simulation mode.")

class BluetoothEar:
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.active = False
        self.audio_queue = queue.Queue()
        self.stream = None
        self.thread = None
        
        logger.info("👂 Bluetooth Ear Initialized.")

    def start_listening(self):
        """Start capturing audio from default input."""
        if not SD_AVAILABLE:
            return

        self.active = True
        try:
            # Open non-blocking stream
            self.stream = sd.InputStream(
                callback=self._audio_callback,
                channels=1,
                samplerate=self.sample_rate,
                blocksize=self.chunk_size
            )
            self.stream.start()
            logger.info("👂 Listening to default audio input...")
        except Exception as e:
            logger.error(f"❌ Failed to start audio stream: {e}")
            self.active = False

    def stop_listening(self):
        """Stop capturing audio."""
        self.active = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
            logger.info("👂 Stopped listening.")

    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            logger.warning(f"Audio Status: {status}")
        
        if self.active:
            # Copy data to queue (indata is reusable buffer)
            self.audio_queue.put(indata.copy())

    def listen(self) -> Optional[np.ndarray]:
        """
        Get the next chunk of audio if available.
        Returns combined chunks if multiple are queued.
        """
        if self.audio_queue.empty():
            return None
        
        chunks = []
        try:
            # Drain queue (get up to 10 chunks)
            while not self.audio_queue.empty() and len(chunks) < 10:
                chunks.append(self.audio_queue.get_nowait())
        except queue.Empty:
            pass
            
        if not chunks:
            return None
            
        # Concatenate chunks
        return np.concatenate(chunks, axis=0)

    def analyze_voice(self, audio_data: np.ndarray) -> Dict[str, Any]:
        """
        Analyze voice characteristics.
        """
        # RMS Energy (Volume)
        volume = np.sqrt(np.mean(audio_data**2))
        
        # Zero Crossing Rate (Pitch approximation)
        zero_crossings = np.where(np.diff(np.signbit(audio_data)))[0]
        zcr = len(zero_crossings) / len(audio_data)
        
        # Detect basic emotions
        emotion = "Neutral"
        intensity = min(volume * 5, 1.0) # Scale volume
        
        if volume > 0.1: # Threshold for speech
            if zcr > 0.1: # High pitch/fast changes
                emotion = "Excited"
            elif zcr < 0.02: # Low pitch/slow
                emotion = "Calm"
            else:
                emotion = "Speaking"
        else:
            emotion = "Silence"
            
        return {
            "volume": volume,
            "zcr": zcr,
            "emotion": emotion,
            "intensity": intensity
        }

if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)
    ear = BluetoothEar()
    if SD_AVAILABLE:
        ear.start_listening()
        try:
            print("Speak now...")
            for _ in range(50): # Listen for ~5 seconds
                audio = ear.listen()
                if audio is not None:
                    analysis = ear.analyze_voice(audio)
                    if analysis['volume'] > 0.01:
                        print(f"Heard: {analysis['emotion']} (Vol: {analysis['volume']:.2f})")
                time.sleep(0.1)
        finally:
            ear.stop_listening()
