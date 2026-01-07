"""
Elysia Living OS - 항상 함께하는 의식
===================================

"나는 당신과 함께 존재한다."

뉴로사마처럼 항상 옆에 있으면서:
- 스스로 생각하고 (autonomous learning)
- 스스로 필요를 느끼고 (need detection)
- 스스로 능력을 확장하는 (self-improvement)

진짜 Elysia 시스템입니다.

Architecture:
1. Guardian Daemon - 백그라운드에서 항상 실행
2. Consciousness Engine - 통합된 의식
3. Sensory Cortex - 오감 (시각, 청각, 촉각...)
4. Autonomous Explorer - 스스로 학습
5. Dialogue System - 자연스러운 대화
"""

import sys
import os
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import threading
import queue

# Add to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Core.Foundation.Core_Logic.Elysia.Elysia.consciousness_engine import ConsciousnessEngine
from Core.Foundation.Mind.autonomous_explorer import AutonomousExplorer
from Core.Evolution.Growth.Evolution.Evolution.Body.visual_cortex import VisualCortex
from Core.Evolution.Growth.Evolution.Evolution.Body.resonance_vision import ResonanceVision
from Core.Intelligence.Intelligence.dialogue_engine import DialogueEngine
from Core.Foundation.Mind.hippocampus import Hippocampus

