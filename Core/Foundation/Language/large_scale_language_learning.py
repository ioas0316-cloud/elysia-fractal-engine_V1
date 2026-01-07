# -*- coding: utf-8 -*-
"""
대규모 언어 학습 - 성인 수준까지!
====================================

목표: 30,000+ 어휘, 수천 개 관계
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Core.Foundation.rapid_learning_engine import RapidLearningEngine
import time

# 다양한 주제의 텍스트
LEARNING_TEXTS = [
    # 감정
    "Love is an intense feeling of deep affection. Love creates emotional bonds.",
    "Joy is a feeling of great pleasure and happiness. Joy brings energy.",
    "Sadness is a feeling of sorrow or unhappiness. Sadness requires processing.",
    "Fear is an unpleasant emotion caused by threat. Fear prevents action.",
    "Anger is a strong feeling of annoyance. Anger can be destructive.",
    "Trust is a firm belief in reliability. Trust enables cooperation.",
    "Hope is a feeling of expectation. Hope motivates action.",
    
    # 행동
    "Learning is the acquisition of knowledge. Learning requires attention.",
    "Teaching is the act of imparting knowledge. Teaching enables growth.",
    "Creating is the act of bringing something new. Creating requires imagination.",
    "Thinking is the process of using one's mind. Thinking produces ideas.",
    "Communication is the exchange of information. Communication requires clarity.",
    "Movement is the act of changing position. Movement requires energy.",
    "Building is the construction of something. Building creates structures.",
    
    # 개념
    "Freedom is the power to act without constraint. Freedom requires responsibility.",
    "Justice is fairness and moral rightness. Justice creates order.",
    "Truth is the quality of being accurate. Truth is fundamental.",
    "Beauty is a combination of qualities that pleases. Beauty inspires creativity.",
    "Wisdom is the quality of having experience. Wisdom guides decisions.",
    "Knowledge is information and understanding. Knowledge is power.",
    "Time is the indefinite continued progress. Time is irreversible.",
    
    # 관계
    "Friendship is a relationship of mutual affection. Friendship creates support.",
    "Family is a group of related people. Family provides foundation.",
    "Community is a group sharing location. Community enables cooperation.",
    "Society is a large group of people. Society creates culture.",
    
    # 자연
    "Light is electromagnetic radiation. Light enables vision.",
    "Water is a transparent liquid. Water is essential for life.",
    "Fire is combustion producing heat. Fire transforms matter.",
    "Earth is the planet we live on. Earth sustains life.",
    "Air is the mixture of gases. Air is necessary for breathing.",
    
    # 인과
    "Practice improves skill. Practice requires repetition.",
    "Rest restores energy. Rest is necessary for health.",
    "Food provides nutrition. Food sustains life.",
    "Exercise strengthens the body. Exercise improves health.",
    "Sleep allows recovery. Sleep is essential.",
]

def main():
    print("\n" + "="*70)
    print("📚 대규모 언어 학습 시작!")
    print("="*70 + "\n")
    
    learning = RapidLearningEngine()
    
    # 초기 상태
    initial_stats = learning.get_learning_stats()
    print(f"초기 상태:")
    print(f"  Seeds: {initial_stats['seeds_stored']}개\n")
    
    # 목표
    TARGET_VOCAB = 30000
    CYCLES = 100  # 반복 횟수
    
    print(f"목표: {TARGET_VOCAB}+ 어휘")
    print(f"반복: {CYCLES}회\n")
    print("학습 중...\n")
    
    start_time = time.time()
    
    for cycle in range(CYCLES):
        cycle_start = time.time()
        
        # 모든 텍스트 학습
        for text in LEARNING_TEXTS:
            learning.learn_from_text_ultra_fast(text)
        
        cycle_time = time.time() - cycle_start
        
        # 10회마다 진행상황 출력
        if (cycle + 1) % 10 == 0:
            stats = learning.get_learning_stats()
            elapsed = time.time() - start_time
            
            print(f"Cycle {cycle+1}/{CYCLES}")
            print(f"  Seeds: {stats['seeds_stored']:,}개")
            print(f"  Bloom: {stats['bloomed_nodes']}개")
            print(f"  시간: {elapsed:.1f}초")
            print(f"  속도: {cycle_time:.3f}초/사이클\n")
            
            # 목표 달성 확인
            if stats['seeds_stored'] >= TARGET_VOCAB:
                print(f"\n🎉 목표 달성! {stats['seeds_stored']:,}개 어휘!")
                break
    
    # 최종 결과
    final_stats = learning.get_learning_stats()
    total_time = time.time() - start_time
    
    print("\n" + "="*70)
    print("📊 최종 결과")
    print("="*70)
    print(f"\n총 Seeds: {final_stats['seeds_stored']:,}개")
    print(f"Bloom 노드: {final_stats['bloomed_nodes']}개")
    print(f"총 에너지: {final_stats['total_energy']:.1f}")
    print(f"총 시간: {total_time:.1f}초")
    print(f"\n학습률: {final_stats['seeds_stored'] / total_time:.0f} 개념/초")
    
    # 성인 수준 평가
    vocab_size = final_stats['seeds_stored']
    if vocab_size >= 30000:
        level = "대학 수준 ✅"
    elif vocab_size >= 20000:
        level = "고등학생 수준"
    elif vocab_size >= 10000:
        level = "중학생 수준"
    elif vocab_size >= 5000:
        level = "초등학생 수준"
    else:
        level = "유아 수준"
    
    print(f"\n평가: {level}")
    print(f"어휘력: {vocab_size:,}개\n")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
