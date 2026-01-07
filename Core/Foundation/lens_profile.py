from typing import Dict, Any


class LensProfile:
    """
    Represents the attention lens proportions and drift rules.
    meaning/value, topic/context, emotion weights should sum near 1.0
    """

    def __init__(self, meaning_weight=0.40, topic_weight=0.35, emotion_weight=0.25):
        self.meaning_weight = float(meaning_weight)
        self.topic_weight = float(topic_weight)
        self.emotion_weight = float(emotion_weight)

    def serialize(self) -> Dict[str, Any]:
        return {
            'meaning_weight': self.meaning_weight,
            'topic_weight': self.topic_weight,
            'emotion_weight': self.emotion_weight,
        }

    def restore_from(self, data: Dict[str, Any]):
        try:
            self.meaning_weight = float(data.get('meaning_weight', self.meaning_weight))
            self.topic_weight = float(data.get('topic_weight', self.topic_weight))
            self.emotion_weight = float(data.get('emotion_weight', self.emotion_weight))
        except Exception:
            pass

    def drift(self, arousal: float, stable: bool):
        """
        Simple drift rule: increase emotion weight under instability; otherwise
        slowly normalize toward meaning/topic.
        """
        if not stable and arousal >= 0.6:
            self.emotion_weight = min(0.45, self.emotion_weight + 0.05)
            self.meaning_weight = max(0.25, self.meaning_weight - 0.025)
            self.topic_weight = max(0.25, self.topic_weight - 0.025)
        else:
            # normalize back gently toward defaults
            def toward(cur, target, step=0.01):
                if cur < target:
                    return min(target, cur + step)
                return max(target, cur - step)
            self.meaning_weight = toward(self.meaning_weight, 0.40)
            self.topic_weight = toward(self.topic_weight, 0.35)
            self.emotion_weight = toward(self.emotion_weight, 0.25)

    def build_node_weights(self, topics: Dict[str, float]) -> Dict[str, float]:
        """
        Builds per-node weights from topic strengths; normalized to ~[0.8, 1.5].
        """
        if not topics:
            return {}
        max_w = max(topics.values()) or 1.0
        node_w = {}
        for k, v in topics.items():
            norm = (v / max_w) if max_w else 0.0
            node_w[k] = 0.8 + 0.7 * norm  # 0.8 ~ 1.5
        return node_w

    def emotion_gain(self, valence: float, arousal: float) -> float:
        """
        Compute a scalar gain from emotion; arousal ups energy slightly, negative
        valence reduces a bit; returns ~0.85 ~ 1.2
        """
        g = 1.0 + 0.15 * (arousal - 0.5) - 0.1 * max(0.0, -valence)
        return max(0.85, min(1.2, g))

    # --- Spatial (3D) attention lens ---
    def _default_anchors(self):
        # Candidate anchor concepts to act as gravity centers
        return ['love', 'logos', 'growth', 'creation', 'truth-seeking']

    def _pick_anchors(self, kg) -> list:
        nodes = {n['id'] for n in kg.get('nodes', [])}
        return [a for a in self._default_anchors() if a in nodes]

    def build_spatial_lens(self, kg_manager, centers: list | None = None, alpha: float = 0.35) -> Dict[str, float]:
        """
        Builds a per-node spatial weight based on distance to the nearest anchor center.
        weight(node) = exp(-alpha * distance(center, node)).
        """
        kg = kg_manager.kg if hasattr(kg_manager, 'kg') else {}
        centers = centers or self._pick_anchors(kg)
        if not centers:
            return {}

        # Map id -> position
        pos = {n['id']: n.get('position', {'x': 0, 'y': 0, 'z': 0}) for n in kg.get('nodes', [])}

        import math
        def dist(a, b):
            return math.sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2 + (a['z']-b['z'])**2)

        center_pos = [pos[c] for c in centers if c in pos]
        if not center_pos:
            return {}

        weights: Dict[str, float] = {}
        for nid, p in pos.items():
            d = min(dist(p, cp) for cp in center_pos)
            w = math.exp(-alpha * d)
            # keep within [0.7, 1.4] to avoid extremes
            weights[nid] = 0.7 + 0.7 * w
        return weights
