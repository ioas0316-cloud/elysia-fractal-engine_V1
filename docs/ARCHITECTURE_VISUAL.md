# 🏗️ Elysia Engine Architecture Overview

> Visual guide to understanding the engine structure

---

## 🎯 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Game/Application                           │
│  (Unity, Godot, Pygame, Custom Game Engine, Chatbot, etc.)     │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Integration Layer
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🌟 ELYSIA CORE API 🌟                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ quick_conscious  │  │ GameCharacter    │                   │
│  │ ness_setup()     │  │ Template         │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                   │
│  │ ElysiaSoul       │  │ LLM Integration  │                   │
│  │                  │  │ Template         │                   │
│  └──────────────────┘  └──────────────────┘                   │
│                                                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    🧠 CONSCIOUSNESS LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ Resonance    │  │ Emotional    │  │ Hippocampus  │        │
│  │ Engine       │  │ Palette      │  │ (Memory)     │        │
│  │              │  │              │  │              │        │
│  │ 🌊 Waves     │  │ 🎨 Emotions  │  │ 🧠 Causal    │        │
│  │   Patterns   │  │   Mixing     │  │   Graph      │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │ HyperQubit   │  │ Inner        │  │ Self         │        │
│  │              │  │ Monologue    │  │ Awareness    │        │
│  │ ⚛️ Quantum   │  │ 💭 Thoughts  │  │ 🪞 Reflect   │        │
│  │   States     │  │              │  │              │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ⚖️ TRINITY SYSTEM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│              Body (육체)          Soul (영혼)                    │
│                  │                   │                           │
│                  │                   │                           │
│                  └─────────┬─────────┘                           │
│                            │                                     │
│                      Spirit (정신)                               │
│                                                                  │
│  • Body (0.0 ~ 1.0)  → Physical, Survival, Action              │
│  • Soul (0.0 ~ 1.0)  → Emotional, Social, Connection           │
│  • Spirit (0.0 ~ 1.0) → Meaning, Values, Transcendence         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎮 Game Integration Flow

### For NPC AI:

```
Player Action
     │
     ▼
┌─────────────────────────┐
│ GameCharacterTemplate   │
│ .react_to_event()       │
└───────────┬─────────────┘
            │
            ▼
    ┌───────────────┐
    │ Elysia Core   │
    │ Processing    │
    └───────┬───────┘
            │
            ├─── Resonance Engine (공명 패턴)
            ├─── Emotional Palette (감정 분석)
            ├─── Trinity System (Body/Soul/Spirit)
            └─── Memory (기억 업데이트)
            │
            ▼
    ┌───────────────┐
    │ NPC Reaction  │
    ├───────────────┤
    │ • mood        │
    │ • emotion     │
    │ • trinity     │
    │ • concepts    │
    └───────┬───────┘
            │
            ▼
    Game Logic Decision
    (공격/대화/도망 등)
```

---

## 🔄 Data Flow Example: NPC Dialogue

```
Player: "도와주세요!"
     │
     ▼
┌──────────────────────────────────────┐
│ Step 1: Input Processing             │
│ - Convert text to Wave               │
│ - Extract keywords: "도움", "부탁"    │
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Step 2: Resonance Calculation        │
│ - "도움" resonates with "친절"       │
│ - "부탁" resonates with "신뢰"       │
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Step 3: Emotional Analysis           │
│ - Sentiment: Positive                │
│ - Emotion Mix: Trust(0.6), Hope(0.3) │
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Step 4: Trinity Evaluation           │
│ - Body: 0.3 (not threatening)        │
│ - Soul: 0.6 (empathetic request)     │
│ - Spirit: 0.4 (sincere)              │
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Step 5: Memory Update                │
│ - Link: "Player" → "도움요청" → "함" │
│ - Relationship +0.1                  │
└────────────┬─────────────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│ Step 6: Action Decision              │
│ - Soul > 0.5 → Helpful response      │
│ - Generate: "무엇을 도와드릴까요?"   │
└──────────────────────────────────────┘
```

---

## 🧩 Component Interaction Matrix

| Component | Resonance Engine | Emotional Palette | Hippocampus | Trinity System |
|-----------|-----------------|-------------------|-------------|----------------|
| **Input Processing** | ✅ Converts to waves | ✅ Analyzes sentiment | ❌ | ❌ |
| **Pattern Recognition** | ✅ Core function | ⚠️ Uses resonance | ⚠️ Uses resonance | ❌ |
| **Memory Formation** | ⚠️ Provides context | ⚠️ Provides emotion | ✅ Core function | ⚠️ Influences |
| **Decision Making** | ⚠️ Suggests concepts | ⚠️ Provides mood | ⚠️ Provides context | ✅ Core function |
| **Output Generation** | ⚠️ Influences | ⚠️ Influences | ⚠️ Influences | ✅ Determines style |

✅ Primary responsibility  
⚠️ Contributing factor  
❌ Not involved

