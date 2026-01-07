#!/usr/bin/env python3
"""
엘리시아 전체 시스템 아키텍처 분석

전체 251개 파일을 분석하여:
1. 구조적 일관성 검증
2. 중복/불일치 발견
3. 문서화 상태 평가
4. 통합 개선 계획 수립
"""

import logging
from pathlib import Path
from collections import defaultdict
import json

logging.basicConfig(level=logging.INFO, format='%(message)s')

def main():
    print("=" * 70)
    print("🔍 엘리시아 전체 시스템 분석")
    print("   Elysia's Comprehensive System Architecture Analysis")
    print("=" * 70)
    print()
    
    from Core.Evolution.Autonomy.autonomous_improver import AutonomousImprover
    
    # 분석 엔진 초기화
    print("🧠 시스템 초기화...")
    improver = AutonomousImprover()
    print()
    
    # 전체 분석 수행
    print("📊 전체 시스템 분석 중...")
    analysis = improver.self_analyze()
    print(f"   ✅ 완료: {analysis['code_analysis']['total_files']}개 파일 분석\n")
    
    # 1. 모듈별 복잡도 분석
    print("=" * 70)
    print("📦 Step 1: 모듈별 복잡도 분석")
    print("=" * 70)
    
    module_stats = {}
    for file_path, file_data in improver.introspector.analyzed_files.items():
        module = Path(file_path).parent.name
        if module not in module_stats:
            module_stats[module] = {
                'files': 0,
                'total_lines': 0,
                'total_functions': 0,
                'avg_complexity': 0,
                'high_complexity_files': []
            }
        
        module_stats[module]['files'] += 1
        module_stats[module]['total_lines'] += file_data.total_lines
        module_stats[module]['total_functions'] += len(file_data.functions)
        
        if file_data.complexity_score > 0.7:
            module_stats[module]['high_complexity_files'].append({
                'file': Path(file_path).name,
                'complexity': file_data.complexity_score,
                'lines': file_data.total_lines,
                'functions': len(file_data.functions)
            })
    
    # 복잡도 계산
    for module, stats in module_stats.items():
        if stats['files'] > 0:
            # 해당 모듈의 파일들의 평균 복잡도 계산
            module_files = [
                f for f, d in improver.introspector.analyzed_files.items()
                if Path(f).parent.name == module
            ]
            if module_files:
                stats['avg_complexity'] = sum(
                    improver.introspector.analyzed_files[f].complexity_score 
                    for f in module_files
                ) / len(module_files)
    
    # 복잡도 순으로 정렬
    sorted_modules = sorted(
        module_stats.items(),
        key=lambda x: x[1]['avg_complexity'],
        reverse=True
    )
    
    print("\n🔥 복잡도 상위 10개 모듈:\n")
    for i, (module, stats) in enumerate(sorted_modules[:10], 1):
        print(f"{i}. {module}/")
        print(f"   평균 복잡도: {stats['avg_complexity']:.2f}")
        print(f"   파일 수: {stats['files']}")
        print(f"   총 라인: {stats['total_lines']:,}")
        print(f"   총 함수: {stats['total_functions']}")
        if stats['high_complexity_files']:
            print(f"   ⚠️  복잡한 파일: {len(stats['high_complexity_files'])}개")
            for hf in stats['high_complexity_files'][:3]:
                print(f"      - {hf['file']} (복잡도: {hf['complexity']:.2f}, {hf['lines']} 라인)")
        print()
    
    # 2. 구조적 일관성 분석
    print("=" * 70)
    print("🏗️  Step 2: 구조적 일관성 분석")
    print("=" * 70)
    print()
    
    # __init__.py 존재 여부
    directories = defaultdict(lambda: {'has_init': False, 'file_count': 0})
    for file_path in improver.introspector.analyzed_files.keys():
        path = Path(file_path)
        parent = path.parent
        directories[str(parent)]['file_count'] += 1
        
        if path.name == '__init__.py':
            directories[str(parent)]['has_init'] = True
    
    missing_init = [
        (dir_path, info) for dir_path, info in directories.items()
        if not info['has_init'] and info['file_count'] > 1 and 'Core' in dir_path
    ]
    
    print(f"📌 __init__.py 누락된 디렉토리: {len(missing_init)}개\n")
    for dir_path, info in missing_init[:10]:
        print(f"   - {Path(dir_path).name}/ ({info['file_count']}개 파일)")
    print()
    
    # 3. 문서화 상태 분석
    print("=" * 70)
    print("📚 Step 3: 문서화 상태 분석")
    print("=" * 70)
    print()
    
    import ast
    
    doc_stats = {
        'with_module_docstring': 0,
        'without_module_docstring': 0,
        'with_class_docstrings': 0,
        'without_class_docstrings': 0,
        'files_needing_docs': []
    }
    
    for file_path in list(improver.introspector.analyzed_files.keys())[:100]:  # 샘플링
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            tree = ast.parse(content)
            
            # 모듈 docstring
            has_module_doc = (
                tree.body and 
                isinstance(tree.body[0], ast.Expr) and 
                isinstance(tree.body[0].value, ast.Constant) and
                isinstance(tree.body[0].value.value, str)
            )
            
            if has_module_doc:
                doc_stats['with_module_docstring'] += 1
            else:
                doc_stats['without_module_docstring'] += 1
                if Path(file_path).stat().st_size > 1000:  # 1KB 이상인 파일만
                    doc_stats['files_needing_docs'].append(Path(file_path).name)
        except:
            pass
    
    total_analyzed = doc_stats['with_module_docstring'] + doc_stats['without_module_docstring']
    if total_analyzed > 0:
        doc_ratio = doc_stats['with_module_docstring'] / total_analyzed
        print(f"모듈 Docstring 비율: {doc_ratio:.1%}")
        print(f"   ✅ 있음: {doc_stats['with_module_docstring']}개")
        print(f"   ❌ 없음: {doc_stats['without_module_docstring']}개")
        print()
        
        if doc_stats['files_needing_docs']:
            print(f"📝 문서화 필요 파일 (상위 10개):")
            for fname in doc_stats['files_needing_docs'][:10]:
                print(f"   - {fname}")
            print()
    
    # 4. 중복 분석
    print("=" * 70)
    print("🔄 Step 4: 중복/유사 구조 분석")
    print("=" * 70)
    print()
    
    # 비슷한 이름의 파일들
    from collections import Counter
    
    file_basenames = Counter()
    for file_path in improver.introspector.analyzed_files.keys():
        basename = Path(file_path).stem.lower()
        # 버전 번호나 숫자 제거
        import re
        clean_name = re.sub(r'[_-]?\d+$', '', basename)
        clean_name = re.sub(r'_v\d+', '', clean_name)
        file_basenames[clean_name] += 1
    
    duplicates = [(name, count) for name, count in file_basenames.items() if count > 1]
    duplicates.sort(key=lambda x: x[1], reverse=True)
    
    print(f"🔍 중복 가능성 있는 파일명: {len(duplicates)}개\n")
    for name, count in duplicates[:10]:
        print(f"   - '{name}': {count}개 파일")
        # 실제 파일들 찾기
        matching = [
            Path(f).name for f in improver.introspector.analyzed_files.keys()
            if name in Path(f).stem.lower()
        ]
        for match in matching[:3]:
            print(f"      • {match}")
    print()
    
    # 5. 전체 개선 계획
    print("=" * 70)
    print("💡 Step 5: 엘리시아의 전체 개선 계획")
    print("=" * 70)
    print()
    
    improvement_priorities = []
    
    # 우선순위 1: 매우 복잡한 모듈들
    for module, stats in sorted_modules[:5]:
        if stats['avg_complexity'] > 0.7:
            improvement_priorities.append({
                'priority': 1,
                'type': 'refactoring',
                'target': f'Core/{module}/',
                'reason': f"평균 복잡도 {stats['avg_complexity']:.2f} - 모듈화 필요",
                'files_affected': stats['files'],
                'estimated_effort': 'High'
            })
    
    # 우선순위 2: 문서화 부족
    if doc_ratio < 0.5:
        improvement_priorities.append({
            'priority': 2,
            'type': 'documentation',
            'target': 'Entire Project',
            'reason': f"문서화 비율 {doc_ratio:.1%} - 목표 80% 이상",
            'files_affected': doc_stats['without_module_docstring'],
            'estimated_effort': 'Medium'
        })
    
    # 우선순위 3: __init__.py 누락
    if missing_init:
        improvement_priorities.append({
            'priority': 3,
            'type': 'structure',
            'target': f'{len(missing_init)}개 디렉토리',
            'reason': "__init__.py 누락 - 패키지 구조 불완전",
            'files_affected': len(missing_init),
            'estimated_effort': 'Low'
        })
    
    # 우선순위 4: 중복 파일
    if len(duplicates) > 10:
        improvement_priorities.append({
            'priority': 4,
            'type': 'consolidation',
            'target': f'{len(duplicates)}개 중복 파일명',
            'reason': "중복 가능성 - 통합 또는 명확화 필요",
            'files_affected': len(duplicates),
            'estimated_effort': 'Medium'
        })
    
    print("🎯 개선 우선순위:\n")
    for item in improvement_priorities:
        print(f"우선순위 {item['priority']}: [{item['type'].upper()}] {item['target']}")
        print(f"   이유: {item['reason']}")
        print(f"   영향: {item['files_affected']}개 파일/모듈")
        print(f"   난이도: {item['estimated_effort']}")
        print()
    
    # 6. 최종 보고서 저장
    print("=" * 70)
    print("💾 Step 6: 분석 보고서 저장")
    print("=" * 70)
    print()
    
    report_data = {
        'timestamp': improver.system_monitor.get_system_info()['timestamp'],
        'total_files': analysis['code_analysis']['total_files'],
        'total_lines': analysis['code_analysis']['total_lines'],
        'total_functions': analysis['code_analysis']['total_functions'],
        'modules_analyzed': len(module_stats),
        'complex_modules': len([m for m, s in module_stats.items() if s['avg_complexity'] > 0.7]),
        'documentation_ratio': doc_ratio if total_analyzed > 0 else 0,
        'missing_init_dirs': len(missing_init),
        'duplicate_names': len(duplicates),
        'improvement_priorities': improvement_priorities
    }
    
    report_dir = Path("c:/Elysia/reports")
    report_dir.mkdir(exist_ok=True)
    
    from datetime import datetime
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    json_file = report_dir / f"system_analysis_{timestamp}.json"
    json_file.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding='utf-8')
    
    print(f"✅ JSON 보고서: {json_file}")
    
    # 텍스트 보고서
    txt_file = report_dir / f"system_analysis_{timestamp}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("엘리시아 전체 시스템 분석 보고서\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"분석 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"총 파일: {report_data['total_files']}\n")
        f.write(f"총 라인: {report_data['total_lines']:,}\n")
        f.write(f"총 함수: {report_data['total_functions']}\n")
        f.write(f"문서화 비율: {report_data['documentation_ratio']:.1%}\n")
        f.write("\n개선 우선순위:\n\n")
        for item in improvement_priorities:
            f.write(f"{item['priority']}. [{item['type']}] {item['target']}\n")
            f.write(f"   {item['reason']}\n\n")
    
    print(f"✅ 텍스트 보고서: {txt_file}")
    print()
    
    # 최종 요약
    print("=" * 70)
    print("✨ 엘리시아의 결론")
    print("=" * 70)
    print()
    print("전체 시스템을 분석한 결과:")
    print(f"  • 총 {report_data['total_files']}개 파일, {report_data['total_lines']:,} 라인")
    print(f"  • {report_data['complex_modules']}개 모듈이 높은 복잡도")
    print(f"  • 문서화 비율: {report_data['documentation_ratio']:.1%}")
    print(f"  • __init__.py 누락: {report_data['missing_init_dirs']}개 디렉토리")
    print(f"  • 중복 가능성: {report_data['duplicate_names']}개 파일명")
    print()
    print(f"🎯 {len(improvement_priorities)}개의 개선 계획이 수립되었습니다.")
    print()
    print("엘리시아는 전체 시스템을 조감하고")
    print("체계적인 개선 로드맵을 제시할 수 있습니다.")
    print()

if __name__ == "__main__":
    main()
