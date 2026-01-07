"""
Planning Cortex (계획 피질)
=========================

원본: Legacy/Project_Sophia/planning_cortex.py
마이그레이션: 2025-12-15

복잡한 고수준 목표를 실행 가능한 도구 호출 시퀀스로 분해합니다.
Elysia의 다단계 계획 수립 및 실행 능력의 핵심입니다.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

try:
    from Core.Foundation.gemini_api import generate_text
except ImportError:
    generate_text = None


class PlanningCortex:
    """
    Breaks down complex, high-level goals into a sequence of executable tool calls.
    This cortex is the heart of Elysia's ability to form and execute multi-step plans.
    """

    def __init__(self, core_memory=None, action_cortex=None):
        self.core_memory = core_memory
        self.action_cortex = action_cortex
        self.logger = logging.getLogger("PlanningCortex")

    def develop_plan(self, goal: str) -> List[Dict[str, Any]]:
        """
        Develops a step-by-step plan to achieve a given goal.

        Args:
            goal: The high-level goal to achieve.

        Returns:
            A list of tool calls (dictionaries) representing the plan.
        """
        self.logger.info(f"Developing plan for goal: {goal}")
        
        if generate_text is None:
            self.logger.warning("LLM not available for planning")
            return []
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        prompt = f"""
You are the Planning Cortex of an advanced AI named Elysia.
Your task is to break down a high-level goal into a sequence of specific tool calls.

Current Time: {current_time}
Goal: {goal}

Available Tools:
- read_file(filepath): Read a file
- write_to_file(filepath, content): Write to a file
- list_dir(directory_path): List directory contents
- google_search(query): Search the web
- view_text_website(url): View a webpage
- get_current_time(): Get current time
- thought(content): Internal processing without tool

Instructions:
1. Analyze the goal and determine the necessary steps.
2. Output the plan as a JSON list of objects.
3. Each step should have 'tool_name' and 'parameters'.

Example Output Format:
[
    {{"tool_name": "get_current_time", "parameters": {{}}}},
    {{"tool_name": "write_to_file", "parameters": {{"filepath": "log.txt", "content": "..."}}}}
]

Generate the JSON plan now (raw JSON only, no markdown):
"""
        try:
            response_text = generate_text(prompt)
            cleaned_text = response_text.strip()
            
            # Clean up markdown formatting if present
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
                
            plan = json.loads(cleaned_text)
            self.logger.info(f"Plan generated with {len(plan)} steps.")
            return plan
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse plan JSON: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error developing plan: {e}")
            return []

    def execute_plan(self, plan: List[Dict[str, Any]], executor=None) -> List[Dict[str, Any]]:
        """
        Executes a plan step by step.
        
        Args:
            plan: List of tool calls
            executor: Function to execute each tool call
            
        Returns:
            List of results from each step
        """
        results = []
        for i, step in enumerate(plan):
            self.logger.info(f"Executing step {i+1}/{len(plan)}: {step.get('tool_name')}")
            
            if executor:
                try:
                    result = executor(step['tool_name'], step.get('parameters', {}))
                    results.append({"step": i+1, "status": "success", "result": result})
                except Exception as e:
                    results.append({"step": i+1, "status": "error", "error": str(e)})
            else:
                results.append({"step": i+1, "status": "skipped", "reason": "no executor"})
        
        return results


# Singleton
_planning_cortex: Optional[PlanningCortex] = None

def get_planning_cortex() -> PlanningCortex:
    global _planning_cortex
    if _planning_cortex is None:
        _planning_cortex = PlanningCortex()
    return _planning_cortex
