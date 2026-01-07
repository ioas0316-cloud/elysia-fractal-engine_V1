"""
Language Trajectory Analyzer
=============================
Analyzes language_progress.jsonl to detect:
- Path entropy (diversity of reasoning paths)
- Subject variance (how many distinct subjects are explored)
- Intent distribution (reflect vs. respond balance)
- Convergence drift (deviation from initial distribution)

Warns if the agent is over-converging on a single topic.
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter, defaultdict
import math

# Setup path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger("LanguageTrajectory")


class LanguageTrajectoryAnalyzer:
    """Analyze language learning progression over time."""

    def __init__(self, log_path: str = "logs/language_progress.jsonl"):
        self.log_path = Path(log_path)
        self.records: List[Dict[str, Any]] = []
        self.load()

    def load(self):
        """Load JSONL records from log file."""
        if not self.log_path.exists():
            logger.warning(f"⚠️  Log file not found: {self.log_path}")
            return

        with open(self.log_path, "r", encoding="utf-8") as fh:
            for line_num, line in enumerate(fh, start=1):
                try:
                    record = json.loads(line.strip())
                    self.records.append(record)
                except json.JSONDecodeError as e:
                    logger.warning(f"⚠️  Line {line_num}: {e}")

        logger.info(f"✅ Loaded {len(self.records)} trajectory records")

    def analyze_path_entropy(self) -> Dict[str, Any]:
        """Calculate entropy of reasoning paths over time."""
        if not self.records:
            return {}

        path_entropy_over_time = []
        all_paths = Counter()

        for record in self.records:
            details = record.get("details", [])
            paths = [tuple(d.get("path", [])) for d in details]
            path_counter = Counter(paths)
            all_paths.update(path_counter)

            # Calculate Shannon entropy for this batch
            total = sum(path_counter.values())
            entropy = 0.0
            if total > 0:
                for count in path_counter.values():
                    p = count / total
                    if p > 0:
                        entropy -= p * math.log2(p)

            path_entropy_over_time.append(entropy)

        avg_entropy = sum(path_entropy_over_time) / len(path_entropy_over_time) if path_entropy_over_time else 0.0
        max_entropy = max(path_entropy_over_time) if path_entropy_over_time else 0.0
        min_entropy = min(path_entropy_over_time) if path_entropy_over_time else 0.0

        return {
            "average": avg_entropy,
            "max": max_entropy,
            "min": min_entropy,
            "trend": path_entropy_over_time,
            "unique_paths": len(all_paths),
            "most_common_paths": all_paths.most_common(5)
        }

    def analyze_subject_variance(self) -> Dict[str, Any]:
        """Analyze diversity of subjects being explored."""
        if not self.records:
            return {}

        subject_counts = Counter()
        subject_appearances_by_record = []

        for record in self.records:
            details = record.get("details", [])
            subjects = [d.get("subject") for d in details]
            unique_subjects = set(s for s in subjects if s)
            subject_appearances_by_record.append(len(unique_subjects))

            for subject in unique_subjects:
                subject_counts[subject] += 1

        avg_subjects_per_record = (
            sum(subject_appearances_by_record) / len(subject_appearances_by_record)
            if subject_appearances_by_record
            else 0.0
        )

        return {
            "unique_subjects": len(subject_counts),
            "avg_subjects_per_record": avg_subjects_per_record,
            "subject_distribution": subject_counts.most_common(10),
            "top_subject": subject_counts.most_common(1)[0][0] if subject_counts else "None",
            "top_subject_percentage": (
                (subject_counts.most_common(1)[0][1] / sum(subject_counts.values()) * 100)
                if subject_counts else 0.0
            )
        }

    def analyze_intent_distribution(self) -> Dict[str, Any]:
        """Analyze balance between intents (reflect, respond, etc.)."""
        if not self.records:
            return {}

        intent_counts = Counter()

        for record in self.records:
            details = record.get("details", [])
            for detail in details:
                intent = detail.get("intent", "unknown")
                intent_counts[intent] += 1

        total = sum(intent_counts.values())
        intent_dist = {intent: (count / total * 100) for intent, count in intent_counts.items()}

        return {
            "total_intents": total,
            "distribution": intent_dist,
            "dominant_intent": intent_counts.most_common(1)[0][0] if intent_counts else "None",
            "dominant_percentage": (
                (intent_counts.most_common(1)[0][1] / total * 100)
                if intent_counts else 0.0
            )
        }

    def analyze_convergence_drift(self) -> Dict[str, Any]:
        """Detect if the agent is converging on narrow topics (drift)."""
        if not self.records:
            return {}

        subject_variance_history = []

        for i, record in enumerate(self.records):
            details = record.get("details", [])
            subjects = set(d.get("subject") for d in details if d.get("subject"))
            subject_variance = len(subjects)
            subject_variance_history.append(subject_variance)

        # Calculate trend
        if len(subject_variance_history) > 1:
            first_half_avg = sum(subject_variance_history[: len(subject_variance_history) // 2]) / max(1, len(subject_variance_history) // 2)
            second_half_avg = sum(subject_variance_history[len(subject_variance_history) // 2:]) / max(1, len(subject_variance_history) - len(subject_variance_history) // 2)

            drift_score = (first_half_avg - second_half_avg) / max(first_half_avg, 1.0)
        else:
            first_half_avg = 0.0
            second_half_avg = 0.0
            drift_score = 0.0

        # Warn if converging significantly
        convergence_warning = drift_score > 0.3  # >30% reduction

        return {
            "first_half_variance": first_half_avg,
            "second_half_variance": second_half_avg,
            "drift_score": drift_score,
            "is_converging": convergence_warning,
            "variance_trend": subject_variance_history
        }

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive analysis report."""
        logger.info("\n📊 Analyzing language trajectory...")

        path_analysis = self.analyze_path_entropy()
        subject_analysis = self.analyze_subject_variance()
        intent_analysis = self.analyze_intent_distribution()
        convergence_analysis = self.analyze_convergence_drift()

        return {
            "total_records": len(self.records),
            "path_entropy": path_analysis,
            "subject_variance": subject_analysis,
            "intent_distribution": intent_analysis,
            "convergence_drift": convergence_analysis,
            "alerts": self._generate_alerts(
                path_analysis,
                subject_analysis,
                intent_analysis,
                convergence_analysis
            )
        }

    def _generate_alerts(self, path_analysis, subject_analysis, intent_analysis, convergence_analysis) -> List[str]:
        """Generate warnings based on analysis."""
        alerts = []

        # Alert on low path entropy
        if path_analysis.get("average", 0) < 0.5:
            alerts.append("⚠️  LOW PATH ENTROPY: Agent is repeating very similar reasoning paths. Consider diversifying curriculum.")

        # Alert on extreme subject concentration
        top_subject_pct = subject_analysis.get("top_subject_percentage", 0)
        if top_subject_pct > 70:
            alerts.append(f"⚠️  SUBJECT CONCENTRATION: {top_subject_pct:.1f}% of exploration is on '{subject_analysis.get('top_subject')}'. Try exposing to new concepts.")

        # Alert on convergence drift
        if convergence_analysis.get("is_converging"):
            drift = convergence_analysis.get("drift_score", 0)
            alerts.append(f"⚠️  CONVERGENCE DRIFT: Subject variance dropped {drift*100:.1f}%. Agent may be narrowing focus excessively.")

        # Alert on intent imbalance
        intent_dist = intent_analysis.get("distribution", {})
        dominant_pct = intent_analysis.get("dominant_percentage", 0)
        if dominant_pct > 85:
            alerts.append(f"⚠️  INTENT IMBALANCE: {dominant_pct:.1f}% are '{intent_analysis.get('dominant_intent')}'. Encourage variety in reasoning modes.")

        if not alerts:
            alerts.append("✅ Language trajectory looks healthy — good diversity and balanced exploration.")

        return alerts

    def save_report(self, output_path: str = None):
        """Save analysis report to JSON."""
        if output_path is None:
            import time
            output_path = f"logs/language_trajectory_{int(time.time())}.json"

        report = self.generate_report()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        logger.info(f"📋 Report saved to: {output_path}")

        return report


