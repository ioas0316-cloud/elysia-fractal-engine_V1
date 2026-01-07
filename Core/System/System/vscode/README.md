# Elysia VSCode Client (Sample)

This is a minimal example VSCode extension that connects to Elysia's HTTP API.

Features:
- Command: `Elysia: Decide Tool` → sends selected text or input to `/tool/decide`.
- Command: `Elysia: Execute Decision` → executes a previously prepared decision via `/tool/execute`.
- If `confirm_required` is present, it prompts the user.

Configuration:
- `elysia.baseUrl` (default `http://127.0.0.1:5000`)

Usage:
1. From this directory, run `npm install`.
2. `npm run compile` (or `npm run watch`).
3. Press F5 in VSCode to launch the extension host.
4. Packaging (optional): install `vsce` (`npm i -g @vscode/vsce`) then run `vsce package`.

Note: This is a scaffold for demonstration and can be adapted as needed.
