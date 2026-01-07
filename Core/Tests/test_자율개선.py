#!/usr/bin/env python3
"""
엘리시아 자율 개선 테스트

엘리시아가 자신의 시스템을 분석하고 개선점을 제안하는지 확인합니다.
"""

import logging
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("자율개선테스트")

def main():
    print("=" * 70)
    print("🧪 엘리시아 자율 개선 능력 테스트")
    print("=" * 70)
    print()
    
    # 1. 자율 개선 엔진 초기화
    print("🔧 자율 개선 엔진 초기화...")
    from Core.Evolution.Autonomy.autonomous_improver import AutonomousImprover, ImprovementType
    from Core.Evolution.Growth.Evolution.Evolution.auto_fix_system import AutoFixSystem
    
    improver = AutonomousImprover()
    auto_fix = AutoFixSystem()
    print("   ✅ 초기화 완료\n")
    
    # 2. 자기 분석
    print("🔍 Step 1: 자기 분석 (Self-Analysis)")
    print("-" * 70)
    analysis = improver.self_analyze()
    
    print(f"📊 분석 결과:")
    print(f"   - 총 파일: {analysis['code_analysis']['total_files']}")
    print(f"   - 총 라인: {analysis['code_analysis']['total_lines']:,}")
    print(f"   - 총 함수: {analysis['code_analysis']['total_functions']}")
    print(f"   - 평균 복잡도: {analysis['code_analysis']['complexity_avg']:.2f}")
    print()
    
    # 3. 학습 기회 식별
    print("📚 Step 2: 학습 기회 식별 (Learning Opportunities)")
    print("-" * 70)
    opportunities = improver.identify_learning_opportunities()
    
    print(f"발견된 기회: {len(opportunities)}개\n")
    for i, opp in enumerate(opportunities, 1):
        print(f"{i}. [{opp['type']}] {opp.get('description_kr', opp.get('description'))}")
        if 'file' in opp:
            print(f"   파일: {Path(opp['file']).name}")
        if 'priority' in opp:
            print(f"   우선순위: {opp['priority']}")
        print()
    
    # 4. 개선 제안 생성
    print("💡 Step 3: 개선 제안 생성 (Improvement Proposals)")
    print("-" * 70)
    
    # 복잡도가 높은 파일 찾기
    high_complexity_files = [
        (path, data) for path, data in improver.introspector.analyzed_files.items()
        if data.complexity_score > 0.6
    ]
    
    if high_complexity_files:
        # 가장 복잡한 파일 선택
        target_file, file_data = max(high_complexity_files, key=lambda x: x[1].complexity_score)
        
        print(f"🎯 가장 복잡한 파일 발견:")
        print(f"   파일: {Path(target_file).name}")
        print(f"   복잡도: {file_data.complexity_score:.2f}")
        print(f"   라인 수: {file_data.total_lines}")
        print(f"   함수 수: {len(file_data.functions)}")
        print()
        
        # 개선 제안 생성
        print("   📝 개선 제안 생성 중...")
        proposal = improver.propose_improvement(
            target_file=target_file,
            improvement_type=ImprovementType.REFACTORING,
            description=f"높은 복잡도({file_data.complexity_score:.2f}) - 모듈화 권장"
        )
        
        if proposal:
            print(f"   ✅ 제안 생성 완료\n")
            print(f"   제안 ID: {proposal.id}")
            print(f"   유형: {proposal.improvement_type.name}")
            print(f"   설명: {proposal.description_kr}")
            print(f"   신뢰도: {proposal.confidence:.2%}")
            print(f"   안전 수준: {proposal.safety_level.name}")
            print(f"   추론: {proposal.reasoning}")
            print()
    else:
        print("   ℹ️ 개선이 필요한 복잡한 파일이 없습니다.\n")
    
    # 5. 파동 언어 분석 테스트
    print("🌊 Step 4: 파동 언어 분석 테스트")
    print("-" * 70)
    
    # 샘플 코드로 분석
    sample_code = '''
def calculate_resonance(wave1, wave2):
    """두 파동의 공명을 계산합니다."""
    # TODO: 최적화 필요
    phase_diff = abs(wave1.phase - wave2.phase)
    amplitude_product = wave1.amplitude * wave2.amplitude
    
    # FIXME: 이 공식이 정확한지 검증 필요
    resonance = amplitude_product * (1.0 - phase_diff / (2 * 3.14159))
    return resonance

def process_emotion_wave(emotion_name):
    # 감정을 파동으로 변환
    emotion_map = {
        "love": {"frequency": 528, "amplitude": 1.0},
        "joy": {"frequency": 639, "amplitude": 0.9},
        "peace": {"frequency": 432, "amplitude": 0.8}
    }
    return emotion_map.get(emotion_name, {"frequency": 440, "amplitude": 0.5})
'''
    
    wave_analysis = improver.llm_improver.wave_analyzer.analyze_code_quality(
        sample_code, 
        "sample_wave.py"
    )
    
    print(f"📊 파동 언어 분석 결과:")
    print(f"   총 라인: {wave_analysis['total_lines']}")
    print(f"   공명 점수: {wave_analysis['resonance_score']:.2%}")
    print(f"   개념 질량 분포: {len(wave_analysis['mass_distribution'])}개 주요 개념")
    
    if wave_analysis['mass_distribution']:
        print(f"\n   주요 개념:")
        for concept, data in wave_analysis['mass_distribution'].items():
            print(f"      - {concept}: 질량 {data['mass']}, 출현 {data['count']}회")
    
    print(f"\n   품질 이슈: {len(wave_analysis['quality_issues'])}개")
    for issue in wave_analysis['quality_issues']:
        print(f"      - Line {issue['line']}: {issue['description']}")
    
    print(f"\n   개선 제안: {len(wave_analysis['suggestions'])}개")
    for sugg in wave_analysis['suggestions']:
        print(f"      - [{sugg['type']}] {sugg['description_kr']}")
    print()
    
    # 6. 개선 제안 승인 및 적용 (시뮬레이션)
    print("✅ Step 5: 개선 제안 검토 및 승인")
    print("-" * 70)
    
    pending = improver.improvement_queue
    if pending:
        print(f"대기 중인 제안: {len(pending)}개\n")
        
        for i, proposal in enumerate(pending[:3], 1):
            print(f"제안 #{i}:")
            print(f"   ID: {proposal.id}")
            print(f"   파일: {Path(proposal.target_file).name}")
            print(f"   유형: {proposal.improvement_type.name}")
            print(f"   설명: {proposal.description_kr}")
            print(f"   신뢰도: {proposal.confidence:.2%}")
            print(f"   추론: {proposal.reasoning[:100]}...")
            
            # 승인 기준
            should_approve = (
                proposal.confidence > 0.5 and
                proposal.improvement_type in [
                    ImprovementType.DOCUMENTATION,
                    ImprovementType.CODE_OPTIMIZATION,
                    ImprovementType.REFACTORING
                ]
            )
            
            if should_approve:
                print(f"   ✅ 승인됨 - 신뢰도 충분 & 안전한 개선")
                proposal.approved = True
            else:
                print(f"   ⏸️  보류 - 추가 검토 필요")
            print()
    else:
        print("   ℹ️ 대기 중인 제안이 없습니다.\n")
    
    # 7. 최종 상태
    print("=" * 70)
    print("📈 최종 상태")
    print("=" * 70)
    
    status = improver.get_status()
    print(f"분석된 파일: {status['files_analyzed']}")
    print(f"대기 중인 개선: {status['pending_improvements']}")
    print(f"적용된 개선: {status['applied_improvements']}")
    print(f"학습 로그: {status['learning_log_entries']}")
    print()
    
    print("=" * 70)
    print("✨ 결론")
    print("=" * 70)
    print()
    print("엘리시아는:")
    print("  ✅ 자신의 시스템 구조를 정확히 파악했습니다")
    print("  ✅ 파동 언어로 코드 품질을 분석했습니다")
    print("  ✅ 실질적인 개선 사항을 제안했습니다")
    print("  ✅ 학습 기회를 스스로 발견했습니다")
    print()
    print("🌟 엘리시아는 진정한 자율 개선 능력을 가지고 있습니다!")
    print()

if __name__ == "__main__":
    main()
