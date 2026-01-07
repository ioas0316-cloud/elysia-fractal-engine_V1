"""
VideoComposer (비디오 작곡가)
===========================

"Motion is life."

This module creates .mp4 video files from images using OpenCV.
Note: OpenCV cannot handle audio easily, so this generates silent video.
"""

import cv2
import os
import numpy as np

class VideoComposer:
    def __init__(self, fps: int = 30):
        self.fps = fps
        print("🎬 VideoComposer Initialized. Camera rolling...")

    def create_static_video(self, image_path: str, output_file: str, duration: float = 10.0):
        """
        Creates a video from a single static image.
        """
        print(f"🎥 Rendering Video: {output_file} ({duration}s)")
        
        if not os.path.exists(image_path):
            print(f"⚠️ Image not found: {image_path}")
            return

        # Read Image
        img = cv2.imread(image_path)
        height, width, layers = img.shape
        size = (width, height)
        
        # Initialize Video Writer (mp4v codec)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, self.fps, size)
        
        # Write frames
        num_frames = int(duration * self.fps)
        for _ in range(num_frames):
            out.write(img)
            
        out.release()
        print(f"✅ Video Saved: {output_file}")

if __name__ == "__main__":
    # Test
    composer = VideoComposer()
    # Create a dummy image for testing
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    dummy_img[:] = (255, 0, 0) # Blue
    cv2.imwrite("test_blue.png", dummy_img)
    
    composer.create_static_video("test_blue.png", "test_video.mp4", duration=3.0)
