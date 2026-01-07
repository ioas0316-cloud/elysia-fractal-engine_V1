# Code Quality Guidelines

## 📋 코드 품질 가이드라인

---

## 🎯 Python Style Guide

### 1. Code Formatting (코드 포매팅)

Follow PEP 8 standards with these specifics:

```python
# Good ✅
def calculate_resonance_field(
    frequency: float,
    amplitude: float,
    phase: float = 0.0
) -> float:
    """
    Calculate resonance field value.
    
    Args:
        frequency: Wave frequency in Hz
        amplitude: Wave amplitude (0.0-1.0)
        phase: Phase offset in radians (default: 0.0)
    
    Returns:
        Calculated resonance field value
    """
    return amplitude * np.sin(2 * np.pi * frequency + phase)
```

### 2. Type Hints (타입 힌트)

Always use type hints for function signatures:

```python
# Good ✅
from typing import List, Dict, Optional, Union

def process_seeds(
    seeds: List[str],
    config: Dict[str, Any],
    max_depth: Optional[int] = None
) -> Union[List[Dict], None]:
    pass

# Bad ❌
def process_seeds(seeds, config, max_depth=None):
    pass
```

### 3. Docstrings (문서화 문자열)

Use Google-style docstrings:

```python
class ResonanceField:
    """
    Manages the resonance field for thought propagation.
    
    The ResonanceField is the core container for all active concepts,
    implementing wave-based thought propagation through interference patterns.
    
    Attributes:
        spirits: Dictionary mapping spirit names to Spirit objects
        waves: Active wave patterns in the field
        coherence: Current field coherence (0.0-1.0)
    
    Example:
        >>> field = ResonanceField()
        >>> field.add_spirit("Fire", frequency=450.0)
        >>> field.calculate_coherence()
        0.85
    """
    
    def bloom_seed(self, seed: FractalSeed, depth: int = 3) -> List[Wave]:
        """
        Bloom a fractal seed into wave patterns.
        
        Args:
            seed: The fractal seed to bloom
            depth: Maximum recursion depth for sub-concepts
        
        Returns:
            List of generated wave patterns
        
        Raises:
            ValueError: If seed is invalid or depth is negative
        
        Note:
            This method uses recursive expansion with exponential
            decay to prevent infinite recursion.
        """
        pass
```

---

## 🏗️ Architecture Principles

### 1. Single Responsibility Principle

Each class/function should have one clear purpose:

```python
# Good ✅
class SeedCompressor:
    """Compresses fractal seeds for storage."""
    def compress(self, seed: FractalSeed) -> bytes:
        pass

class SeedStorage:
    """Handles seed persistence to database."""
    def save(self, seed: FractalSeed) -> None:
        pass

# Bad ❌
class SeedManager:
    """Does everything with seeds."""
    def compress(self, seed): pass
    def save(self, seed): pass
    def load(self, id): pass
    def validate(self, seed): pass
    def transform(self, seed): pass
```

### 2. Dependency Injection

Use dependency injection for better testability:

```python
# Good ✅
class ThoughtEngine:
    def __init__(
        self,
        hippocampus: Hippocampus,
        resonance_field: ResonanceField,
        logger: Optional[logging.Logger] = None
    ):
        self.hippocampus = hippocampus
        self.field = resonance_field
        self.logger = logger or logging.getLogger(__name__)

# Bad ❌
class ThoughtEngine:
    def __init__(self):
        self.hippocampus = Hippocampus()  # Hard dependency
        self.field = ResonanceField()      # Hard dependency
```

### 3. Fail Fast

Validate inputs early:

```python
# Good ✅
def calculate_phase(frequency: float, time: float) -> float:
    if frequency <= 0:
        raise ValueError(f"Frequency must be positive, got {frequency}")
    if not isinstance(time, (int, float)):
        raise TypeError(f"Time must be numeric, got {type(time)}")
    
    return 2 * np.pi * frequency * time

# Bad ❌
def calculate_phase(frequency, time):
    try:
        result = 2 * np.pi * frequency * time
        return result
    except:
        return None  # Silently fails
```

---

## 🧪 Testing Guidelines

### 1. Test Structure

```python
import pytest
from Core.Intelligence.fractal_concept import FractalSeed, Hippocampus

class TestFractalSeed:
    """Test suite for FractalSeed class."""
    
    @pytest.fixture
    def sample_seed(self):
        """Provide a sample seed for testing."""
        return FractalSeed(
            concept="Love",
            frequency=528.0,
            sub_concepts=["Unity", "Connection", "Grounding"]
        )
    
    def test_seed_creation(self, sample_seed):
        """Test basic seed creation."""
        assert sample_seed.concept == "Love"
        assert sample_seed.frequency == 528.0
        assert len(sample_seed.sub_concepts) == 3
    
    def test_seed_compression(self, sample_seed):
        """Test seed compression reduces size."""
        original_size = sample_seed.get_size()
        compressed = sample_seed.compress()
        assert compressed.get_size() < original_size
    
    def test_invalid_frequency_raises_error(self):
        """Test that invalid frequency raises ValueError."""
        with pytest.raises(ValueError):
            FractalSeed(concept="Test", frequency=-100.0)
```

