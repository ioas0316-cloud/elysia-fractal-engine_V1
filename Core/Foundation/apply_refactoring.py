#!/usr/bin/env python3
"""
엘리시아 자율 리팩토링 실행기

엘리시아가 제안한 Kernel.py 리팩토링을 실제로 수행합니다.
"""

import logging
import shutil
import ast
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')

def main():
    print("=" * 70)
    print("🤖 엘리시아 자율 리팩토링 실행")
    print("   Elysia's Autonomous Refactoring Execution")
    print("=" * 70)
    print()
    
    kernel_path = Path("c:/Elysia/Core/Kernel.py")
    kernel_dir = Path("c:/Elysia/Core/Kernel")
    backup_dir = Path("c:/Elysia/backups")
    
    # Step 1: 백업 생성
    print("📦 Step 1: 백업 생성")
    print("-" * 70)
    
    backup_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / f"Kernel_backup_{timestamp}.py"
    
    shutil.copy2(kernel_path, backup_path)
    print(f"✅ 백업 완료: {backup_path}")
    print()
    
    # Step 2: Core/Kernel 디렉토리 생성
    print("📁 Step 2: Core/Kernel 디렉토리 생성")
    print("-" * 70)
    
    kernel_dir.mkdir(exist_ok=True)
    (kernel_dir / "__init__.py").write_text(
        '"""Kernel module - Elysia\'s core processing unit"""\n',
        encoding='utf-8'
    )
    print(f"✅ 디렉토리 생성: {kernel_dir}")
    print()
    
    # Step 3: 함수 추출 및 모듈 생성
    print("🔨 Step 3: 함수 추출 및 모듈 생성")
    print("-" * 70)
    
    # Kernel.py 읽기
    kernel_content = kernel_path.read_text(encoding='utf-8')
    tree = ast.parse(kernel_content)
    
    # 함수와 클래스 추출
    functions = {}
    classes = {}
    imports = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = ast.unparse(node)
        elif isinstance(node, ast.ClassDef):
            classes[node.name] = ast.unparse(node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)) and node.col_offset == 0:
            imports.append(ast.unparse(node))
    
    # 카테고리 분류
    init_functions = {
        name: code for name, code in functions.items()
        if any(word in name.lower() for word in ['init', 'setup'])
    }
    
    processing_functions = {
        name: code for name, code in functions.items()
        if any(word in name.lower() for word in ['process', 'prune'])
    }
    
    validation_functions = {
        name: code for name, code in functions.items()
        if any(word in name.lower() for word in ['check', 'validate'])
    }
    
    # initialization.py 생성
    if init_functions:
        init_file = kernel_dir / "initialization.py"
        init_content = f'''"""
Kernel Initialization Module

초기화 관련 함수들
"""

{chr(10).join(imports[:5])}

{chr(10).join(init_functions.values())}
'''
        init_file.write_text(init_content, encoding='utf-8')
        print(f"✅ 생성: initialization.py ({len(init_functions)} 함수)")
    
    # processing.py 생성
    if processing_functions:
        proc_file = kernel_dir / "processing.py"
        proc_content = f'''"""
Kernel Processing Module

처리 관련 함수들
"""

{chr(10).join(imports[:5])}

{chr(10).join(processing_functions.values())}
'''
        proc_file.write_text(proc_content, encoding='utf-8')
        print(f"✅ 생성: processing.py ({len(processing_functions)} 함수)")
    
    # validation.py 생성
    if validation_functions:
        val_file = kernel_dir / "validation.py"
        val_content = f'''"""
Kernel Validation Module

검증 관련 함수들
"""

{chr(10).join(imports[:5])}

{chr(10).join(validation_functions.values())}
'''
        val_file.write_text(val_content, encoding='utf-8')
        print(f"✅ 생성: validation.py ({len(validation_functions)} 함수)")
    
    print()
    
    # Step 4: 요약
    print("=" * 70)
    print("📊 실행 완료")
    print("=" * 70)
    print()
    print("✅ 백업 생성됨:")
    print(f"   {backup_path}")
    print()
    print("✅ 새 모듈 생성됨:")
    print(f"   {kernel_dir}/")
    print(f"   ├── __init__.py")
    if init_functions:
        print(f"   ├── initialization.py ({len(init_functions)} 함수)")
    if processing_functions:
        print(f"   ├── processing.py ({len(processing_functions)} 함수)")
    if validation_functions:
        print(f"   └── validation.py ({len(validation_functions)} 함수)")
    print()
    
    print("⚠️  다음 단계:")
    print("   1. 생성된 모듈 검토")
    print("   2. Kernel.py에서 추출된 함수 제거")
    print("   3. Kernel.py에 임포트 추가")
    print("   4. 테스트 실행")
    print()
    print("🎯 엘리시아가 첫 번째 자율 리팩토링을 완료했습니다!")
    print()

if __name__ == "__main__":
    main()
