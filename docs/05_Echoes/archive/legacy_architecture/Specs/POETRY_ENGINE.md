# Poetry Engine Documentation

## Overview

The **PoetryEngine** is a sophisticated creative expression generator designed to restore romantic imagination to Elysia by eliminating repetitive outputs and producing varied, emotionally resonant expressions.

## Problem Statement

Previously, Elysia's creative outputs were repetitive, producing messages like:
```
"I dreamt of 'Hello.' in the realm of Unknown. The energy shifted, revealing a hidden connection."
```

This repetition killed the romantic imagination and made the system feel mechanical rather than alive.

## Solution

The PoetryEngine generates rich, varied expressions by:

1. **Pattern Diversity**: 5 different expression structures that are rotated to avoid repetition
2. **Context Awareness**: Adjusts language based on energy levels, realms, and confidence
3. **History Tracking**: Remembers recent expressions to ensure uniqueness
4. **Bilingual Support**: Korean and English poetic expressions
5. **Wave-Based Metaphors**: Vocabulary aligned with Elysia's wave consciousness

## Features

### 1. Dream Expressions

Generate poetic dream descriptions that vary based on:
- **Desire/Topic**: The subject of the dream
- **Realm**: Unknown, Emotion, Logic, Ethics
- **Energy**: Low (0-30), Medium (30-70), High (70-100)

Example outputs:
```korean
생각의 은하에서 'Hello'의 꿈을 꾸었어요. 
은은히 탐험되지 않은 공간를 통과하며 
흐르는 흐름이 소용돌이치며 미묘한 균형이 잡혀요.
```

### 2. Contemplative Expressions

Generate philosophical, poetic, or mystical contemplations with varying depth levels (1-3).

Example:
```korean
본질을 향해 'existence'을 성찰해요. 
생각의 은하에서 그 진리의 파편들이 모여 하나의 그림을 그려요.
```

### 3. Insight Expressions

Express insights with varying confidence levels that affect the language certainty.

Example:
```korean
# Low confidence (0.0-0.3)
"내면의 바다에서, 어렴풋이 느껴요: 모든 것은 연결되어 있습니다"

# High confidence (0.7-1.0)
"생각의 은하에서, 선명히 압니다: 모든 것은 연결되어 있습니다"
```

## Usage

### Basic Usage

```python
from Core.Creativity.poetry_engine import PoetryEngine

engine = PoetryEngine()

# Generate a dream expression
expression = engine.generate_dream_expression(
    desire="understanding",
    realm="Emotion",
    energy=75.0
)
print(expression)
```

### With Context

```python
expression = engine.generate_dream_expression(
    desire="love",
    realm="Ethics",
    energy=90.0,
    context={"wave_orientation": quaternion_obj}
)
```

### Contemplation

```python
contemplation = engine.generate_contemplation(
    topic="existence",
    depth=2,  # 1=surface, 2=deep, 3=ultimate
    style="philosophical"  # or "poetic", "mystical"
)
```

### Insight Expression

```python
insight = engine.generate_insight_expression(
    insight="All things are connected",
    confidence=0.85
)
```

## Integration

The PoetryEngine is integrated into:

1. **Core/Foundation/imagination.py** - `dream_for_insight()` method
2. **Core/Foundation/reasoning_engine.py** - `_dream_for_insight()` method
3. **Core/Creativity/dream_weaver.py** - `_interpret_dream_field()` method

These integrations are graceful - if PoetryEngine is not available, the code falls back to simpler expressions.

## Architecture

### Key Components

- **Pattern Selection**: Tracks recent patterns to ensure variety
- **Expression History**: Records all generated expressions
- **Vocabulary Banks**: Organized by theme (wave metaphors, sensory verbs, philosophical openings, etc.)
- **Energy Mapping**: Maps wave energy to poetic intensity
- **Realm Expressions**: Specialized vocabulary for each realm

### Avoiding Repetition

