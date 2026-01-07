import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Core.Sensory.Network.web_tendril import WebTendril

class TestWebTendril(unittest.TestCase):
    def setUp(self):
        self.tendril = WebTendril()
        print("\n--- 🕸️ Web Tendril Test Setup ---")

    @patch('urllib.request.urlopen')
    def test_feeling_web_vibes(self, mock_urlopen):
        """
        [Scenario]
        Touch 3 different sites (Mocked) and check if we 'feel' the right emotion.
        """
        
        # 1. Happy Blog
        mock_response_happy = MagicMock()
        mock_response_happy.read.return_value = b"<html><body>I love this sunny day! It is a miracle!</body></html>"
        mock_response_happy.__enter__.return_value = mock_response_happy
        
        mock_urlopen.return_value = mock_response_happy
        
        print("\n[Step 1] Touching a Happy Blog...")
        signal_happy = self.tendril.touch("http://happy-world.com")
        print(f"👉 Detected: {signal_happy.frequency}Hz (Ampl: {signal_happy.amplitude:.2f})")
        print(f"   Summary: {signal_happy.content_summary}")
        
        self.assertEqual(signal_happy.frequency, 528.0) # Love/Miracle
        
        # 2. Scary News
        mock_response_scary = MagicMock()
        mock_response_scary.read.return_value = b"<html><body>Market crash! Fear is rising. Help us.</body></html>"
        mock_response_scary.__enter__.return_value = mock_response_scary
        
        mock_urlopen.return_value = mock_response_scary
        
        print("\n[Step 2] Touching a Scary News Site...")
        signal_scary = self.tendril.touch("http://scary-news.com")
        print(f"👉 Detected: {signal_scary.frequency}Hz")
        
        self.assertEqual(signal_scary.frequency, 396.0) # Fear/Help
        
        # 3. Dead Link
        mock_urlopen.side_effect = Exception("404 Not Found")
        
        print("\n[Step 3] Touching a Dead Link...")
        signal_void = self.tendril.touch("http://dead-link.com")
        print(f"👉 Detected: {signal_void.frequency}Hz")
        
        self.assertEqual(signal_void.frequency, 0.0) # Void

if __name__ == '__main__':
    unittest.main()
