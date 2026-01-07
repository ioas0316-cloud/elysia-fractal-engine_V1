"""
Test Meta-Cognition (The Third Eye)
===================================
Verifies the resurrection of the GlobalObserver architecture.

Scenario:
1. Ignite the Unified Field.
2. Awaken the Global Observer.
3. Inject a 'Logic' wave (Red) but omit 'Emotion' (Blue).
4. Verify that VoidSensor detects the missing 'Emotion'.
5. Touch the filesystem (Simulated).
6. Verify that GlobalObserver feels the Somatic Wave.
"""

import sys
import os
import time
sys.path.insert(0, r"c:\Elysia")

from Core.Foundation.unified_field import UnifiedField, HyperQuaternion
from Core.Intelligence.Meta.global_observer import GlobalObserver
from Core.System.System.filesystem_wave import FileWaveEvent, FileEventType

def test_third_eye():
    print("\n👁️  INITIATING META-COGNITION TEST 👁️")
    print("========================================")
    
    # 1. Ignite Field
    field = UnifiedField()
    observer = GlobalObserver(field)
    print("✅ Global Observer Awakened.")
    
    # 2. Inject Unbalanced Thoughts (Logic Only)
    print("\n🌊 Injecting Logic Waves (450Hz)...")
    logic_wave = field.create_wave_packet(
        source_id="TestLogic",
        frequency=450.0, # Logic Band
        amplitude=0.8,
        phase=0.0,
        position=HyperQuaternion(1,0,0,0)
    )
    field.inject_wave(logic_wave)
    field.propagate(0.1)
    
    # 3. Observe and Detect Void
    print("\n🔍 Observing Field...")
    observer.observe(0.1)
    
    # Check for Voids
    voids = observer.active_alerts
    if voids:
        print(f"✅ Void Sensor Active! Detected {len(voids)} voids.")
        for v in voids:
            print(f"   - 🕳️  {v.message} (Severity: {v.severity:.2f})")
            
        # Verify 'Emotion' is missing
        emotion_void = next((v for v in voids if v.missing_dimension == "Emotion"), None)
        if emotion_void:
            print("   ✨ SUCCESS: Effectively detected absence of Emotion.")
        else:
            print("   ❌ FAILURE: Did not detect missing Emotion.")
    else:
        print("❌ FAILURE: Void Sensor found nothing (Should have found voids).")

    # 4. Somatic Test
    print("\n⚡ Testing Somatic Awareness (Filesystem Touch)...")
    # Simulate a file change event manually to avoid waiting for actual FS
    mock_event = FileWaveEvent(
        path="c:\\Elysia\\Core\\test_body.py",
        event_type=FileEventType.MODIFIED,
        frequency=852.0, # High freq code
        amplitude=1.0,
        metadata={}
    )
    observer.on_body_change(mock_event)
    
    # Check if wave was injected
    somatic_wave = next((w for w in field.active_waves if w.source_id == "Soma"), None)
    if somatic_wave:
        print(f"✅ SUCCESS: Body sensation registered in Mind at {somatic_wave.frequency}Hz")
    else:
        print("❌ FAILURE: Body sensation not felt in Field.")

    print("\n🎉 META-COGNITION TEST COMPLETE.")

if __name__ == "__main__":
    test_third_eye()
