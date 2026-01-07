from dataclasses import dataclass, field
from pyquaternion import Quaternion
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class Experience:
    truth: float = 1.0
    emotion: float = 0.0
    causality: float = 0.0
    beauty: float = 0.0
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimelineNode:
    id: str
    timestamp: str
    q: Quaternion
    experience: Experience
    parent_id: Optional[str] = None
    branch_id: str = "main"
    note: Optional[str] = None
    scopes: List[str] = field(default_factory=list)  # 부분 시간 조작 대상(개념/영역 태그)


@dataclass
class Branch:
    id: str
    name: str
    origin_node_id: Optional[str] = None
    nodes: List[str] = field(default_factory=list)


class ElysiaDivineEngineV2:
    """
    ElysiaDivineEngine V2:
    - 전역 타임라인 + 브랜치 (불변 기록)
    - scope(concept_id 등) 단위 '부분 시간 조작' 지원
    - 부분 되감기/운명 편집은 해당 scope에 태깅된 노드 시퀀스 위에서만 작동
    """

    def __init__(self):
        self.nodes: Dict[str, TimelineNode] = {}
        self.branches: Dict[str, Branch] = {}
        self.current_branch_id: str = "main"
        self.current_node_id: Optional[str] = None

        # scope별 "현재 포인터"
        self.scope_current_node: Dict[str, str] = {}

        # 메인 브랜치 생성
        self.branches["main"] = Branch(id="main", name="Main Timeline")

    # ===== 내부 유틸 =====

    def _experience_to_quaternion(self, exp: Experience) -> Quaternion:
        return Quaternion(exp.truth, exp.emotion, exp.causality, exp.beauty).normalised

    def _add_node(
        self,
        exp: Experience,
        branch_id: Optional[str] = None,
        parent_id: Optional[str] = None,
        note: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ) -> TimelineNode:
        if branch_id is None:
            branch_id = self.current_branch_id

        q = self._experience_to_quaternion(exp)
        ts = datetime.now().isoformat()
        node_id = str(uuid.uuid4())

        node = TimelineNode(
            id=node_id,
            timestamp=ts,
            q=q,
            experience=exp,
            parent_id=parent_id,
            branch_id=branch_id,
            note=note,
            scopes=scopes or [],
        )

        self.nodes[node_id] = node
        self.branches.setdefault(branch_id, Branch(id=branch_id, name=f"Branch:{branch_id}"))
        self.branches[branch_id].nodes.append(node_id)

        self.current_branch_id = branch_id
        self.current_node_id = node_id

        # scope 포인터 갱신
        for s in node.scopes:
            self.scope_current_node[s] = node_id

        # print(f"⏳ [INGEST] {ts} @ {branch_id} → 노드 {node_id} (scopes={node.scopes})")
        return node

    def _get_current_node(self) -> Optional[TimelineNode]:
        return self.nodes.get(self.current_node_id) if self.current_node_id else None

    def _get_scope_current_node(self, scope: str) -> Optional[TimelineNode]:
        nid = self.scope_current_node.get(scope)
        return self.nodes.get(nid) if nid else None

    def _branch_from(self, base_node_id: str, name: Optional[str] = None) -> Branch:
        branch_id = str(uuid.uuid4())
        if name is None:
            name = f"Branch@{base_node_id[:8]}"
        br = Branch(id=branch_id, name=name, origin_node_id=base_node_id)
        self.branches[branch_id] = br
        # print(f"🌿 [BRANCH] {branch_id} 생성 (origin={base_node_id})")
        return br

    def _scope_sequence(self, scope: str, branch_id: Optional[str] = None) -> List[str]:
        """
        특정 scope에 태깅된 노드들만 시간순/브랜치 기준으로 추출.
        branch_id를 주면 해당 브랜치 내에서만 필터링.
        """
        seq = []
        for nid, node in self.nodes.items():
            if scope in node.scopes:
                if branch_id is None or node.branch_id == branch_id:
                    seq.append((node.timestamp, nid))
        seq.sort(key=lambda x: x[0])
        return [nid for _, nid in seq]

    # ===== 전역 인터페이스 =====

    def ingest(self, experience_dict: Dict[str, Any],
               note: Optional[str] = None,
               scopes: Optional[List[str]] = None) -> TimelineNode:
        exp = Experience(
            truth=experience_dict.get("truth", 1.0),
            emotion=experience_dict.get("emotion", 0.0),
            causality=experience_dict.get("causality", 0.0),
            beauty=experience_dict.get("beauty", 0.0),
            meta=experience_dict.get("meta", {})
        )
        parent_id = self.current_node_id
        return self._add_node(exp, parent_id=parent_id, note=note, scopes=scopes)

    def rewind(self, steps: int = 1) -> Optional[TimelineNode]:
        node = self._get_current_node()
        if not node:
            return None

        br = self.branches[node.branch_id]
        try:
            idx = br.nodes.index(node.id)
        except ValueError:
            return None

        new_idx = max(0, idx - steps)
        self.current_node_id = br.nodes[new_idx]
        new_node = self.nodes[self.current_node_id]
        return new_node

    def fast_forward(self, steps: int = 1) -> Optional[TimelineNode]:
        node = self._get_current_node()
        if not node:
            return None

        br = self.branches[node.branch_id]
        try:
            idx = br.nodes.index(node.id)
        except ValueError:
            return None

        new_idx = min(len(br.nodes) - 1, idx + steps)
        self.current_node_id = br.nodes[new_idx]
        new_node = self.nodes[self.current_node_id]
        return new_node

    def simulate_future(self, experience_dict: Dict[str, Any]) -> Quaternion:
        base = self._get_current_node()
        if not base:
            base = Experience()

        exp = Experience(
            truth=experience_dict.get("truth", base.experience.truth),
            emotion=experience_dict.get("emotion", base.experience.emotion),
            causality=experience_dict.get("causality", base.experience.causality),
            beauty=experience_dict.get("beauty", base.experience.beauty),
            meta=experience_dict.get("meta", {})
        )
        q = self._experience_to_quaternion(exp)
        return q

    def edit_fate(self, new_experience_dict: Dict[str, Any],
                  note: Optional[str] = "Fate Edit") -> TimelineNode:
        base = self._get_current_node()
        if not base:
            return self.ingest(new_experience_dict, note=note)

        new_branch = self._branch_from(base_node_id=base.id)
        self.current_branch_id = new_branch.id
        self.current_node_id = base.id

        node = self.ingest(new_experience_dict, note=note)
        return node

    # ===== 부분 시간 조작 (핵심) =====

    def rewind_scope(self, scope: str, steps: int = 1) -> Optional[TimelineNode]:
        cur = self._get_scope_current_node(scope)
        if not cur:
            return None

        seq = self._scope_sequence(scope, branch_id=cur.branch_id)
        if cur.id not in seq:
            return None

        idx = seq.index(cur.id)
        new_idx = max(0, idx - steps)
        new_id = seq[new_idx]
        self.scope_current_node[scope] = new_id
        node = self.nodes[new_id]
        return node

    def fast_forward_scope(self, scope: str, steps: int = 1) -> Optional[TimelineNode]:
        cur = self._get_scope_current_node(scope)
        if not cur:
            return None

        seq = self._scope_sequence(scope, branch_id=cur.branch_id)
        if cur.id not in seq:
            return None

        idx = seq.index(cur.id)
        new_idx = min(len(seq) - 1, idx + steps)
        new_id = seq[new_idx]
        self.scope_current_node[scope] = new_id
        node = self.nodes[new_id]
        return node

    def edit_fate_scope(self, scope: str,
                        new_experience_dict: Dict[str, Any],
                        note: Optional[str] = None) -> TimelineNode:
        base = self._get_scope_current_node(scope) or self._get_current_node()
        if not base:
            return self.ingest(new_experience_dict, note=note, scopes=[scope])

        new_branch = self._branch_from(base_node_id=base.id,
                                       name=f"Scope:{scope}")
        self.current_branch_id = new_branch.id
        self.current_node_id = base.id

        node = self.ingest(new_experience_dict,
                           note=note or f"FateEdit:{scope}",
                           scopes=[scope])
        self.scope_current_node[scope] = node.id
        return node
