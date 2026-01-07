from typing import List, Dict, Any
from collections import deque, Counter
import re


class WorkingMemory:
    """
    Maintains a lightweight working memory of recent utterances as
    keyword-level summaries for fast, offline context.
    """
    def __init__(self, size: int = 10):
        self.size = size
        self.buffer = deque(maxlen=size)

    def add(self, role: str, text: str):
        tokens = re.findall(r"\b\w+\b", text.lower())
        summary = {
            'role': role,
            'keywords': [w for w, _ in Counter(tokens).most_common(8)]
        }
        self.buffer.append(summary)

    def get_summary(self) -> List[Dict[str, Any]]:
        return list(self.buffer)

    def serialize(self) -> Dict[str, Any]:
        return {
            'size': self.size,
            'buffer': list(self.buffer)
        }

    def restore_from(self, data: Dict[str, Any]):
        try:
            self.size = int(data.get('size', self.size))
            self.buffer = deque(data.get('buffer', []), maxlen=self.size)
        except Exception:
            pass

    def prune(self, topic_strengths: Dict[str, float], keep: int = 6, protect_recent: int = 2, return_items: bool = False) -> Dict[str, Any]:
        """
        Prunes low-salience items from working memory to keep background load low.
        - Always keep the most recent `protect_recent` items.
        - Score older items by overlap with strong topics; keep top `keep - protect_recent`.
        Returns counts: {'kept': x, 'pruned': y}.
        """
        items = list(self.buffer)
        if len(items) <= keep:
            return {'kept': len(items), 'pruned': 0, 'pruned_items': []} if return_items else {'kept': len(items), 'pruned': 0}

        recent = items[-protect_recent:] if protect_recent > 0 else []
        older = items[:-protect_recent] if protect_recent > 0 else items

        # Build topic weight map
        strengths = topic_strengths or {}
        def score(it: Dict[str, Any]) -> float:
            kws = it.get('keywords', []) if isinstance(it, dict) else []
            return float(sum(strengths.get(k, 0.0) for k in kws))

        ranked = sorted(older, key=score, reverse=True)
        slots = max(0, keep - len(recent))
        selected = ranked[:slots]
        new_buf = selected + recent

        # derive pruned subset (from older pool only)
        removed = [it for it in older if it not in selected]
        pruned = len(items) - len(new_buf)
        self.buffer = deque(new_buf, maxlen=self.size)
        out = {'kept': len(new_buf), 'pruned': pruned}
        if return_items:
            out['pruned_items'] = removed
        return out


class TopicTracker:
    """
    Tracks topical focus with time-decay and reinforcement from echo activation.
    """
    def __init__(self, decay: float = 0.9):
        self.decay = decay
        self.topics: Dict[str, float] = {}

    def step(self):
        # Apply decay to all topics each turn
        for k in list(self.topics.keys()):
            self.topics[k] *= self.decay
            if self.topics[k] < 0.01:
                del self.topics[k]

    def reinforce_from_echo(self, echo: Dict[str, float]):
        for k, v in echo.items():
            self.topics[k] = self.topics.get(k, 0.0) + float(v)

    def snapshot(self) -> Dict[str, float]:
        return dict(sorted(self.topics.items(), key=lambda x: x[1], reverse=True)[:8])

    def serialize(self) -> Dict[str, Any]:
        return {
            'decay': self.decay,
            'topics': dict(self.topics)
        }

    def restore_from(self, data: Dict[str, Any]):
        try:
            self.decay = float(data.get('decay', self.decay))
            topics = data.get('topics', {})
            if isinstance(topics, dict):
                self.topics = {str(k): float(v) for k, v in topics.items()}
        except Exception:
            pass
