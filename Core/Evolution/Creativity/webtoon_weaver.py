"""
Webtoon Weaver (The Conductor)
==============================
"The ink flows, the pages turn, the universe expands."

This module orchestrates the entire Webtoon Creation Process.
It connects the MIND (LiteraryCortex) to the HAND (WebtoonIllustrator).
"""

import logging
import time
from pathlib import Path
from Core.Evolution.Creativity.literary_cortex import LiteraryCortex
from Core.Evolution.Creativity.webtoon_illustrator import WebtoonIllustrator

# Optional External AI
try:
    from Core.Sensory.Network.comfy_adapter import ComfyAdapter
    HAS_COMFY = True
except ImportError:
    HAS_COMFY = False

logger = logging.getLogger("WebtoonWeaver")
logging.basicConfig(level=logging.INFO)

class WebtoonWeaver:
    def __init__(self):
        self.writer = LiteraryCortex()
        self.artist = WebtoonIllustrator()
        
        self.comfy = None
        if HAS_COMFY:
            self.comfy = ComfyAdapter()
            logger.info("🔌 ComfyUI Adapter Detected.")
        
    def produce_episode(self, concept_seed: str = "Resonance", episode_num: int = None):
        """
        Generates an Episode. Persistently tracks episode number.
        """
        logger.info(f"🚀 Starting Production: {concept_seed}")
        
        # 1. Write the Script (Mind) - Persistent
        bible = self.writer.seed_story(concept_seed)
        
        # Determine episode number if not forced
        target_ep = episode_num if episode_num is not None else bible.current_episode
        
        # If we are filling backwork, we might need to adjust logic, but assuming linear generation for now:
        script = self.writer.write_episode_script(bible, episode_num=target_ep)
        
        # 2. Draw the Panels (Hand)
        from Core.Evolution.Creativity.style_mimic import StyleMimic
        from Core.Intelligence.Physics_Waves.Holographic.synaptic_cortex import SynapticCortex
        
        self.mimic = StyleMimic()
        self.cortex = SynapticCortex()
        
        # Register Organs (Capabilities)
        # In a real run, this would be populated by the ModelDigester. 
        # Here we abstract "Methods" as Organs to demonstrate the Logic.
        self.cortex.register_organ("Redice-Engine", "Diffuser", {"Action": 0.9, "Romance": 0.4})
        self.cortex.register_organ("Ghibli-Engine", "Diffuser", {"Peace": 0.9, "Action": 0.2})
        self.cortex.register_organ("Default-Engine", "Diffuser", {"Balanced": 0.8})
        
        panel_map = {} # seq -> (image_source, dialogue)
        
        for scene in script:
            filename = f"ep{target_ep}_panel_{scene.sequence_id}_{int(time.time())}.png"
            rendered_src = None
            
            # 1. Sense the Mood (Energy)
            mood_energy = 0.5
            if "!" in scene.dialogue or "Attack" in scene.visual_prompt: mood_energy = 0.9
            if "..." in scene.dialogue or "Quiet" in scene.visual_prompt: mood_energy = 0.2
            
            # 2. Consult Synaptic Cortex for Best Tool
            task_type = "Action" if mood_energy > 0.7 else "Peace" if mood_energy < 0.3 else "Balanced"
            best_engine = self.cortex.select_best_organ(task_type, "Diffuser")
            
            # 3. Adapt Parameters (Organic Fluidity)
            optimal_cfg = self.cortex.adapt_parameter(best_engine, "cfg", mood_energy)
            optimal_steps = int(20 + (mood_energy * 10)) # More energy = more detail/steps
            
            # Determine Style
            style_name = self.mimic.suggest_style(scene.visual_prompt)
            style_prompt = self.mimic.get_style_prompt(style_name)
            
            # Construct Prompt
            prompt = f"{style_prompt}, {scene.visual_prompt}"
            if "[SYSTEM]" in scene.dialogue:
                 prompt += ", game ui, blue holographic interface, glowing text, digital hud, system window"
                 
            logger.info(f"🎨 Synaptic Plan: Tool={best_engine} | CFG={optimal_cfg:.1f} | Mood={task_type}")

            # Hybrid Rendering Logic
            if self.comfy and self.comfy.connect():
                logger.info("⚡ Generating with Sovereign AI (ComfyUI)...")
                
                # Dynamic Physics from Cortex
                physics = {
                    "cfg": optimal_cfg,
                    "steps": optimal_steps,
                    "sampler_name": "dpmpp_2m" if mood_energy > 0.6 else "euler"
                }

                # Generate
                gen_filename = self.comfy.generate_sync(prompt, overrides=physics)
                
                if gen_filename:
                    rendered_src = f"http://127.0.0.1:8188/view?filename={gen_filename}&type=output"
                    # Reinforce Behavior (Simulated Reward)
                    self.cortex.organs[best_engine].update_personality(task_type, True)
            
            # Fallback to Vector Pen
            if not rendered_src:
                local_path = self.artist.draw_panel(
                    filename=filename,
                    scene_description=f"{scene.visual_prompt}. [Mode: {best_engine}]", 
                    dialogue=scene.dialogue
                )
                rendered_src = Path(local_path).name # Just the filename for local
            
            panel_map[scene.sequence_id] = (rendered_src, scene.dialogue)
            time.sleep(0.5) 
            
        # 3. Assemble (Publishing)
        self._publish_html(f"{bible.title} - Episode {target_ep}", panel_map, target_ep)

    def _determine_physics(self, scene) -> dict:
        """
        Maps Narrative Mood -> Generative Physics (Sampler/CFG).
        """
        text = (scene.visual_prompt + scene.dialogue).lower()
        
        # 1. Rigid Order (System Windows)
        if "system" in text or "window" in text or "hud" in text:
            return {
                "cfg": tuple(random.uniform(11.0, 13.0) for _ in range(1))[0], 
                "sampler_name": "euler", 
                "steps": random.randint(18, 22)
            }
            
        # 2. Chaos / Action
        if any(w in text for w in ["attack", "battle", "blood", "kill", "explosion", "fight"]):
            # Higher variance for chaos
            return {
                "cfg": tuple(random.uniform(8.0, 10.0) for _ in range(1))[0], 
                "sampler_name": "dpmpp_2s_ancestral", 
                "steps": random.randint(22, 28)
            }
            
        # 3. Mystery / Magic
        if any(w in text for w in ["magic", "spell", "dark", "glow", "aura"]):
            return {
                "cfg": tuple(random.uniform(7.0, 9.0) for _ in range(1))[0], 
                "sampler_name": "dpmpp_2m", 
                "steps": random.randint(24, 30)
            }
            
        # 4. Default Harmony
        # Soft variance
        return {
            "cfg": tuple(random.uniform(6.5, 7.5) for _ in range(1))[0], 
            "sampler_name": "euler", 
            "steps": random.randint(20, 25)
        }
        
    def _publish_html(self, title: str, panel_map: dict, episode_num: int):
        """
        Manhwa-Style Vertical Scroll Publisher.
        Implements Dynamic Pacing (Gutter Spacing) and Seamless Layout.
        """
        output_dir = Path("outputs/comic")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as specific episode AND latest
        filename = f"episode_{episode_num:03d}.html"
        html_path = output_dir / filename
        latest_path = output_dir / "latest_episode.html"
        
        mode = "✨ AI-Enhanced High Definition" if (self.comfy and self.comfy.connect()) else "📐 Vector Abstract (Concept Draft)"
        
        html = f"""
        <html>
        <head>
            <title>{title}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&family=Nanum+Pen+Script&family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
            <style>
                body {{ 
                    background: #121212; 
                    display: flex; 
                    flex-direction: column; 
                    align-items: center; 
                    padding: 0; 
                    margin: 0;
                    font-family: 'Nanum Gothic', sans-serif; 
                }}
                
                .webtoon-canvas {{
                    max-width: 800px;
                    width: 100%;
                    background: #000;
                    box-shadow: 0 0 50px rgba(0,0,0,0.5);
                }}

                .panel-container {{ 
                    position: relative; 
                    width: 100%; 
                    display: flex;
                    justify-content: center;
                    background: #000; /* Seamless transition */
                }}
                
                img {{ 
                    width: 100%; 
                    display: block; 
                    /* No border for seamless flow */
                }}
                
                /* Dynamic Gutter Spacing (Pacing) */
                .gap-zero   {{ margin-bottom: 0px; }}
                .gap-small  {{ margin-bottom: 20px; }}   /* Action Sequence */
                .gap-medium {{ margin-bottom: 80px; }}   /* Standard Dialogue */
                .gap-large  {{ margin-bottom: 200px; }}  /* Emotional Pause / Time Pass */
                
                /* Dialogue Components */
                .dialogue-box {{ 
                    background: rgba(20, 20, 20, 0.9); 
                    color: #fff; 
                    padding: 20px; 
                    text-align: center; 
                    font-size: 1.1em; 
                    line-height: 1.6;
                    border-bottom: 1px solid #333;
                    width: 90%;
                    margin: 0 auto;
                    border-radius: 0 0 10px 10px;
                    position: relative;
                    top: -5px;
                }}

                /* Typography Styles */
                .system {{
                    font-family: 'Orbitron', sans-serif;
                    background: rgba(0, 20, 50, 0.95);
                    color: #00FFFF;
                    border: 1px solid #00FFFF;
                    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }}
                .thought {{
                    font-family: 'Nanum Pen Script', cursive;
                    font-size: 1.4em;
                    color: #bbb;
                    background: transparent;
                    border: none;
                    font-style: italic;
                    margin-top: 10px;
                }}
                .yell {{
                    font-weight: 800;
                    font-size: 1.3em;
                    color: #FFE6E6;
                    background: rgba(80, 0, 0, 0.6);
                    border-bottom: 4px solid #FF4444;
                    text-shadow: 2px 2px 0px #000;
                }}
                .speech {{}}

                h1 {{ color: #E6E6FA; font-weight: 300; margin: 40px 0 10px 0; text-align: center; }}
                .banner {{ background: #333; color: #aaa; padding: 5px 15px; border-radius: 20px; font-size: 0.8em; margin-bottom: 30px; text-align: center;}}
                .footer {{ color: #666; font-size: 0.8em; margin: 100px 0; text-align: center; max-width: 600px; padding: 20px; }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            <div class="banner">RENDER MODE: {mode}</div>
            
            <div class="webtoon-canvas">
        """
        
        sorted_keys = sorted(panel_map.keys())
        for i, seq in enumerate(sorted_keys):
            src, dialogue = panel_map[seq]
            
            # Determine Typography
            style_class = "speech"
            display_text = dialogue
            
            if "[SYSTEM]" in dialogue:
                style_class = "system"
                display_text = dialogue.replace("[SYSTEM]", "").strip()
            elif "(" in dialogue and ")" in dialogue:
                style_class = "thought"
            elif "!!" in dialogue or dialogue.isupper():
                style_class = "yell"

            # Determine Pacing (Gutter)
            # Default to medium
            gap_class = "gap-medium"
            if style_class == "yell" or "Action" in src: # Heuristic
                gap_class = "gap-small" # Fast pace
            elif style_class == "system":
                gap_class = "gap-medium"
            elif style_class == "thought":
                gap_class = "gap-large" # Contemplation time
            
            # Last panel gets extra space
            if i == len(sorted_keys) - 1:
                gap_class = "gap-large"

            # Handle Source
            if src.startswith("http"):
                img_tag = f'<img src="{src}" />'
            else:
                img_tag = f'<img src="images/{src}" />'
                
            html += f"""
                <div class="panel-container {gap_class}">
                    <div style="width:100%">
                        {img_tag}
                        <div class="dialogue-box {style_class}">{display_text}</div>
                    </div>
                </div>
            """
            
        html += """
            </div>
            <div class="footer">
                <p><strong>End of Episode</strong></p>
                <p>Generated by Elysia Core Creativity Engine.</p>
                <p>Scroll Dynamics Enabled: Gutter spacing adjusts to narrative time.</p>
            </div>
        </body></html>
        """
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        # UX Fix: Update 'latest' pointer so user sees changes immediately
        # Use a meta-redirect instead of copying to prevent caching stale content
        redirect_html = f"""
        <html>
        <head>
            <meta http-equiv="refresh" content="0; url={filename}" />
            <title>Redirecting to Latest Episode...</title>
        </head>
        <body>
            <p>Redirecting to latest episode: <a href="{filename}">{filename}</a>...</p>
        </body>
        </html>
        """
        with open(latest_path, "w", encoding="utf-8") as f:
            f.write(redirect_html)
            
        logger.info(f"📚 Webtoon Published at: {html_path} (and latest_episode.html -> {filename})")

if __name__ == "__main__":
    weaver = WebtoonWeaver()
    weaver.create_pilot_episode("Aether")
