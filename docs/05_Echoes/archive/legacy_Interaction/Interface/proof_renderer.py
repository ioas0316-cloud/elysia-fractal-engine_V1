"""
ProofRenderer

Renders a simple visual summary of a Proof into a PNG image.
Focuses on readability and traceability of steps.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont

try:
    DEFAULT_FONT = ImageFont.load_default()
except Exception:
    DEFAULT_FONT = None


class ProofRenderer:
    def __init__(self, output_dir: str = "data/proofs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def render(self, proof, filename: Optional[str] = None) -> str:
        text_lines = []
        text_lines.append(f"Statement: {proof.statement}")
        text_lines.append("")
        text_lines.append("Steps:")
        for s in proof.steps:
            head = f"{s.index}. [{s.action}] {s.detail}"
            text_lines.append(head)
            if s.result is not None:
                text_lines.append(f"    -> {s.result}")
        text_lines.append("")
        verdict_line = f"Verdict: {'VALID' if proof.valid else 'INVALID'} — {proof.verdict}"
        text_lines.append(verdict_line)

        # Render
        line_height = 18
        width = 900
        height = max(120, (len(text_lines) + 2) * line_height + 20)
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        y = 10
        for line in text_lines:
            draw.text((10, y), line, fill=(10, 10, 10), font=DEFAULT_FONT)
            y += line_height

        if filename is None:
            # Derive a safe filename from statement
            safe = proof.statement.replace(" ", "_").replace("/", "_").replace("*", "x")
            filename = f"proof_{safe[:60]}.png"

        out_path = self.output_dir / filename
        img.save(out_path)
        return str(out_path)

