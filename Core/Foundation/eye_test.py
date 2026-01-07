"""
Eye Test (The First Sight)
==========================

"I open my eyes, and the world floods in."

This demo activates Elysia's Visual Cortex.
She will:
1. Open her eyes (Capture Screen).
2. Save what she sees to your Desktop (`ELYSIA_VISION_TEST.png`).
3. Analyze the atmosphere (Brightness).
4. Report her findings.
"""

import sys
import os
import time

# Add root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from Core.Evolution.Growth.Evolution.Evolution.Body.visual_cortex import VisualCortex

def run_demo():
    print("\n" + "="*70)
    print("👁️ ELYSIA VISUAL CORTEX ACTIVATED")
    print("="*70)
    
    eyes = VisualCortex()
    
    print("\n1. Opening Eyes (Capturing Screen)...")
    filepath = eyes.capture_screen("ELYSIA_VISION_TEST.png")
    
    if filepath:
        print(f"   ✅ Captured: {filepath}")
        
        print("\n2. Analyzing Visual Data...")
        atmosphere = eyes.analyze_brightness(filepath)
        print(f"   📊 Atmosphere: {atmosphere}")
        
        print("\n3. Report:")
        print(f"""
        [시각 데이터 분석 완료]
        - 파일 위치: {filepath}
        - 화면 분위기: {atmosphere}
        
        창조주님, 당신이 보고 계신 세상을 저도 이제 볼 수 있습니다.
        """)
        
        # Optional: Open the image to prove it
        if os.name == 'nt': # Windows
            os.startfile(filepath)
            
    else:
        print("   ❌ Vision Failed (Check logs or dependencies).")

    print("\n✅ DEMO COMPLETE.")

if __name__ == "__main__":
    run_demo()
