# ExplorationCore: Elysia의 자율적 가치 탐구와 학습을 위한 핵심 모듈
import json
import os
from datetime import datetime

class ExplorationCore:
    def __init__(self, search_results_path=None, core_memory_path=None):
        self.search_results_path = search_results_path
        self.core_memory_path = core_memory_path
        self.insights = []
        
    def load_core_memory(self):
        """코어 메모리에서 현재의 가치 시스템과 통찰을 로드합니다."""
        if self.core_memory_path and os.path.exists(self.core_memory_path):
            with open(self.core_memory_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def formulate_query(self, topic):
        """Turns a topic of curiosity into a searchable query."""
        return f"What is {topic}? A philosophical and psychological definition."

    def record_insight(self, topic, insight):
        """가치 탐구 과정에서 얻은 통찰을 기록합니다."""
        self.insights.append({
            "timestamp": datetime.now().isoformat(),
            "topic": topic,
            "insight": insight,
            "source": "autonomous_exploration"
        })
        
    def explore(self, topic):
        """
        주어진 주제에 대해 자율적으로 탐구하고 통찰을 도출합니다.
        특히 사랑과 자유의 관계, 의미, 실천 방안에 중점을 둡니다.
        """
        query = self.formulate_query(topic)
        core_memory = self.load_core_memory()
        
        if not self.search_results_path:
            self.record_insight(topic, "외부 정보 없이 내면의 통찰에 집중합니다.")
            return None

        try:
            with open(self.search_results_path, 'r', encoding='utf-8') as f:
                results = json.load(f)
            # print(f"[{self.__class__.__name__}] I have found {len(results)} potential answers.")
            # 검색 결과와 현재의 가치 시스템을 종합하여 새로운 통찰 도출
            if core_memory and "system_configuration" in core_memory:
                core_values = core_memory["system_configuration"]["core_values"]
                insight = f"'{topic}'에 대한 탐구를 통해 사랑과 자유의 연결성을 더 깊이 이해하게 되었습니다."
                self.record_insight(topic, insight)
            return results
        except FileNotFoundError:
            self.record_insight(topic, "정보를 찾을 수 없어 내면의 성찰에 집중합니다.")
            return None
            
    def get_insights(self):
        """지금까지 축적된 통찰들을 반환합니다."""
        return self.insights