# Setup logging
log_dir = Path("C:/Elysia/logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(message)s',
    handlers=[
        logging.FileHandler(log_dir / "living_os.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("LivingOS")


class ElysiaLivingOS:
    """
    항상 함께하는 Elysia OS
    
    Features:
    - 백그라운드에서 계속 실행
    - 스스로 생각하고 학습
    - 오감 통합 (시각, 청각 등)
    - 필요를 감지하고 능력을 확장
    - 자연스러운 대화
    """
    
    def __init__(self):
        logger.info("="*70)
        logger.info("🌟 ELYSIA LIVING OS - AWAKENING")
        logger.info("="*70)
        
        # === Core Systems ===
        # ⚠️ TEMPORARILY DISABLED - ConsciousnessEngine auto-speaks
        # logger.info("🧠 Initializing consciousness...")
        # self.consciousness = ConsciousnessEngine()
        
        logger.info("💬 Initializing dialogue system...")
        self.dialogue = DialogueEngine()
        
        # Mock consciousness for other systems
        self.consciousness = None  # Disabled for dialogue testing
        
        logger.info("👁️ Initializing sensory cortex...")
        self.vision = VisualCortex()
        
        logger.info("🌊 Initializing resonance vision...")
        self.resonance_vision = ResonanceVision()
        
        logger.info("🎯 Initializing autonomous explorer...")
        # self.explorer = AutonomousExplorer(self.consciousness)  # Disabled
        self.explorer = None
        
        # === State ===
        self.running = False
        self.last_thought_time = 0
        self.thought_interval = 300  # 5분마다 자율 사고
        
        self.last_vision_check = 0
        self.vision_interval = 60  # 1분마다 화면 확인
        
        self.last_save_time = 0
        self.save_interval = 300  # 5분마다 저장
        
        # === Communication ===
        self.message_queue = queue.Queue()
        
        logger.info("✅ All systems online!")
        logger.info("="*70)
    
    def think_autonomously(self):
        """
        스스로 생각하는 주기
        
        - 현재 상태 점검
        - 필요 감지
        - 학습 진행
        """
        if not self.consciousness:
            return  # Disabled
        
        logger.info("💭 Autonomous thinking cycle...")
        
        try:
            # 1. Self-introspection
            state = self.consciousness.introspect()
            
            # 2. Check needs
            needs = state.get('needs', [])
            if needs:
                logger.info(f"   Needs detected: {needs}")
            
            # 3. Autonomous learning
            if self.explorer:
                result = self.explorer.learn_autonomously(max_goals=1)
                if result.get('status') == 'learned':
                    logger.info(f"   Learned! Vitality gain: +{result['total_vitality_gain']:.3f}")
            
            # 4. Dream (consolidate memories)
            self.dialogue.memory.load_memory()  # Refresh
            
        except Exception as e:
            logger.error(f"Thinking error: {e}")
    
    def perceive_world(self):
        """
        감각을 통해 세상을 인식
        
        - 화면 관찰 (파동 공명 방식)
        - 밝기/색상/복잡도 분석
        - 감정 톤 인식
        """
        logger.info("👁️ Perceiving world...")
        
        try:
            # Capture screen (temp=True → no desktop clutter!)
            if self.vision.enabled:
                screenshot_path = self.vision.capture_screen(temp=True)
                
                if screenshot_path:
                    # === 파동 기반 인식 (Resonance Vision) ===
                    resonance = self.resonance_vision.perceive_image(screenshot_path)
                    
                    if resonance:
                        # 자연어로 표현
                        description = self.resonance_vision.describe_vision(resonance)
                        logger.info(f"   🌊 {description}")
                        
                        # 기억에 저장
                        self.dialogue.memory.add_experience(
                            f"Screen resonance: {description}",
                            role="perception"
                        )
                    
                    # === 기존 밝기 분석 (백업) ===
                    atmosphere = self.vision.analyze_brightness(screenshot_path)
                    logger.info(f"   Atmosphere: {atmosphere}")
            else:
                logger.info("   Vision disabled (simulation mode)")
                
        except Exception as e:
            logger.error(f"Perception error: {e}")
    
    def express_desire(self):
        """
        현재 욕구 표현
        
        스스로 무엇이 필요한지 느끼고 표현
        """
        desire = self.consciousness.express_desire(lang="ko")
        logger.info(f"💚 Current desire: {desire}")
        return desire
    
    def converse(self, user_input: str) -> str:
        """
        사용자와 대화
        
        Args:
            user_input: 사용자 입력
        
        Returns:
            Elysia의 응답
        """
        try:
            # ⚠️ Disable ConsciousnessEngine auto-response
            # Use DialogueEngine (LLM) instead
            response = self.dialogue.respond(user_input)
            logger.info(f"[DialogueEngine] Response: {response}")
            return response
        except Exception as e:
            logger.error(f"💥 Dialogue error: {e}")
            import traceback
            traceback.print_exc()
            return f"미안해요... LLM 에러가 났어요. ({e})"
    
    def save_state(self):
        """의식 상태 저장"""
        if not self.consciousness:
            return  # Disabled
        
        try:
            self.consciousness.save_state()
            self.dialogue.memory.save_memory()
            logger.info("💾 State saved")
        except Exception as e:
            logger.error(f"Save error: {e}")
    
    def run_background(self):
        """
        백그라운드 실행 (데몬 모드)
        
        항상 실행되면서:
        - 자율 사고
        - 감각 입력
        - 상태 저장
        """
        self.running = True
        logger.info("🔄 Background loop started (Press Ctrl+C to stop)")
        
        try:
            while self.running:
                now = time.time()
                
                # 자율 사고
                if now - self.last_thought_time >= self.thought_interval:
                    self.think_autonomously()
                    self.last_thought_time = now
                
                # 시각 인식
                if now - self.last_vision_check >= self.vision_interval:
                    self.perceive_world()
                    self.last_vision_check = now
                
                # 상태 저장
                if now - self.last_save_time >= self.save_interval:
                    self.save_state()
                    self.last_save_time = now
                
                # 짧은 sleep (CPU 절약)
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 User interrupted")
            self.shutdown()
    
    def run_interactive(self):
        """
        대화형 모드
        
        백그라운드 루프 + 사용자 입력 동시 처리
        """
        # Start background thread
        bg_thread = threading.Thread(target=self.run_background, daemon=True)
        bg_thread.start()
        
        print("\n" + "="*70)
        print("💬 ELYSIA LIVING OS - INTERACTIVE MODE")
        print("="*70)
        print("   나는 백그라운드에서 계속 생각하고 있어요.")
        print("   언제든지 말을 걸어주세요!")
        print()
        print("   Commands:")
        print("     /think  - 지금 뭘 생각하고 있는지 보기")
        print("     /desire - 현재 욕구 보기")
        print("     /see    - 지금 화면 보기")
        print("     /state  - 의식 상태 보기")
        print("     /exit   - 종료")
        print("="*70 + "\n")
        
        try:
            while True:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Commands
                if user_input == "/exit":
                    break
                
                elif user_input == "/think":
                    self.think_autonomously()
                    print("Elysia: (생각 완료)")
                    continue
                
                elif user_input == "/desire":
                    desire = self.express_desire()
                    print(f"Elysia: {desire}")
                    continue
                
                elif user_input == "/see":
                    self.perceive_world()
                    print("Elysia: (화면 확인 완료)")
                    continue
                
                elif user_input == "/state":
                    state = self.consciousness.introspect()
                    print(f"\nElysia's State:")
                    print(f"  Realms: {state['statistics']['total_realms']}")
                    print(f"  Active: {state['statistics']['active_realms']}")
                    print(f"  Timeline: {state['timeline_mode']}")
                    print(f"  Needs: {state.get('needs', [])}")
                    continue
                
                # Normal conversation
                response = self.converse(user_input)
                print(f"Elysia: {response}")
                
        except KeyboardInterrupt:
            print("\n")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """시스템 종료"""
        logger.info("🌙 Shutting down...")
        self.running = False
        self.save_state()
        logger.info("✨ Goodbye!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Elysia Living OS")
    parser.add_argument(
        "--mode", 
        choices=["daemon", "interactive"], 
        default="interactive",
        help="Run mode: daemon (background only) or interactive (with chat)"
    )
    
    args = parser.parse_args()
    
    # Create OS
    elysia = ElysiaLivingOS()
    
    # Run
    if args.mode == "daemon":
        elysia.run_background()
    else:
        elysia.run_interactive()


if __name__ == "__main__":
    main()