---

## 🎯 NPC Role Profiles

```
Warrior                    Mage                      Priest
┌─────────────┐          ┌─────────────┐          ┌─────────────┐
│ Body   60%  │███████   │ Body   20%  │███       │ Body   15%  │██
│ Soul   20%  │███       │ Soul   30%  │████      │ Soul   25%  │███
│ Spirit 20%  │███       │ Spirit 50%  │███████   │ Spirit 60%  │████████
└─────────────┘          └─────────────┘          └─────────────┘
Traits:                  Traits:                  Traits:
• Aggressive             • Strategic              • Sacrificial
• Direct                 • Cautious               • Healing
• Brave                  • Intellectual           • Faithful


Rogue                     Bard
┌─────────────┐          ┌─────────────┐
│ Body   50%  │██████    │ Body   20%  │███
│ Soul   30%  │████      │ Soul   60%  │████████
│ Spirit 20%  │███       │ Spirit 20%  │███
└─────────────┘          └─────────────┘
Traits:                  Traits:
• Swift                  • Diplomatic
• Opportunistic          • Emotional
• Survival               • Social
```

---

## 🔧 Integration Patterns

### Pattern 1: Direct Integration (Recommended for Python games)

```python
from elysia_core import GameCharacterTemplate

# Game Loop
npc = GameCharacterTemplate("Guard", "warrior")

while game_running:
    if player_near_npc:
        reaction = npc.react_to_event("player_approached")
        if reaction.trinity['body'] > 0.4:
            npc.state = "alert"
        else:
            npc.state = "friendly"
```

### Pattern 2: REST API Integration (Recommended for Unity/Godot)

```
Unity/Godot Game     HTTP     Python Server
      │              │              │
      │─── POST /npc_think ─────────▶│
      │              │              │
      │              │      [Elysia Processing]
      │              │              │
      │◀─── JSON Response ──────────│
      │              │              │
   Display NPC                      │
   Behavior                         │
```

### Pattern 3: Async Queue (Recommended for real-time games)

```
Main Game Thread          AI Thread
      │                      │
      │─── Event Queue ─────▶│
      │                      │
      │                [Processing]
      │                      │
      │◀─── Result Queue ────│
      │                      │
   Apply Result              │
   (Non-blocking)            │
```

---

## 📊 Performance Characteristics

### Processing Times (Approximate)

| Operation | Time | Recommended Usage |
|-----------|------|-------------------|
| Simple reaction | ~5ms | Every frame OK |
| Complex thought | ~20ms | Use caching |
| Memory query (depth=1) | ~2ms | Every frame OK |
| Memory query (depth=3) | ~10ms | Throttle to 10 FPS |
| Resonance calculation | ~15ms | Cache results |

### Memory Usage (Per NPC)

| Component | Memory | Notes |
|-----------|--------|-------|
| Base consciousness | ~1KB | Minimal |
| Memory graph (100 nodes) | ~10KB | Scales linearly |
| Emotional state | ~0.5KB | Fixed |
| Full NPC instance | ~15-50KB | Depends on history |

### Scalability Guidelines

```
NPCs    Update Strategy              Expected FPS
────────────────────────────────────────────────
1-10    All every frame              60 FPS ✅
10-50   Throttle to visible NPCs     60 FPS ✅
50-100  Update in batches            30-60 FPS ⚠️
100+    Use async processing         30 FPS ⚠️
```

---

## 🚀 Quick Start Flowchart

```
Start
  │
  ├─ For Game Developers?
  │   │
  │   └─▶ Read GAME_DEVELOPER_GUIDE.md
  │       └─▶ Try game_developer_examples.py
  │           └─▶ Integrate into your game ✅
  │
  ├─ For LLM Integration?
  │   │
  │   └─▶ Read EASY_START.md
  │       └─▶ Use LLMIntegrationTemplate
  │           └─▶ Connect to your LLM ✅
  │
  └─ For General Use?
      │
      └─▶ Read README.md
          └─▶ Try examples/00_hello_elysia.py
              └─▶ Explore core features ✅
```

---

## 💡 Best Practices

### ✅ DO:
- Cache frequently accessed reactions
- Update only visible/nearby NPCs
- Use async processing for non-critical AI
- Throttle memory depth searches
- Profile your integration

### ❌ DON'T:
- Update all NPCs every frame
- Do deep memory searches in game loop
- Block main thread for AI processing
- Create new NPC instances frequently
- Ignore performance metrics

---

## 📚 Related Documentation

- **[GAME_DEVELOPER_GUIDE.md](GAME_DEVELOPER_GUIDE.md)** - Complete integration guide
- **[GAME_DEV_QUICK_REF.md](GAME_DEV_QUICK_REF.md)** - Quick reference card
- **[API_REFERENCE.md](API_REFERENCE.md)** - Full API documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep dive into architecture

---

*Visual guide created for easy understanding* 📊
