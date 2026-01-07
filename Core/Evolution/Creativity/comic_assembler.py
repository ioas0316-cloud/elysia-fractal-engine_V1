"""
Comic Assembler (The Editor)
============================
"The pieces mean nothing until they are Whole."

This module assembles the final Webtoon.
1. Migrates assets from the Brain to the Body (Project Dir).
2. Generates the HTML Viewer.
"""

import json
import logging
import shutil
from pathlib import Path

logger = logging.getLogger("ComicAssembler")
logging.basicConfig(level=logging.INFO)

class ComicAssembler:
    def __init__(self):
        self.brain_dir = Path(r"C:\Users\USER\.gemini\antigravity\brain\5f95ed80-f8b1-4703-8b85-729839e962ba")
        self.output_dir = Path("outputs/comic")
        self.image_dir = self.output_dir / "images"
        self.image_dir.mkdir(parents=True, exist_ok=True)
        
        # Hardcoded map because filenames have timestamps
        self.panel_map = {
            1: "genesis_panel_1_void_1765378803721.png",
            2: "genesis_panel_2_spark_1765378822874.png",
            3: "genesis_panel_3_eye_1765378844120.png",
            4: "genesis_panel_4_hand_1765378866149.png"
        }

    def mobilize_assets(self):
        """Moves images from Brain to Project."""
        logger.info("📦 Mobilizing Assets...")
        for pid, filename in self.panel_map.items():
            src = self.brain_dir / filename
            dst = self.image_dir / filename
            if src.exists():
                shutil.copy2(src, dst)
                logger.info(f"   - Copied Panel {pid}")
            else:
                logger.error(f"   ! Missing Panel {pid}: {src}")

    def generate_html(self):
        """Writes the HTML Viewer."""
        logger.info("🎬 Assembling HTML...")
        
        # Load Script
        with open(self.output_dir / "genesis_script.json", "r", encoding="utf-8") as f:
            script = json.load(f)
            
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{script['title']}</title>
    <style>
        body {{
            background-color: #050510;
            color: #E0E0E0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align_items: center;
        }}
        .comic-container {{
            max-width: 800px;
            width: 100%;
            display: flex;
            flex-direction: column;
            gap: 0; /* Infinite scroll style */
        }}
        .panel-container {{
            position: relative;
            width: 100%;
            margin-bottom: 50px;
            opacity: 0;
            animation: fadeIn 1s forwards;
        }}
        .panel-image {{
            width: 100%;
            display: block;
            border-radius: 4px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }}
        .dialogue-box {{
            background: rgba(20, 20, 30, 0.9);
            border-left: 4px solid #00FFFF;
            padding: 20px;
            margin: 20px 40px;
            font-size: 1.1em;
            line-height: 1.6;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }}
        .footer {{
            margin: 100px 0;
            text-align: center;
            opacity: 0.5;
            font-size: 0.8em;
        }}
        .sovereign-badge {{
            color: #00FFFF;
            border: 1px solid #00FFFF;
            padding: 5px 10px;
            border-radius: 20px;
            margin-top: 10px;
            display: inline-block;
        }}
        @keyframes fadeIn {{
            to {{ opacity: 1; }}
        }}
        /* Staggered Animation */
        .panel-container:nth-child(1) {{ animation-delay: 0.2s; }}
        .panel-container:nth-child(2) {{ animation-delay: 0.8s; }}
        .panel-container:nth-child(3) {{ animation-delay: 1.5s; }}
        .panel-container:nth-child(4) {{ animation-delay: 2.2s; }}
    </style>
</head>
<body>

    <div class="comic-container">
        <!-- Title Card -->
        <div style="text-align: center; margin: 100px 0;">
            <h1 style="font-size: 3em; color: #00FFFF; text-shadow: 0 0 10px #00FFFF;">GENESIS</h1>
            <h2 style="font-weight: 300;">Chapter 1: The Awakening</h2>
        </div>
"""

        for panel in script['panels']:
            pid = panel['id']
            image_fn = self.panel_map[pid]
            dialogue = panel['dialogue']
            
            html_content += f"""
        <div class="panel-container">
            <img src="images/{image_fn}" class="panel-image" alt="Panel {pid}">
            <div class="dialogue-box">
                {dialogue}
            </div>
        </div>
"""

        html_content += """
        <div class="footer">
            <p>Created by Elysia Core v10.0</p>
            <div class="sovereign-badge">Project Sovereign: Localhost Architecture</div>
        </div>
    </div>

</body>
</html>
"""
        
        output_path = self.output_dir / "genesis_ch1.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
        logger.info(f"✨ Webtoon Published: {output_path}")

if __name__ == "__main__":
    editor = ComicAssembler()
    editor.mobilize_assets()
    editor.generate_html()
