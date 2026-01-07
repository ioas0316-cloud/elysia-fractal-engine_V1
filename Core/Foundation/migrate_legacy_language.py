
import json
import math
import os
import sys

# 시스템 경로에 프로젝트 루트 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Legacy.Project_Sophia.primordial_language import PrimordialLanguageEngine, WordStats
from Core.Foundation.Mind.world_tree import WorldTree
from Core.Foundation.Mind.hyper_qubit import HyperQubit, QubitState

def convert_stats_to_qubit_state(stats: WordStats) -> QubitState:
    """
    '영혼 변환 규칙'에 따라 WordStats를 QubitState로 변환합니다. (개선된 공식)
    """
    # 기억 강도(avg_memory)는 '실재성/구체성'(alpha)에 직접 비례하도록 합니다.
    alpha_val = stats.avg_memory / 100.0

    # 사용 빈도(count)는 '관계/연결성'(beta)에 로그 비례하도록 하여,
    # 사용될수록 다른 개념과의 연결성이 강해짐을 표현합니다.
    beta_val = math.log1p(stats.count)

    # gamma와 delta는 작은 기본값을 부여하여 잠재성을 표현합니다.
    gamma_val = 0.1
    delta_val = 0.05

    # 복소수로 변환 (위상은 0으로 초기화)
    state = QubitState(
        alpha=complex(alpha_val, 0),
        beta=complex(beta_val, 0),
        gamma=complex(gamma_val, 0),
        delta=complex(delta_val, 0),
    )

    return state.normalize()

def run_migration():
    """
    레거시 언어 데이터를 HyperQubit 기반의 WorldTree로 마이그레이션합니다.
    """
    print("언어 마이그레이션을 시작합니다: 과거의 영혼에 새로운 육체를...")

    # 1. 과거의 언어 엔진 준비 및 '경험' 시뮬레이션
    suffix_map = {"joy": "ra", "fear": "ka", "curiosity": "ii"}
    language_engine = PrimordialLanguageEngine(suffix_map)

    # 과거에 이런 '경험'들이 있었다고 가정하고 Lexicon을 채웁니다.
    language_engine.observe({"target": "fire"}, "joy", "fire rara", 80.0)
    language_engine.observe({"target": "fire"}, "joy", "fire rara", 90.0) # count: 2, avg_mem: 85
    language_engine.observe({"target": "fire"}, "joy", "fire rarara", 75.0) # count: 1, avg_mem: 75
    language_engine.observe({"target": "fire"}, "fear", "fire ka", 95.0) # count: 1, avg_mem: 95
    language_engine.observe({"target": "water"}, "joy", "water rara", 60.0) # count: 1, avg_mem: 60
    language_engine.observe({"target": "water"}, "curiosity", "water iii", 85.0) # count: 1, avg_mem: 85

    print("과거 언어의 '경험' 시뮬레이션 완료. Lexicon 생성됨.")

    # 2. 새로운 의식의 나무(WorldTree) 준비
    world_tree = WorldTree()
    lang_root_id = world_tree.ensure_concept("PrimordialLanguage", parent_id=world_tree.root.id)
    print("새로운 WorldTree 생성 및 'PrimordialLanguage' 루트 노드 추가 완료.")

    # 3. 데이터 이주: Lexicon을 순회하며 HyperQubit으로 변환 및 WorldTree에 추가
    lexicon = language_engine.lexicon
    for (base, emotion), variants in lexicon.items():
        base_id = world_tree.ensure_concept(base, parent_id=lang_root_id)
        emotion_id = world_tree.ensure_concept(emotion, parent_id=base_id)

        for word, stats in variants.items():
            word_id = world_tree.ensure_concept(word, parent_id=emotion_id)
            qubit_state = convert_stats_to_qubit_state(stats)

            hyper_qubit = HyperQubit(
                concept_or_value=word,
                name=word,
                initial_content={"Point": word, "Line": f"{base}-{emotion} context"}
            )
            hyper_qubit.state = qubit_state

            word_node = world_tree._find_node(word_id)
            if word_node:
                setattr(word_node, 'qubit', hyper_qubit)

    print("모든 언어 데이터의 HyperQubit 변환 및 WorldTree 통합 완료.")

    # 4. 결과 저장
    output_path = "data/world_tree_with_language.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    def serialize_tree(node):
        node_dict = {
            "id": node.id,
            "concept": node.concept,
            "metadata": node.metadata,
            "depth": node.depth,
            "children": [serialize_tree(child) for child in node.children]
        }
        if hasattr(node, 'qubit') and isinstance(node.qubit, HyperQubit):
            node_dict['qubit'] = {
                'name': node.qubit.name,
                'state': {
                    'alpha': [node.qubit.state.alpha.real, node.qubit.state.alpha.imag],
                    'beta': [node.qubit.state.beta.real, node.qubit.state.beta.imag],
                    'gamma': [node.qubit.state.gamma.real, node.qubit.state.gamma.imag],
                    'delta': [node.qubit.state.delta.real, node.qubit.state.delta.imag],
                }
            }
        return node_dict

    final_tree_dict = serialize_tree(world_tree.root)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_tree_dict, f, ensure_ascii=False, indent=2)

    print(f"새로운 의식의 나무가 '{output_path}'에 저장되었습니다.")
    print("언어 마이그레이션이 성공적으로 완료되었습니다!")

if __name__ == "__main__":
    run_migration()
