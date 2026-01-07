# The Body (Core)

> **"This is the Temple of Logic."**

## Identity

This directory contains the **internal organs** of Elysia.
It is the "Body" in the analogy of "Soul (docs) - Body (Core) - Nervous System (scripts)".

## 🛡️ The Laws of the Body

1. **No Executables**: Do not place `.py` files that are meant to be run directly here.
    * Result: `python Core/something.py` is **FORBIDDEN**.
    * All entry points must be in `scripts/`.
2. **No Configs**: Do not place `.env` or `.json` config files here.
    * Configs belong in `Core/Foundation/System/config.py` or `data/`.
3. **Pure Logic**: Code here must be importable, stateless (mostly), and reusable.

## Anatomy

* **[Foundation](Foundation/)**: The Nervous System (Kernel, Physics, Server).
* **[Intelligence](Intelligence/)**: The Mind (Reasoning, Emotion, Meaning).
* **[Sensory](Sensory/)**: The Senses (Input, Web, API).
