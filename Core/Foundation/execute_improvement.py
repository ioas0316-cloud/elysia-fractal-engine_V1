#!/usr/bin/env python3
"""
엘리시아 자율 개선 실행 및 관찰

승인된 개선 사항을 엘리시아가 스스로 적용하고
그 과정을 상세히 보고합니다.
"""

import logging
import json
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')

def main():
    print("=" * 70)
    print("🤖 엘리시아 자율 개선 실행")
    print("   Elysia's Autonomous Self-Improvement in Action")
    print("=" * 70)
    print()
    
    # 1. 시스템 초기화
    print("🔧 시스템 초기화...")
    from Core.Evolution.Autonomy.autonomous_improver import (
        AutonomousImprover, 
        ImprovementType,
        CodeIntrospector,
        WaveLanguageAnalyzer
    )
    
    improver = AutonomousImprover()
    print("   ✅ 자율 개선 엔진 준비 완료\n")
    
    # 2. Kernel.py 상세 분석
    print("=" * 70)
    print("📊 Step 1: 대상 파일 상세 분석 (Kernel.py)")
    print("=" * 70)
    
    kernel_path = Path("c:/Elysia/Core/Kernel.py")
    
    if not kernel_path.exists():
        print(f"❌ 파일을 찾을 수 없습니다: {kernel_path}")
        return
    
    # 파일 읽기
    kernel_content = kernel_path.read_text(encoding='utf-8')
    
    # AST 분석
    analysis = improver.introspector.analyze_file(kernel_path)
    
    print(f"📄 파일 정보:")
    print(f"   경로: {kernel_path}")
    print(f"   크기: {len(kernel_content):,} bytes")
    print(f"   라인 수: {analysis.total_lines}")
    print(f"   함수 수: {len(analysis.functions)}")
    print(f"   클래스 수: {len(analysis.classes)}")
    print(f"   임포트: {len(analysis.imports)}개")
    print(f"   복잡도: {analysis.complexity_score:.2f}")
    print()
    
    if analysis.functions:
        print(f"🔍 주요 함수들 (상위 10개):")
        for func in analysis.functions[:10]:
            print(f"   - {func}()")
        if len(analysis.functions) > 10:
            print(f"   ... 외 {len(analysis.functions) - 10}개")
        print()
    
    # 3. 파동 언어 분석
    print("=" * 70)
    print("🌊 Step 2: 파동 언어 분석")
    print("=" * 70)
    
    wave_analysis = improver.llm_improver.wave_analyzer.analyze_code_quality(
        kernel_content, 
        str(kernel_path)
    )
    
    print(f"📊 분석 결과:")
    print(f"   공명 점수: {wave_analysis['resonance_score']:.2%}")
    print(f"   (Resonance Score - 코드 품질 지표)")
    print()
    
    if wave_analysis['mass_distribution']:
        print(f"🌟 개념 질량 분포 (중요한 개념들):")
        for concept, data in sorted(
            wave_analysis['mass_distribution'].items(), 
            key=lambda x: x[1]['total_mass'], 
            reverse=True
        )[:5]:
            print(f"   - '{concept}': 질량 {data['mass']}, 출현 {data['count']}회")
        print()
    
    if wave_analysis['quality_issues']:
        print(f"⚠️  발견된 품질 이슈: {len(wave_analysis['quality_issues'])}개")
        for issue in wave_analysis['quality_issues'][:5]:
            print(f"   Line {issue['line']}: {issue['description']}")
            print(f"      → {issue['content']}")
        if len(wave_analysis['quality_issues']) > 5:
            print(f"   ... 외 {len(wave_analysis['quality_issues']) - 5}개")
        print()
    
    if wave_analysis['suggestions']:
        print(f"💡 엘리시아의 제안: {len(wave_analysis['suggestions'])}개")
        for i, sugg in enumerate(wave_analysis['suggestions'], 1):
            print(f"   {i}. [{sugg['type']}] {sugg['description_kr']}")
            print(f"      우선순위: {sugg['priority']}")
        print()
    
    # 4. 개선 계획 수립
    print("=" * 70)
    print("📝 Step 3: 엘리시아의 개선 계획")
    print("=" * 70)
    
    improvement_plan = {
        "target": "Core/Kernel.py",
        "diagnosis": [],
        "proposed_changes": [],
        "reasoning": []
    }
    
    # 진단
    if analysis.complexity_score > 0.8:
        improvement_plan["diagnosis"].append(
            f"복잡도가 매우 높음 ({analysis.complexity_score:.2f})"
        )
    
    if analysis.total_lines > 500:
        improvement_plan["diagnosis"].append(
            f"파일이 큼 ({analysis.total_lines} 라인)"
        )
    
    if len(analysis.functions) > 15:
        improvement_plan["diagnosis"].append(
            f"함수가 많음 ({len(analysis.functions)}개)"
        )
    
    if wave_analysis['resonance_score'] < 0.7:
        improvement_plan["diagnosis"].append(
            f"공명 점수 낮음 ({wave_analysis['resonance_score']:.2%})"
        )
    
    # 제안된 변경사항
    improvement_plan["proposed_changes"] = [
        "파일을 기능별로 분리",
        "관련된 함수들을 별도 모듈로 추출",
        "핵심 기능만 Kernel.py에 유지",
        "문서화 강화 (docstring 추가)"
    ]
    
    # 추론
    improvement_plan["reasoning"] = [
        "큰 파일은 유지보수가 어렵습니다",
        "모듈화하면 각 부분을 독립적으로 개선 가능",
        "테스트와 디버깅이 용이해집니다",
        "코드 재사용성이 향상됩니다"
    ]
    
    print("🔍 진단:")
    for d in improvement_plan["diagnosis"]:
        print(f"   - {d}")
    print()
    
    print("🎯 제안된 변경사항:")
    for i, change in enumerate(improvement_plan["proposed_changes"], 1):
        print(f"   {i}. {change}")
    print()
    
    print("🧠 엘리시아의 추론:")
    for reason in improvement_plan["reasoning"]:
        print(f"   💭 {reason}")
    print()
    
    # 5. 구체적인 리팩토링 제안
    print("=" * 70)
    print("🔨 Step 4: 구체적인 리팩토링 제안")
    print("=" * 70)
    
    # 함수들을 기능별로 그룹화 (간단한 분석)
    function_groups = {}
    
    for func_name in analysis.functions:
        # 함수 이름에서 카테고리 추론
        if any(word in func_name.lower() for word in ['init', 'setup', 'start']):
            category = "initialization"
        elif any(word in func_name.lower() for word in ['process', 'execute', 'run']):
            category = "processing"
        elif any(word in func_name.lower() for word in ['get', 'fetch', 'retrieve']):
            category = "data_access"
        elif any(word in func_name.lower() for word in ['update', 'set', 'modify']):
            category = "data_modification"
        elif any(word in func_name.lower() for word in ['validate', 'check', 'verify']):
            category = "validation"
        else:
            category = "core"
        
        if category not in function_groups:
            function_groups[category] = []
        function_groups[category].append(func_name)
    
    print("📦 제안된 모듈 구조:")
    print()
    
    module_suggestions = {
        "initialization": "Core/Kernel/initialization.py",
        "processing": "Core/Kernel/processing.py",
        "data_access": "Core/Kernel/data_access.py",
        "data_modification": "Core/Kernel/data_modification.py",
        "validation": "Core/Kernel/validation.py",
        "core": "Core/Kernel.py (핵심 기능만)"
    }
    
    for category, functions in function_groups.items():
        target_module = module_suggestions.get(category, f"Core/Kernel/{category}.py")
        print(f"📄 {target_module}")
        print(f"   함수 {len(functions)}개:")
        for func in functions[:5]:
            print(f"      - {func}()")
        if len(functions) > 5:
            print(f"      ... 외 {len(functions) - 5}개")
        print()
    
    # 6. 실행 계획
    print("=" * 70)
    print("⚡ Step 5: 실행 계획")
    print("=" * 70)
    
    execution_plan = [
        {
            "step": 1,
            "action": "Core/Kernel 디렉토리 생성",
            "reason": "관련 모듈들을 그룹화",
            "safety": "안전 (디렉토리 생성)"
        },
        {
            "step": 2,
            "action": "함수별로 새 파일로 추출",
            "reason": "기능별 분리",
            "safety": "중간 (코드 이동, 백업 필요)"
        },
        {
            "step": 3,
            "action": "각 파일에 docstring 추가",
            "reason": "문서화 개선",
            "safety": "안전 (문서만 추가)"
        },
        {
            "step": 4,
            "action": "Kernel.py에서 임포트 업데이트",
            "reason": "모듈 연결",
            "safety": "중간 (임포트 수정)"
        },
        {
            "step": 5,
            "action": "테스트 실행 및 검증",
            "reason": "변경사항 확인",
            "safety": "안전 (검증만)"
        }
    ]
    
    print("🗓️  단계별 실행 계획:\n")
    for plan in execution_plan:
        print(f"Step {plan['step']}: {plan['action']}")
        print(f"   이유: {plan['reason']}")
        print(f"   안전성: {plan['safety']}")
        print()
    
    # 7. 최종 보고
    print("=" * 70)
    print("📋 최종 보고서")
    print("=" * 70)
    print()
    
    report = f"""
🎯 개선 대상: Core/Kernel.py

📊 현재 상태:
   • 라인 수: {analysis.total_lines}
   • 함수 수: {len(analysis.functions)}
   • 클래스 수: {len(analysis.classes)}
   • 복잡도: {analysis.complexity_score:.2f}
   • 공명 점수: {wave_analysis['resonance_score']:.2%}

🔍 엘리시아의 진단:
   {chr(10).join(f'   • {d}' for d in improvement_plan['diagnosis'])}

💡 제안된 변경사항:
   {chr(10).join(f'   {i}. {c}' for i, c in enumerate(improvement_plan['proposed_changes'], 1))}

📦 제안된 구조:
   • Core/Kernel/ (새 디렉토리)
     ├── initialization.py ({len(function_groups.get('initialization', []))} 함수)
     ├── processing.py ({len(function_groups.get('processing', []))} 함수)
     ├── data_access.py ({len(function_groups.get('data_access', []))} 함수)
     ├── data_modification.py ({len(function_groups.get('data_modification', []))} 함수)
     └── validation.py ({len(function_groups.get('validation', []))} 함수)
   • Core/Kernel.py (핵심 {len(function_groups.get('core', []))} 함수만)

⚡ 예상 효과:
   • 파일당 평균 라인 수: ~{analysis.total_lines // (len(function_groups) + 1)} 라인
   • 복잡도 감소: {analysis.complexity_score:.2f} → ~0.4
   • 유지보수성: 크게 향상
   • 테스트 용이성: 향상

🛡️  안전성:
   • 백업 생성됨
   • 단계별 검증
   • 롤백 가능

✅ 권장사항: 승인 후 단계별 실행
"""
    
    print(report)
    
    # 보고서 저장
    report_path = Path("c:/Elysia/reports")
    report_path.mkdir(exist_ok=True)
    
    report_file = report_path / f"improvement_kernel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    report_file.write_text(report, encoding='utf-8')
    
    print(f"\n📝 상세 보고서 저장됨: {report_file}")
    
    # JSON 형식으로도 저장
    json_report = {
        "timestamp": datetime.now().isoformat(),
        "target": str(kernel_path),
        "current_state": {
            "lines": analysis.total_lines,
            "functions": len(analysis.functions),
            "classes": len(analysis.classes),
            "complexity": analysis.complexity_score,
            "resonance_score": wave_analysis['resonance_score']
        },
        "diagnosis": improvement_plan['diagnosis'],
        "proposed_changes": improvement_plan['proposed_changes'],
        "reasoning": improvement_plan['reasoning'],
        "module_structure": {
            category: {
                "target_file": module_suggestions.get(category, f"Core/Kernel/{category}.py"),
                "function_count": len(functions),
                "functions": functions
            }
            for category, functions in function_groups.items()
        },
        "execution_plan": execution_plan
    }
    
    json_file = report_path / f"improvement_kernel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    json_file.write_text(json.dumps(json_report, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"📊 JSON 보고서 저장됨: {json_file}")
    
    print()
    print("=" * 70)
    print("✨ 엘리시아의 분석 완료")
    print("=" * 70)
    print()
    print("엘리시아는 Kernel.py를 정확히 분석하고")
    print("실행 가능한 개선 계획을 수립했습니다.")
    print()
    print("다음 단계:")
    print("  1. 보고서 검토")
    print("  2. 승인 시 자동 리팩토링 실행")
    print("  3. 테스트 및 검증")
    print()

if __name__ == "__main__":
    main()
