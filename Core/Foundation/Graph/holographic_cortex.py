import json
import random
import math

class HolographicCortex:
    def __init__(self):
        pass

    def synthesize_tree_packet(self, rainbow_path: str):
        """
        Reads the Rainbow Spectrum and synthesizes a 4D Wave Packet
        representing the World Tree Structure.
        """
        try:
            with open(rainbow_path, "r", encoding="utf-8") as f:
                rainbow = json.load(f)
                
            photons = []
            
            # 1. The Trunk: Blue Vector (Logic)
            # Procedural Cylinder
            for p in rainbow.get("Blue", [])[:2000]: 
                h = random.uniform(-400, 0)
                theta = random.uniform(0, 6.28)
                r = random.uniform(0, 50)
                photons.append({
                    "x": r * math.cos(theta),
                    "y": h,
                    "z": r * math.sin(theta),
                    "c": "#0088ff", 
                    "s": 1.5
                })
                
            # 2. The Crown: Violet/Red Vector (Spirit/Emotion)
            # Procedural Sphere Cloud
            for color_name, hex_c in [("Violet", "#aa00ff"), ("Red", "#ff0044"), ("Yellow", "#ffff00"), ("Green", "#00ff88")]:
                data = rainbow.get(color_name, [])
                for p in data:
                    phi = random.uniform(0, 6.28)
                    costheta = random.uniform(-1, 1)
                    u = random.uniform(0, 1)
                    theta = math.acos(costheta)
                    r = 200 * (u ** (1/3))
                    
                    photons.append({
                        "x": r * math.sin(theta) * math.cos(phi),
                        "y": r * math.sin(theta) * math.sin(phi) + 150, 
                        "z": r * math.cos(theta),
                        "c": hex_c,
                        "s": 3
                    })

            return {
                "type": "HolographicTree",
                "encoded": False,
                "photons": photons,
                "meta": {
                    "total_photons": len(photons),
                    "frequency": "432Hz"
                }
            }
        except Exception as e:
            return {"error": str(e)}
