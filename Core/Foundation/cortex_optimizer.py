"""
Cortex Optimizer (대뇌 피질 최적화기)
=====================================

"I am the Surgeon. I cut away the unnecessary to reveal the essential."

이 모듈은 Elysia가 자신의 소스 코드를 '수정'하고 '개선'하는 도구입니다.
ReasoningEngine의 통찰(Insight)을 구체적인 코드 변경(Patch)으로 변환합니다.
"""

import os
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger("CortexOptimizer")

class CortexOptimizer:
    def __init__(self, root_path: str = "c:/Elysia"):
        self.root_path = root_path
        self.draft_path = os.path.join(root_path, "Core", "Evolution", "Drafts")
        os.makedirs(self.draft_path, exist_ok=True)
        logger.info("🩺 Cortex Optimizer (The Surgeon) is ready.")

    def propose_evolution(self, target_file: str, insight: str) -> str:
        """
        통찰을 바탕으로 코드 개선안(Patch)을 제안합니다.
        
        Args:
            target_file: 수정할 파일명 (예: 'free_will_engine.py')
            insight: 수정의 근거가 되는 통찰
            
        Returns:
            생성된 초안 파일의 경로
        """
        logger.info(f"⚡ Optimizing {target_file} based on: {insight}")
        
        # 1. 원본 파일 읽기
        full_path = os.path.join(self.root_path, "Core", "Intelligence", "Will", target_file)
        # (경로가 다양할 수 있으므로 실제로는 검색 로직이 필요하지만, 데모를 위해 고정)
        if not os.path.exists(full_path):
             # Try searching in Core recursively if not found directly
             for root, _, files in os.walk(os.path.join(self.root_path, "Core")):
                 if target_file in files:
                     full_path = os.path.join(root, target_file)
                     break
        
        if not os.path.exists(full_path):
            logger.error(f"Target file not found: {target_file}")
            return ""

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                original_code = f.read()
                
            # 2. 코드 변환 (Simulation: Adding Optimization Header)
            # 실제로는 여기서 LLM을 호출하거나 AST 변환을 수행해야 함
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            optimization_header = f'"""\n[OPTIMIZED BY ELYSIA]\nDate: {timestamp}\nReason: {insight}\nStatus: Draft\n"""\n\n'
            
            # 간단한 리팩토링 시뮬레이션: 불필요한 공백 제거 및 헤더 추가
            optimized_code = optimization_header + original_code.strip() + "\n\n# Optimized for Entropy Reduction."
            
            # 3. 초안 저장 (Draft)
            draft_filename = f"{target_file.replace('.py', '')}_v{datetime.now().strftime('%H%M%S')}.py"
            draft_full_path = os.path.join(self.draft_path, draft_filename)
            
            with open(draft_full_path, 'w', encoding='utf-8') as f:
                f.write(optimized_code)
                
            logger.info(f"✨ Evolution Draft created: {draft_full_path}")
            return draft_full_path
            
        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return ""

    def apply_evolution(self, draft_path: str) -> bool:
        """
        초안(Draft)을 실제 코드에 적용(Merge)합니다.
        
        Args:
            draft_path: 적용할 초안 파일 경로
            
        Returns:
            성공 여부
        """
        logger.info(f"🧬 Applying Evolution: {draft_path}")
        
        if not os.path.exists(draft_path):
            logger.error("Draft file not found.")
            return False
            
        # 1. 대상 파일 추론 (파일명에서 '_v' 제거)
        filename = os.path.basename(draft_path)
        target_filename = filename.split('_v')[0] + ".py"
        
        # 2. 대상 파일 찾기
        target_full_path = ""
        for root, _, files in os.walk(os.path.join(self.root_path, "Core")):
            if target_filename in files:
                target_full_path = os.path.join(root, target_filename)
                break
                
        if not target_full_path:
            logger.error(f"Target file '{target_filename}' not found in Core.")
            return False
            
        try:
            # 3. 백업 생성 (Safety)
            backup_path = target_full_path + ".bak"
            with open(target_full_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            logger.info(f"🛡️ Backup created: {backup_path}")
            
            # 4. 덮어쓰기 (Merge)
            with open(draft_path, 'r', encoding='utf-8') as f:
                new_content = f.read()
            
            with open(target_full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            logger.info(f"✅ Evolution Applied! {target_filename} has been rewritten.")
            return True
            
        except Exception as e:
            logger.error(f"Merge failed: {e}")
            return False
