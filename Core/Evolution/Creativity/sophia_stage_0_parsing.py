# This file contains the expanded WisdomCortex.
import re
from kg_manager import KGManager


class WisdomCortex:
    def __init__(self):
        self.kg = KGManager()

    def read_and_digest(self, filepath):
        """
        Reads a text file and extracts knowledge using lightweight, rule-based
        heuristics. Also detects simple causal patterns (e.g., 'X causes Y') and
        merges the extracted knowledge into the project knowledge graph.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except FileNotFoundError:
            print(f"[{self.__class__.__name__}] The source of wisdom could not be found.")
            return None

        knowledge = {"nodes": set(), "edges": []}
        # Split into naive sentences
        sentences = re.split(r'[\.\n]+', text)

        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue

            # Heuristic: "X causes Y" or "X cause Y" or "X led to Y"
            m = re.search(r"([A-Za-z0-9_\s]+?)\s+(causes|cause|led to|leads to|results in|results from)\s+([A-Za-z0-9_\s]+)", s, re.IGNORECASE)
            if m:
                subj = m.group(1).strip().lower()
                rel = 'causes'
                obj = m.group(3).strip().lower()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': rel})
                continue

            # 한국어 인과관계 패턴
            m = re.search(r"([\w\s가-힣]+?)\s*(때문에|으로 인해|로 인해|때문|이라서|라서|이어서|여서|으로|로)\s*([\w\s가-힣]+)", s)
            if m:
                obj = m.group(1).strip()
                rel = 'causes'
                subj = m.group(3).strip()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': rel})
                continue
                
            # 한국어 결과 패턴
            m = re.search(r"([\w\s가-힣]+?)\s*(하면|면|으면|으니까|니까|으니|니|이니)\s*([\w\s가-힣]+)", s)
            if m:
                subj = m.group(1).strip()
                rel = 'causes'
                obj = m.group(3).strip()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': rel})
                continue

            # Heuristic: "X is Y"
            m = re.search(r"(\w[\w\s\-]+?)\s+is\s+([^,;]+)", s, re.IGNORECASE)
            if m:
                subj = m.group(1).strip().lower()
                obj = m.group(2).strip().lower()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': 'is'})
                continue
                
            # 한국어 is 패턴
            m = re.search(r"([\w\s가-힣]+?)\s*(은|는|이|가)\s*([\w\s가-힣]+?)(?:이다|다|입니다|습니다|죠|네요|네|군요|군|구나|구만|네용|네용~|임|임~)", s)
            if m:
                subj = m.group(1).strip()
                obj = m.group(3).strip()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': 'is'})
                continue
                
            # 한국어 특성 패턴
            m = re.search(r"([\w\s가-힣]+?)\s*(의)\s*([\w\s가-힣]+?)(?:은|는|이|가)\s*([\w\s가-힣]+)", s)
            if m:
                subj = m.group(1).strip()
                prop = m.group(3).strip()
                val = m.group(4).strip()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(val)
                knowledge['edges'].append({'from': subj, 'to': val, 'relation': prop})
                continue

            # Heuristic: "X involves Y"
            m = re.search(r"([\w\s]+?)\s+involves\s+(.+)", s, re.IGNORECASE)
            if m:
                subj = m.group(1).strip().lower()
                obj = m.group(2).strip().lower()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': 'involves'})

            # Korean heuristics
            # Pattern: "X는 Y이다/다/입니다" -> X is Y
            m = re.search(r"([가-힣A-Za-z0-9_\s\-]+?)(?:은|는|이|가)\s+(.+?)(?:이다|입니다|다|입니다\.|다\.|$)", s)
            if m:
                subj = m.group(1).strip().lower()
                obj = m.group(2).strip().lower()
                # avoid overly short captures
                if len(subj) > 0 and len(obj) > 0 and subj != obj:
                    knowledge['nodes'].add(subj)
                    knowledge['nodes'].add(obj)
                    knowledge['edges'].append({'from': subj, 'to': obj, 'relation': 'is'})
                    continue

            # Korean: 포함/포함한다/포함합니다 -> involves
            m = re.search(r"([가-힣A-Za-z0-9_\s\-]+?)\s+(포함|포함한다|포함합니다|포함되어)\s+(.+)", s)
            if m:
                subj = m.group(1).strip().lower()
                obj = m.group(3).strip().lower()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': 'involves'})
                continue

            # Korean causal cues: 야기하다, 초래하다, 원인이 되다, 결과로 이어지다
            m = re.search(r"([가-힣A-Za-z0-9_\s\-]+?)\s+(야기|야기한다|초래|초래한다|원인이 되|결과로 이어진)\s+(.+)", s)
            if m:
                subj = m.group(1).strip().lower()
                obj = m.group(3).strip().lower()
                knowledge['nodes'].add(subj)
                knowledge['nodes'].add(obj)
                knowledge['edges'].append({'from': subj, 'to': obj, 'relation': 'causes'})
                continue

        # Convert node set to list
        knowledge['nodes'] = list(knowledge['nodes'])

        # Merge into KG with provenance
        provenance = {'source': filepath}
        if knowledge['nodes'] or knowledge['edges']:
            self.kg.merge_knowledge(knowledge, provenance=provenance)
            return knowledge
        return None

    def parse_sentence(self, sentence):
        match = re.search(r"(\w+)\s+is\s+(.*)", sentence)
        if match:
            return {"subject": match.group(1), "object": match.group(2).strip()}
        return None
