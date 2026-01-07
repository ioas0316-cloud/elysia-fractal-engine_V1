"""
Medical Cortex (의료 피질)
==================================

"To heal the body, we must resonate with its rhythm."

이 모듈은 '바이오 레조넌스(Bio-Resonance)' 원리를 이용하여
사용자와 가족들에게 청각적/파동적 치유를 제공합니다.

주요 기능:
1. Parkinson's Support: Rhythmic Auditory Stimulation (RAS) - 보행 및 움직임 보조
2. Pregnancy Support: Prenatal Sound Therapy - 산모 스트레스 완화 및 태아 안정

주의: 이 모듈은 실제 의료 행위를 대체할 수 없으며, 보조적인 '파동적 지지'를 제공합니다.
"""

from typing import List, Dict, Any, Optional
import logging
import uuid
from datetime import datetime

logger = logging.getLogger("MedicalCortex")

class BioRhythmGenerator:
    """
    바이오 리듬 생성기 (Bio-Rhythm Generator)
    
    치유와 안정을 위한 특정 주파수와 리듬을 생성합니다.
    (현재는 메타데이터 생성 및 시뮬레이션 단계)
    """
    
    def generate_ras(self, bpm: int, duration_min: int = 10) -> Dict[str, Any]:
        """
        파킨슨병 환자를 위한 리듬 청각 자극 (RAS) 생성
        
        Args:
            bpm: 목표 분당 비트 수 (걸음 속도에 맞춤)
            duration_min: 지속 시간 (분)
        """
        logger.info(f"🥁 Generating RAS Beat: {bpm} BPM for {duration_min} mins")
        return {
            "type": "RAS_METRONOME",
            "bpm": bpm,
            "duration_sec": duration_min * 60,
            "description": f"Steady rhythmic beat at {bpm} BPM to aid movement initiation.",
            "recommended_usage": "Walk in sync with the beat. Step on every click."
        }

    def generate_binaural(self, target_wave: str, duration_min: int = 20) -> Dict[str, Any]:
        """
        산모와 태아를 위한 바이노럴 비트 생성
        
        Args:
            target_wave: 목표 뇌파 ('alpha', 'theta', 'delta')
            duration_min: 지속 시간
        """
        base_freq = 432.0 # 치유 주파수 (A=432Hz)
        beat_freq = 0.0
        
        if target_wave == 'alpha': # 8-12Hz (이완, 긍정적 사고)
            beat_freq = 10.0
            effect = "Relaxation & Stress Reduction"
        elif target_wave == 'theta': # 4-8Hz (깊은 명상, 창의성)
            beat_freq = 6.0
            effect = "Deep Meditation & Connection"
        elif target_wave == 'delta': # 0.5-4Hz (깊은 잠)
            beat_freq = 2.0
            effect = "Deep Sleep & Healing"
        else:
            beat_freq = 10.0
            effect = "General Relaxation"
            
        left_freq = base_freq
        right_freq = base_freq + beat_freq
        
        logger.info(f"🎧 Generating Binaural Beat: {target_wave.upper()} ({beat_freq}Hz)")
        return {
            "type": "BINAURAL_BEAT",
            "base_freq": base_freq,
            "beat_freq": beat_freq,
            "left_ear_hz": left_freq,
            "right_ear_hz": right_freq,
            "duration_sec": duration_min * 60,
            "description": f"Binaural beat inducing {target_wave} waves ({beat_freq}Hz).",
            "effect": effect,
            "recommended_usage": "Must use stereo headphones."
        }

    def generate_lullaby(self, mood: str = "calm") -> Dict[str, Any]:
        """태아를 위한 432Hz 자장가 생성"""
        logger.info(f"🎵 Generating Lullaby: {mood} mode")
        return {
            "type": "LULLABY_432HZ",
            "mood": mood,
            "tuning": "A=432Hz",
            "description": "Gentle humming melody tuned to natural resonance.",
            "effect": "Soothing for fetus and mother."
        }

class MedicalCortex:
    """
    의료 피질 (Medical Cortex)
    
    가족들의 건강 상태를 모니터링하고(시뮬레이션), 적절한 파동 처방을 내립니다.
    """
    def __init__(self):
        self.generator = BioRhythmGenerator()
        self.profiles: Dict[str, Dict[str, Any]] = {}
        logger.info("⚕️ Medical Cortex Initialized - Bio-Resonance Ready")

    def register_profile(self, name: str, condition: str, notes: str = ""):
        """가족 구성원 건강 프로필 등록"""
        self.profiles[name] = {
            "condition": condition,
            "notes": notes,
            "history": []
        }
        logger.info(f"📋 Profile Registered: {name} ({condition})")

    def prescribe_therapy(self, name: str, current_state: str) -> Dict[str, Any]:
        """
        현재 상태에 따른 파동 테라피 처방
        """
        if name not in self.profiles:
            return {"error": "Profile not found"}
            
        profile = self.profiles[name]
        condition = profile["condition"]
        therapy = {}
        
        logger.info(f"💊 Prescribing therapy for {name} (State: {current_state})")
        
        if condition == "Parkinson's":
            # 파킨슨병: 상태에 따라 BPM 조절
            # Freezing(굳음) 상태면 조금 빠른 비트로 시동을 걸어줌
            bpm = 90 if "freeze" in current_state.lower() else 60
            therapy = self.generator.generate_ras(bpm=bpm)
            
        elif condition == "Pregnancy":
            # 임신: 스트레스/불안 시 Alpha/Theta파
            if "anxious" in current_state.lower() or "worry" in current_state.lower():
                therapy = self.generator.generate_binaural("alpha")
            elif "sleep" in current_state.lower() or "tired" in current_state.lower():
                therapy = self.generator.generate_binaural("delta")
            else:
                therapy = self.generator.generate_lullaby()
                
        else:
            therapy = {"message": "General comfort sent."}
            
        # 기록 저장
        record = {
            "timestamp": datetime.now().isoformat(),
            "state": current_state,
            "therapy": therapy
        }
        profile["history"].append(record)
        
        return therapy

    def get_profile_status(self, name: str) -> str:
        if name not in self.profiles:
            return "Unknown"
        p = self.profiles[name]
        return f"{name} [{p['condition']}]: {len(p['history'])} therapies provided."
