"""
Simple ingestion utility: split text into sentences, extract concepts via lexicon,
store into Hippocampus + WorldTree with phase metadata.

Usage (example):
    python Tools/ingest_phase.py --file data/sample.txt --min-words 3
"""

import argparse
import logging
import re
from typing import List, Dict

from Core.System.System.System.Kernel import kernel

logger = logging.getLogger("IngestPhase")


def split_sentences(text: str) -> List[str]:
    # Basic sentence splitter for demo purposes
    return [s.strip() for s in re.split(r"[.!?\\n]+", text) if s.strip()]


def extract_concepts(sentence: str, vocabulary: Dict[str, float]) -> List[str]:
    concepts = []
    lower = sentence.lower()
    for key in vocabulary:
        if key.lower() in lower:
            concepts.append(key)
    return list(set(concepts))


def ingest_sentences(sentences: List[str], min_words: int = 3, min_unique: int = 2, dedup: bool = True) -> int:
    voice = kernel.voice
    seen: set = set()
    count = 0
    for sent in sentences:
        tokens = sent.split()
        if len(tokens) < min_words:
            continue
        if len(set(tokens)) < min_unique:
            continue
        norm = sent.strip().lower()
        if dedup and norm in seen:
            continue
        seen.add(norm)
        concepts = extract_concepts(sent, voice.vocabulary)
        voice.memory.add_turn(sent, "")  # store raw context
        voice._update_knowledge_graphs(concepts)
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Text file to ingest")
    parser.add_argument("--min-words", type=int, default=3)
    parser.add_argument("--min-unique", type=int, default=2, help="Minimum unique tokens per sentence")
    parser.add_argument("--no-dedup", action="store_true", help="Disable simple sentence deduplication")
    args = parser.parse_args()

    with open(args.file, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = split_sentences(text)
    ingested = ingest_sentences(
        sentences,
        min_words=args.min_words,
        min_unique=args.min_unique,
        dedup=not args.no_dedup,
    )
    stats = kernel.hippocampus.get_statistics()
    phase_tags = len(kernel.hippocampus.get_phase_tags())
    logger.info(f"Ingested {ingested} sentences. Memory stats: {stats}, phase_tags={phase_tags}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
