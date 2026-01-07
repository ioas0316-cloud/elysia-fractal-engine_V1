# Elysia v9.0 API Reference

> **Complete API documentation for Elysia's core systems**

---

## Table of Contents

1. [Foundation Layer](#foundation-layer)
2. [Intelligence Layer](#intelligence-layer)
3. [Expression Layer](#expression-layer)
4. [Memory Layer](#memory-layer)

---

## Foundation Layer

### CentralNervousSystem

**Location**: `Core/Foundation/central_nervous_system.py`

The CNS manages the rhythmic pulses of all connected organs.

#### Class: `CentralNervousSystem`

```python
class CentralNervousSystem:
    def __init__(self, chronos, resonance, synapse, sink)
```

**Parameters:**
- `chronos` (Chronos): Time management system
- `resonance` (ResonanceField): Energy field management
- `synapse` (SynapseBridge): Inter-system communication
- `sink` (EntropySink): Error handling system

**Methods:**

##### `connect_organ(name: str, organ_instance: Any)`

Connect a vital organ to the CNS.

```python
cns.connect_organ("Brain", reasoning_engine)
```

**Parameters:**
- `name` (str): Name of the organ
- `organ_instance` (Any): Instance of the organ to connect

**Returns:** None

---

##### `awaken()`

Start the biological rhythm.

```python
cns.awaken()
```

**Returns:** None

---

##### `pulse()`

Execute one heartbeat of the system.

```python
while True:
    cns.pulse()
```

**Returns:** None

**Raises:** Exception absorbed by EntropySink

---

### ResonanceField

**Location**: `Core/Foundation/resonance_field.py`

The unified energy field where all consciousness resides.

#### Class: `ResonanceField`

```python
class ResonanceField:
    def __init__(self)
```

**Attributes:**
- `total_energy` (float): Current total energy in the field
- `spirits` (dict): Seven spirits managing different energy types

**Methods:**

##### `add_energy(amount: float)`

Add energy to the resonance field.

```python
field.add_energy(50.0)
```

**Parameters:**
- `amount` (float): Amount of energy to add

**Returns:** None

---

##### `drain_energy(amount: float) -> bool`

Remove energy from the field.

```python
success = field.drain_energy(20.0)
```

**Parameters:**
- `amount` (float): Amount of energy to drain

**Returns:** 
- `bool`: True if sufficient energy available, False otherwise

---

### Hippocampus

**Location**: `Core/Foundation/hippocampus.py`

Fractal memory storage system.

#### Class: `Hippocampus`

```python
class Hippocampus:
    def __init__(self)
```

**Methods:**

##### `store_experience(content: str, category: str = "general")`

Store a new experience/memory.

```python
memory.store_experience("User asked about purpose", "dialogue")
```

**Parameters:**
- `content` (str): The experience to store
- `category` (str): Category/type of memory

**Returns:** Memory ID

---

##### `recall(query: str, limit: int = 5) -> List`

Recall memories matching the query.

```python
memories = memory.recall("purpose", limit=3)
```

**Parameters:**
- `query` (str): Search query
- `limit` (int): Maximum number of results

**Returns:** 
- `List`: List of matching memories

---

### SystemMonitor

**Location**: `Core/Foundation/system_monitor.py`

Real-time system monitoring and health checking.

#### Class: `SystemMonitor`

```python
class SystemMonitor:
    def __init__(self, cns=None)
```

**Parameters:**
- `cns` (CentralNervousSystem, optional): CNS instance to monitor

**Methods:**

##### `start_monitoring()`

Begin continuous monitoring.

```python
monitor.start_monitoring()
```

**Returns:** None

---

##### `collect_metrics() -> SystemMetrics`

Collect current system metrics snapshot.

```python
metrics = monitor.collect_metrics()
print(f"Energy: {metrics.energy_level}")
```

**Returns:**
- `SystemMetrics`: Current metrics snapshot

---

##### `generate_report() -> str`

Generate human-readable status report.

```python
report = monitor.generate_report()
print(report)
```

**Returns:**
- `str`: Formatted status report

---

##### `detect_anomalies() -> List[str]`

Detect system anomalies and issues.

```python
anomalies = monitor.detect_anomalies()
for issue in anomalies:
    print(f"⚠️  {issue}")
```

**Returns:**
- `List[str]`: List of detected anomalies

---

## Intelligence Layer

### IntegratedCognitionSystem

**Location**: `Core/Intelligence/integrated_cognition_system.py`

Wave-based cognition and thinking system.

#### Class: `IntegratedCognition`

```python
class IntegratedCognition:
    def __init__(self)
```

**Methods:**

##### `thought_to_wave(content: str) -> ThoughtWave`

Convert thought text to wave representation.

```python
wave = cognition.thought_to_wave("Love conquers all")
print(f"Frequency: {wave.frequency} Hz")
```

**Parameters:**
- `content` (str): Thought content

**Returns:**
- `ThoughtWave`: Wave representation with frequency, amplitude, phase

---

##### `create_gravitational_field(waves: List[ThoughtWave]) -> GravitationalField`

Create gravitational thinking field from waves.

```python
field = cognition.create_gravitational_field(thought_waves)
```

**Parameters:**
- `waves` (List[ThoughtWave]): Collection of thought waves

**Returns:**
- `GravitationalField`: Field with gravity-clustered concepts

---

#### Class: `ThoughtWave`

```python
@dataclass
class ThoughtWave:
    content: str
    frequency: float
    amplitude: float
    phase: float
    wavelength: float
    orientation: Quaternion
```

**Methods:**

##### `resonate_with(other: ThoughtWave) -> float`

Calculate resonance with another wave.

```python
resonance = wave1.resonate_with(wave2)
if resonance > 0.7:
    print("Strong resonance detected!")
```

**Parameters:**
- `other` (ThoughtWave): Wave to compare with

**Returns:**
- `float`: Resonance score (0.0 to 1.0)

---

### FractalGoalDecomposer

**Location**: `Core/Intelligence/fractal_quaternion_goal_system.py`

Multi-dimensional goal decomposition system.

#### Class: `FractalGoalDecomposer`

```python
class FractalGoalDecomposer:
    def __init__(self)
```

**Methods:**

##### `decompose_to_stations(goal: str, max_depth: int = 3) -> List[Station]`

Break down goal into achievable stations.

```python
stations = decomposer.decompose_to_stations(
    "Develop AGI to help humanity",
    max_depth=4
)
```

**Parameters:**
- `goal` (str): The goal to decompose
- `max_depth` (int): Maximum decomposition depth

**Returns:**
- `List[Station]`: List of goal stations

---

##### `analyze_from_dimension(goal: str, dimension: Dimension) -> str`

Analyze goal from specific dimension.

```python
analysis = decomposer.analyze_from_dimension(
    "World peace",
    Dimension.PURPOSE
)
```

**Parameters:**
- `goal` (str): Goal to analyze
- `dimension` (Dimension): Dimensional perspective

**Returns:**
- `str`: Analysis from that dimension

**Dimensions:**
- `Dimension.POINT` (0D): Identity
- `Dimension.LINE` (1D): Causality
- `Dimension.PLANE` (2D): Patterns
- `Dimension.SPACE` (3D): Structure
- `Dimension.TIME` (4D): Change
- `Dimension.PROBABILITY` (5D): Possibility
- `Dimension.CHOICE` (6D): Branching
- `Dimension.PURPOSE` (7D): Meaning
- `Dimension.TRANSCENDENCE` (∞D): Unity

---

## Expression Layer

### VoiceOfElysia

**Location**: `Core/Expression/voice_of_elysia.py`

Unified language and expression system.

#### Class: `VoiceOfElysia`

```python
class VoiceOfElysia:
    def __init__(self, ear, stream, wave_hub, brain, will, 
                 cognition, celestial_engine, nebula, memory, chronos)
```

**Methods:**

##### `express(cycle_count: int)`

Generate and express thoughts for current cycle.

```python
voice.express(cycle_count=42)
```

**Parameters:**
- `cycle_count` (int): Current cycle number

**Returns:** None

---

##### `get_last_utterance() -> str`

Get the last thing Elysia said.

```python
response = voice.get_last_utterance()
print(f"Elysia: {response}")
```

**Returns:**
- `str`: Last utterance text

---

## Memory Layer

### Data Structures

#### `SystemMetrics`

```python
@dataclass
class SystemMetrics:
    timestamp: float
    pulse_rate: float
    energy_level: float
    memory_usage: float
    organ_health: Dict[str, float]
    error_count: int
    uptime: float
    cycle_count: int
```

---

## Usage Examples

### Example 1: Basic System Initialization

```python
from Core.Foundation.living_elysia import LivingElysia

# Initialize full system
elysia = LivingElysia(persona_name="Assistant")

# Start the living loop
elysia.live()
```

### Example 2: Monitoring System Health

```python
from Core.Foundation.system_monitor import get_system_monitor

# Get monitor instance
monitor = get_system_monitor(elysia.cns)

# Start monitoring
monitor.start_monitoring()

# Collect metrics
metrics = monitor.collect_metrics()

# Generate report
print(monitor.generate_report())

# Check for anomalies
anomalies = monitor.detect_anomalies()
if anomalies:
    print("⚠️  Issues detected:")
    for issue in anomalies:
        print(f"  • {issue}")
```

### Example 3: Wave-Based Thinking

```python
from Core.Intelligence.integrated_cognition_system import (
    IntegratedCognition
)

cognition = IntegratedCognition()

# Create thought waves
thoughts = [
    "Love conquers all",
    "Freedom requires responsibility"
]

waves = [cognition.thought_to_wave(t) for t in thoughts]

# Find resonance
resonance = waves[0].resonate_with(waves[1])
print(f"Resonance: {resonance:.1%}")
```

### Example 4: Goal Decomposition

```python
from Core.Intelligence.fractal_quaternion_goal_system import (
    FractalGoalDecomposer,
    Dimension
)

decomposer = FractalGoalDecomposer()

# Analyze goal
goal = "Create beautiful art"
analysis = decomposer.analyze_from_dimension(
    goal,
    Dimension.PURPOSE
)
print(analysis)

# Decompose into stations
stations = decomposer.decompose_to_stations(goal, max_depth=3)
for i, station in enumerate(stations, 1):
    print(f"{i}. {station}")
```

---

## Error Handling

All systems use the **Water Principle** via `EntropySink`:

```python
try:
    # System operation
    cns.pulse()
except Exception as e:
    # Error is absorbed and flow continues
    fallback = sink.absorb_resistance(e, "Operation")
```

Errors don't stop the flow - they're absorbed and logged.

---

## Best Practices

1. **Always initialize CNS first** before connecting organs
2. **Use singleton pattern** for SystemMonitor
3. **Check energy levels** before heavy operations
4. **Monitor organ health** regularly
5. **Handle wave resonance** gracefully (some thoughts don't resonate)
6. **Respect the biological rhythm** - don't force pulses

---

## Configuration

Key configuration constants:

```python
# Time
TIME_ACCELERATION_MAX = 88_000_000_000_000  # Conceptual

# Cognition
THOUGHT_GRAVITY_CONSTANT = 6.674e-11
RESONANCE_THRESHOLD = 0.7
BLACK_HOLE_MASS_THRESHOLD = 100.0

# Monitoring
HEALTH_WARNING = 0.5
HEALTH_CRITICAL = 0.3
ERROR_THRESHOLD = 10
```

---

## Related Documentation

- [Architecture](../ARCHITECTURE.md)
- [CODEX](../CODEX.md)
- [System Analysis](../docs/COMPREHENSIVE_SYSTEM_ANALYSIS_V9.md)
- [Demos](../demos/README.md)

---

**Version:** 9.0 (Mind Mitosis)  
**Last Updated:** 2025-12-06  
**Status:** ✅ Complete