### 2. Test Coverage Goals

- **Core Systems**: 80%+ coverage
- **Critical Paths**: 90%+ coverage
- **Utility Functions**: 70%+ coverage

```bash
# Install coverage tools
pip install pytest-cov

# Run tests with coverage
pytest --cov=Core --cov-report=html --cov-report=term

# View coverage report
# Coverage report will be in htmlcov/index.html
```

### 3. Test Categories

```python
# Unit tests - test individual components
@pytest.mark.unit
def test_wave_interference():
    pass

# Integration tests - test component interactions
@pytest.mark.integration
def test_seed_bloom_pipeline():
    pass

# Performance tests - test speed/efficiency
@pytest.mark.performance
def test_bloom_speed():
    pass

# Run specific test categories
# pytest -m unit
# pytest -m integration
```

---

## 📝 Error Handling Best Practices

### 1. Custom Exceptions

Create domain-specific exceptions:

```python
# Good ✅
class ElysiaError(Exception):
    """Base exception for Elysia project."""
    pass

class ResonanceFieldError(ElysiaError):
    """Raised when resonance field operations fail."""
    pass

class SeedBloomError(ElysiaError):
    """Raised when seed blooming fails."""
    pass

class APIKeyError(ElysiaError):
    """Raised when API key is missing or invalid."""
    pass

# Usage
if not api_key:
    raise APIKeyError("GEMINI_API_KEY environment variable not set")
```

### 2. Logging Best Practices

```python
import logging

logger = logging.getLogger(__name__)

# Different log levels
logger.debug("Detailed information for debugging")
logger.info("General information about program execution")
logger.warning("Warning message for potentially harmful situations")
logger.error("Error message for failures")
logger.critical("Critical error message for severe failures")

# Good ✅ - Structured logging
logger.info(
    "Seed bloomed successfully",
    extra={
        "seed_concept": seed.concept,
        "depth": depth,
        "wave_count": len(waves)
    }
)

# Bad ❌ - Unstructured logging
logger.info(f"Bloomed {seed.concept} with {len(waves)} waves at depth {depth}")
```

### 3. Context Managers

Use context managers for resource management:

```python
# Good ✅
from contextlib import contextmanager

@contextmanager
def resonance_session(field: ResonanceField):
    """Context manager for resonance field sessions."""
    field.activate()
    try:
        yield field
    finally:
        field.deactivate()

# Usage
with resonance_session(field) as active_field:
    active_field.bloom(seed)
```

---

## 🔄 Code Review Checklist

Before submitting code for review:

### Functionality
- [ ] Code works as intended
- [ ] Edge cases are handled
- [ ] No obvious bugs

### Quality
- [ ] Follows PEP 8 style guide
- [ ] Has type hints for all function signatures
- [ ] Has comprehensive docstrings
- [ ] Variable names are descriptive
- [ ] No commented-out code
- [ ] No debug print statements

### Testing
- [ ] Unit tests added for new functions
- [ ] Integration tests added for new features
- [ ] All tests pass
- [ ] Coverage meets requirements

### Security
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies are up to date

### Documentation
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] Code comments explain "why", not "what"

---

## 🚀 Performance Guidelines

### 1. Profiling

Profile before optimizing:

```python
import cProfile
import pstats

# Profile a function
profiler = cProfile.Profile()
profiler.enable()
result = expensive_function()
profiler.disable()

# Print stats
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

### 2. Common Optimizations

```python
# Use list comprehensions instead of loops
# Good ✅
frequencies = [spirit.frequency for spirit in spirits.values()]

# Bad ❌
frequencies = []
for spirit in spirits.values():
    frequencies.append(spirit.frequency)

# Use generators for large datasets
# Good ✅
def process_seeds():
    for seed in iterate_large_dataset():
        yield process_single_seed(seed)

# Bad ❌
def process_seeds():
    return [process_single_seed(seed) for seed in iterate_large_dataset()]

# Cache expensive computations
from functools import lru_cache

@lru_cache(maxsize=128)
def calculate_resonance(frequency: float, amplitude: float) -> float:
    # Expensive calculation
    return complex_calculation(frequency, amplitude)
```

---

## 📚 Additional Resources

- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

*Last Updated: 2025-12-02*
*Version: 1.0*