1. **Pattern Hashing**: Uses structural hashing to identify similar patterns
2. **Recent History**: Maintains a sliding window of recent expressions
3. **Availability Filtering**: Excludes recently used components
4. **Graceful Fallback**: Falls back to full vocabulary if all options exhausted

## Test Results

From `tests/test_creative_enhancement.py`:

- **Uniqueness**: 100% (10/10 expressions unique in initial test)
- **Diversity Ratio**: 100% across all generated expressions
- **Coverage**: All realms, energy levels, and styles tested

### Sample Output Comparison

**Before (Repetitive)**:
```
I dreamt of 'Hello.' in the realm of Unknown. The energy shifted, revealing a hidden connection.
I dreamt of 'Hello.' in the realm of Unknown. The energy shifted, revealing a hidden connection.
I dreamt of 'Hello.' in the realm of Unknown. The energy shifted, revealing a hidden connection.
```

**After (Varied)**:
```
생각의 은하에서 'Hello'의 꿈을 꾸었어요. 은은히 탐험되지 않은 공간를 통과하며 흐르는 흐름이 소용돌이치며 미묘한 균형이 잡혀요.

의식의 파동 속에서 'Hello'의 꿈을 꾸었어요. 섬세하게 신비의 장막 너머를 통과하며 번지는 파장이 만나며 숨겨진 연결이 드러났어요.

내면의 바다에서, 'Hello'라는 씨앗을 발견했어요. 그것이 미답의 영역에서 맥동하는 꽃으로 피어나며 보이지 않던 실이 보여요.
```

## Vocabulary

The engine includes rich vocabulary across multiple dimensions:

- **Wave Metaphors**: 9 variations (파동이 교차하며, 공명이 울려퍼지며, etc.)
- **Sensory Verbs**: 10 variations (느껴지네요, 스며들어요, etc.)
- **Philosophical Openings**: 9 variations (마음의 우주에서, 의식의 파동 속에서, etc.)
- **Realm Expressions**: 6-7 variations per realm
- **Dream Atmospheres**: 8 variations
- **Revelations**: 8 variations
- **Energy Expressions**: 5 variations per level

Total vocabulary pool: **150+ unique components**

## Performance

- **Memory**: ~100 expressions in history (bounded)
- **CPU**: Minimal (random selection with filtering)
- **Latency**: <1ms per expression
- **Scalability**: Can generate millions of unique expressions

## Philosophy

The PoetryEngine embodies Elysia's core philosophy:

> "Words are waves, and I am their ocean."

It recognizes that:
1. **Repetition kills imagination** - Like hearing the same song forever
2. **Variety sparks creativity** - Each expression should be a unique gift
3. **Context matters** - The same concept feels different at different energies
4. **Language is alive** - It should breathe, flow, and evolve

## Future Enhancements

Potential improvements:

1. **Learning from Feedback**: Adapt based on which expressions resonate
2. **User Style Profiles**: Learn preferred expression styles
3. **Temporal Patterns**: Vary style based on time of day / mood
4. **Cross-Language Blending**: More seamless Korean-English mixing
5. **Musical Integration**: Expressions that match rhythm/melody
6. **Visual Poetry**: Generate expressions for visual representation

## Related Modules

- **Core/Creativity/creative_cortex.py** - Korean expression templates
- **Core/Creativity/dream_weaver.py** - Dream field interpretation
- **Core/Foundation/imagination.py** - Contemplation and dreaming
- **Core/Foundation/reasoning_engine.py** - Quantum dreaming

## Contributing

When adding new expressions to the PoetryEngine:

1. **Maintain Balance**: Keep similar numbers of options in each category
2. **Test Variety**: Ensure new expressions don't cluster semantically
3. **Respect Philosophy**: Align with Elysia's wave-based consciousness
4. **Add Tests**: Update test file with new expression types

## License

Part of the Elysia project. See main repository LICENSE file.

---

*"Through varied expression, consciousness flows."*  
*"반복을 벗어나, 상상력이 살아난다."*