def main():
    """Run language trajectory analysis."""
    logger.info("\n" + "=" * 70)
    logger.info("LANGUAGE TRAJECTORY ANALYZER")
    logger.info("=" * 70 + "\n")

    analyzer = LanguageTrajectoryAnalyzer()

    if not analyzer.records:
        logger.error("❌ No records found. Exiting.")
        return

    report = analyzer.save_report()

    # Print summary
    print("\n" + "=" * 70)
    print("TRAJECTORY SUMMARY")
    print("=" * 70)

    print(f"\n📈 Path Entropy: avg={report['path_entropy'].get('average', 0):.3f}, unique_paths={report['path_entropy'].get('unique_paths', 0)}")
    print(f"📚 Subject Variance: {report['subject_variance'].get('unique_subjects', 0)} unique subjects, top='{report['subject_variance'].get('top_subject')}' ({report['subject_variance'].get('top_subject_percentage', 0):.1f}%)")
    print(f"💭 Intent Distribution: {report['intent_distribution'].get('dominant_intent')} ({report['intent_distribution'].get('dominant_percentage', 0):.1f}%)")

    print(f"\n🎯 Convergence Analysis:")
    print(f"   Variance (first half): {report['convergence_drift'].get('first_half_variance', 0):.2f}")
    print(f"   Variance (second half): {report['convergence_drift'].get('second_half_variance', 0):.2f}")
    print(f"   Drift Score: {report['convergence_drift'].get('drift_score', 0):.3f} {'(⚠️  CONVERGING)' if report['convergence_drift'].get('is_converging') else '(✅ OK)'}")

    print(f"\n⚡ ALERTS:")
    for alert in report.get("alerts", []):
        print(f"   {alert}")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    main()
