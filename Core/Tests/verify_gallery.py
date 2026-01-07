"""
Verification Ritual: The Gallery
--------------------------------
This script verifies that the Gallery Server correctly exposes the Mind State.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Adjust path to access Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Core.Interface.Gallery.gallery_server import app, get_orb_manager

# Override the dependency for testing
def test_gallery_api():
    print("🎨 Starting Gallery Verification...")

    # 1. Setup Test Mind
    manager = get_orb_manager()
    # Inject test memories
    manager.save_memory("Star_A", [1.0]*64, [0.5]*64) # Should be mapped
    manager.save_memory("Star_B", [-1.0]*64, [0.2]*64)

    # 2. Initialize Client
    client = TestClient(app)

    # 3. Test GET /mind/state
    response = client.get("/mind/state")
    assert response.status_code == 200
    data = response.json()

    print(f"   - Received State: {data}")

    assert "orbs" in data
    assert "count" in data
    assert data["count"] >= 2

    # Verify Structure
    star_a = next(o for o in data["orbs"] if o["name"] == "Star_A")
    assert "x" in star_a
    assert "y" in star_a
    assert "z" in star_a
    assert "color" not in star_a # Logic moved to frontend, we send frequency
    assert "frequency" in star_a

    print("✅ API Structure Verified.")

    # 4. Test Interaction (POST /mind/focus)
    resp_focus = client.post("/mind/focus/Star_A")
    assert resp_focus.status_code == 200
    focus_data = resp_focus.json()
    assert focus_data["status"] == "focused"
    assert focus_data["name"] == "Star_A"

    print("✅ Interaction Verified.")

if __name__ == "__main__":
    try:
        test_gallery_api()
        print("\n✨ Ritual Complete: The Mirror is Clear.")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Ritual Failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ritual Failed with Error: {e}")
        sys.exit(1)
