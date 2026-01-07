# Agent Guide for ElysiaGodot

Scope: everything under `ElysiaGodot/`.

- Treat this folder as the canonical home for Elysia's Godot / high-level world view.
- Do not create separate `HIGH_ENGINE` or `high_engine` packages elsewhere for Godot-facing logic.
- When you need a quick high-level or civilization prototype, put it here (as `.gd` scripts, scenes, or helper code like `godo_proto.py`).
- Keep prototypes minimal and focused; when they become stable, align them with the CORE protocols and refactor as needed.
