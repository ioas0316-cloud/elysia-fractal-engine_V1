"""
ReadingCoach

Purpose: Provide offline reading utilities for summarization and feature
extraction (characters, themes) without external APIs. Uses lightweight
frequency and heuristic methods to stay deterministic and fast.

Role: Agent Sophia component supporting journaling and book report flows.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import List, Dict


class ReadingCoach:
    """Offline summarization and extraction helper."""

    SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
    WORD_RE = re.compile(r"[A-Za-z가-힣0-9']+")

    def _sentences(self, text: str) -> List[str]:
        text = text.strip()
        if not text:
            return []
        # Basic sentence splitting by punctuation; fallback to lines
        sents = re.split(self.SENT_SPLIT, text)
        if len(sents) <= 1:
            sents = [s for s in text.splitlines() if s.strip()]
        return [s.strip() for s in sents if s.strip()]

    def _keywords(self, text: str, top_k: int = 20) -> List[str]:
        words = [w.lower() for w in self.WORD_RE.findall(text)]
        counts = Counter(words)
        # Remove very short tokens
        for k in list(counts.keys()):
            if len(k) <= 2:
                del counts[k]
        return [w for w, _ in counts.most_common(top_k)]

    def summarize_text(self, text: str, max_sentences: int = 5) -> str:
        sents = self._sentences(text)
        if len(sents) <= max_sentences:
            return " ".join(sents)

        # Sentence scoring by keyword overlap (TextRank-style lite)
        keywords = set(self._keywords(text, top_k=30))
        scored = []
        for i, s in enumerate(sents):
            tokens = set(w.lower() for w in self.WORD_RE.findall(s))
            score = len(tokens & keywords) + 0.1  # small bias to avoid zeros
            scored.append((score, i, s))
        scored.sort(reverse=True)
        chosen = sorted(scored[:max_sentences], key=lambda x: x[1])
        return " ".join(s for _, _, s in chosen)

    def extract_characters(self, text: str, top_k: int = 8) -> List[str]:
        # Heuristic: proper-like tokens (Capitalized ASCII words) with frequency
        tokens = self.WORD_RE.findall(text)
        candidates = [t for t in tokens if t[:1].isupper() and len(t) > 2]
        counts = Counter(candidates)
        # Filter out common sentence-start artefacts by threshold
        common = [w for w, c in counts.most_common(50) if c >= 2]
        # Deduplicate near-duplicates (case-insensitive)
        seen = set()
        dedup: List[str] = []
        for w in common:
            k = w.lower()
            if k not in seen:
                seen.add(k)
                dedup.append(w)
        return dedup[:top_k]

    def extract_themes(self, text: str, top_k: int = 5) -> List[str]:
        # Map of simple keyword groups to theme labels
        THEME_MAP = {
            "love": ["love", "romance", "heart"],
            "betrayal": ["betrayal", "deceit", "lie"],
            "growth": ["grow", "learn", "change", "transformation"],
            "freedom": ["free", "freedom", "escape"],
            "hope": ["hope", "light", "future"],
            "conflict": ["war", "fight", "conflict", "battle"],
        }
        text_low = text.lower()
        scores: Dict[str, int] = {k: 0 for k in THEME_MAP}
        for theme, keys in THEME_MAP.items():
            for kw in keys:
                scores[theme] += text_low.count(kw)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [t for t, s in ranked if s > 0][:top_k]

    # --- Advanced (lightweight) helpers ---
    def resolve_coreference(self, text: str, characters: List[str]) -> dict:
        """
        Very simple heuristic: map pronouns to the most recent named character seen.
        Returns a dict of pronoun->character for the last seen entity.
        """
        pronouns = ["he", "she", "they", "him", "her", "them"]
        last = None
        mapping = {}
        tokens = self.WORD_RE.findall(text)
        for tok in tokens:
            if tok in characters:
                last = tok
            elif tok.lower() in pronouns and last:
                mapping[tok.lower()] = last
        return mapping

    def extract_conflicts(self, text: str, characters: List[str]) -> List[dict]:
        """
        Extract simple character-to-character conflicts from sentences containing
        conflict keywords and two or more character mentions.
        Returns list of dicts: {a, b, type, snippet}.
        """
        conflict_keywords = [
            "versus", "against", "betray", "fight", "fought", "battle",
            "argue", "argument", "rival", "rivalry", "kill", "murder"
        ]
        sents = self._sentences(text)
        conflicts: List[dict] = []
        for s in sents:
            low = s.lower()
            if any(kw in low for kw in conflict_keywords):
                # find character mentions in sentence (case-sensitive match)
                present = [c for c in characters if c in s]
                if len(present) >= 2:
                    # pairwise conflicts
                    for i in range(len(present)):
                        for j in range(i+1, len(present)):
                            conflicts.append({
                                "a": present[i],
                                "b": present[j],
                                "type": "conflict",
                                "snippet": s[:180]
                            })
        return conflicts

    def sentence_cooccurrence_pairs(self, text: str, characters: List[str]) -> List[tuple]:
        """Return co-occurring character pairs per sentence as undirected edges."""
        sents = self._sentences(text)
        pairs = set()
        for s in sents:
            present = [c for c in characters if c in s]
            for i in range(len(present)):
                for j in range(i+1, len(present)):
                    a, b = sorted((present[i], present[j]))
                    pairs.add((a, b))
        return sorted(pairs)
