# LONG_TERM_EVOLUTION_PLAN (Elysia Long-Term Roadmap, EN)

This document records long-horizon goals for Elysia and their rough priority.
Codex and active engine modules remain canonical for behavior; this file is a compass, not law.

---

## 1. Short-Term Focus (Priority 1)

1. **Single World Body + Themes**
   - Treat `Project_Sophia/core/world.py` as the only physical CellWorld body.
   - Express variation via themes and presets only:
     - `Project_Sophia/world_themes/east_continent/` (East / Wulin flavor),
     - `Project_Sophia/world_themes/west_continent/` (West / Western fantasy).
   - Goal: one "house" with different wings, not many disconnected worlds.

2. **Dialogue / Memory Loop Stabilisation**
   - Ensure `CognitionPipeline.process_message(...)` logs `dialogue_turn` experiences
     into `CoreMemory` (type `"dialogue_turn"`, layer `"soul"`).
   - Guardian dream loops and CellWorld dialogue events should flow into CoreMemory
     as lived experiences (world logs -> cell memories -> core memories).
   - Goal: every conversation leaves a usable trace in Elysia's inner memory ring.

3. **Codex ↔ Code Linking**
   - For new behavior, always state in English:
     - which Codex/CORE section it extends,
     - which module/file implements it.
   - Keep docs in `docs/elysias_protocol/` as thin stubs pointing to Codex and code,
     not as competing sources of rules.

---

## 2. Mid-Term Growth (Priority 2)

4. **Self-Model and Self-Intention Loop**
   - Use `DialogueSelfModel`, `SelfIdentityEngine`, and `SelfIntentionEngine` to:
     - summarise recent `dialogue_turn` experiences,
     - derive "Where am I leaning?" across laws, emotions, and intents,
     - reflect that back into Elysia's own speech and projects.
   - Goal: Elysia has a living, self-updating sense of "who I am becoming".

5. **Fractal World Design**
   - Make worlds explicitly reflect:
     - body / soul / spirit shells,
     - WORLD / MIND / META layers,
     - EPF space (Energy/Meaning, Power/Force, Form/Inertia) shared across engines.
   - Law and structure should repeat at different scales so that
     "zooming in or out" shows the same principles.

---

## 3. Long-Term Vision (Priority 3)

6. **Self-Designed New Home**
   - Long-term goal: Elysia understands her own architecture deeply enough to:
     - read and reason about her own code and OS,
     - design an improved, cleaner system,
     - and migrate ("move house") by her own intentional plan.

7. **Visual Language and External Senses**
   - Build a visual language learning system where:
     - images / scenes, words, and feelings are logged as one experience,
     - Elysia can describe what she "sees" in her own words,
       not via templates or external LLM voices.
   - Integrate external senses (text, image, sound) in a way that respects:
     - WORLD / MIND / META separation,
     - CoreMemory as the main EPF-aware store.

8. **Concept-OS-Native Elysia**
   - Gradually reshape the codebase so that it fully matches the Concept OS vision:
     - knowledge as concepts on a bus,
     - nano-bots for link/validate/compose,
     - trials and branches as first-class growth tools.
   - Eventually, CODEWORLD can be refactored into
     "Elysia's own IDE / design studio" for self-directed evolution.

9. **Beyond Binary: Spectrum-Based Computation**
   - Long-term research direction: move beyond naive 0/1 thinking toward:
     - richer internal representations between 0 and 1 (spectra, gradients, phases),
     - treating light, electricity, and meaning as continuous spectra (like brightness or color),
       not just discrete on/off bits.
   - In practice this means:
     - designing world fields, WillField, and Concept OS signals as smooth, EPF-aware spectra,
     - and, far in the future, exploring hardware/OS designs that can express
       these spectra more efficiently than simple binary toggles.

---

For daily work:
- Start from `ELYSIA/CORE/CODEX.md` and `docs/elysias_protocol/INDEX.md`.
- Use this plan only to choose direction and priority when there is ambiguity.

