# Testing Infrastructure Guide

## 🧪 테스트 인프라 가이드

---

## 📋 Overview

This document provides guidelines for setting up and maintaining a comprehensive testing infrastructure for Project Elysia.

---

## 🎯 Testing Strategy

### Testing Pyramid

```
                    /\
                   /  \
                  / E2E \              - Few, slow, expensive
                 /______\
                /        \
               / Integ.   \           - Moderate number, medium speed
              /__________\
             /            \
            /    Unit      \          - Many, fast, cheap
           /________________\
```

### Test Categories

1. **Unit Tests** (70% of tests)
   - Test individual functions/methods
   - Fast execution (< 100ms per test)
   - No external dependencies
   - High coverage goal: 80%+

2. **Integration Tests** (20% of tests)
   - Test component interactions
   - Medium execution time (100ms - 1s)
   - May use test databases
   - Coverage goal: 60%+

3. **End-to-End Tests** (10% of tests)
   - Test complete workflows
   - Slower execution (1s+)
   - Test entire system
   - Coverage goal: Critical paths only

---

## 🛠️ Setup

### 1. Install pytest

```bash
# Install pytest and plugins
pip install pytest pytest-cov pytest-mock pytest-asyncio pytest-timeout

# Verify installation
pytest --version
```

### 2. Create pytest.ini

```ini
# pytest.ini
[pytest]
# Test discovery patterns
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Test paths
testpaths = tests

# Minimum Python version
minversion = 3.12

# Command line options
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=Core
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=70

# Markers for categorizing tests
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow running tests
    performance: Performance tests
    requires_api: Tests requiring API access

# Test timeout (prevents hanging tests)
timeout = 300
timeout_method = thread

# Asyncio mode
asyncio_mode = auto
```

### 3. Create conftest.py

```python
# tests/conftest.py
"""
Shared test fixtures and configuration.
"""
import pytest
import tempfile
import os
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Provide a directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_api_key(monkeypatch):
    """Mock API key for testing."""
    monkeypatch.setenv("GEMINI_API_KEY", "test_api_key_12345")
    yield "test_api_key_12345"

@pytest.fixture
def temp_db_path(tmp_path):
    """Provide a temporary database path."""
    db_path = tmp_path / "test_memory.db"
    yield db_path
    # Cleanup happens automatically with tmp_path

@pytest.fixture
def sample_seed():
    """Provide a sample FractalSeed for testing."""
    from Core.Intelligence.fractal_concept import FractalSeed
    return FractalSeed(
        concept="Love",
        frequency=528.0,
        sub_concepts=["Unity", "Connection", "Grounding"]
    )

@pytest.fixture
def resonance_field():
    """Provide a clean ResonanceField instance."""
    from Core.Foundation.resonance_field import ResonanceField
    field = ResonanceField()
    yield field
    field.clear()  # Cleanup

@pytest.fixture(scope="function")
def clean_environment():
    """Clean up test environment after each test."""
    yield
    # Cleanup code here
    # Remove test files, clear caches, etc.

# Hook to print test execution time
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Log slow tests."""
    if call.when == "call":
        duration = call.stop - call.start
        if duration > 1.0:  # Warn if test takes > 1 second
            print(f"\n⚠️  Slow test: {item.nodeid} took {duration:.2f}s")
```

---

## 📝 Writing Tests

### Example Test Module Structure

```python
# tests/Core/test_fractal_concept.py
"""
Tests for fractal concept and seed-bloom architecture.
"""
import pytest
from Core.Intelligence.fractal_concept import FractalSeed, Hippocampus

class TestFractalSeed:
    """Test suite for FractalSeed class."""
    
    # Fixtures specific to this test class
    @pytest.fixture
    def seed_with_bonds(self, sample_seed):
        """Create seed with causal bonds."""
        sample_seed.add_causal_bond("Hope")
        sample_seed.add_causal_bond("Joy")
        return sample_seed
    
    # Unit tests
    @pytest.mark.unit
    def test_seed_creation(self, sample_seed):
        """Test basic seed creation."""
        assert sample_seed.concept == "Love"
        assert sample_seed.frequency == 528.0
        assert len(sample_seed.sub_concepts) == 3
    
    @pytest.mark.unit
    def test_add_sub_concept(self, sample_seed):
        """Test adding sub-concepts."""
        initial_count = len(sample_seed.sub_concepts)
        sample_seed.add_sub_concept("Harmony")
        assert len(sample_seed.sub_concepts) == initial_count + 1
        assert "Harmony" in sample_seed.sub_concepts
    
    @pytest.mark.unit
    def test_invalid_frequency_raises_error(self):
        """Test that invalid frequency raises ValueError."""
        with pytest.raises(ValueError, match="Frequency must be positive"):
            FractalSeed(concept="Test", frequency=-100.0)
    
    @pytest.mark.unit
    def test_empty_concept_raises_error(self):
        """Test that empty concept raises ValueError."""
        with pytest.raises(ValueError, match="Concept cannot be empty"):
            FractalSeed(concept="", frequency=100.0)
    
    # Integration tests
    @pytest.mark.integration
    def test_seed_storage_and_retrieval(self, temp_db_path):
        """Test storing and retrieving seeds from Hippocampus."""
        hippocampus = Hippocampus(db_path=temp_db_path)
        
        # Create and store seed
        seed = FractalSeed(concept="Hope", frequency=852.0)
        hippocampus.store_seed(seed)
        
        # Retrieve and verify
        retrieved = hippocampus.retrieve_seed("Hope")
        assert retrieved is not None
        assert retrieved.concept == "Hope"
        assert retrieved.frequency == 852.0
    
    # Performance tests
    @pytest.mark.performance
    @pytest.mark.timeout(5)
    def test_bloom_performance(self, sample_seed):
        """Test that blooming completes within time limit."""
        from Core.Foundation.resonance_field import ResonanceField
        
        field = ResonanceField()
        waves = field.bloom(sample_seed, depth=5)
        
        # Should complete in < 5 seconds
        assert len(waves) > 0
    
    # Parametrized tests
    @pytest.mark.unit
    @pytest.mark.parametrize("concept,frequency", [
        ("Love", 528.0),
        ("Hope", 852.0),
        ("Joy", 600.0),
        ("Peace", 432.0),
    ])
    def test_various_seeds(self, concept, frequency):
        """Test seed creation with various values."""
        seed = FractalSeed(concept=concept, frequency=frequency)
        assert seed.concept == concept
        assert seed.frequency == frequency

class TestHippocampus:
    """Test suite for Hippocampus (memory storage)."""
    
    @pytest.mark.integration
    def test_hippocampus_initialization(self, temp_db_path):
        """Test Hippocampus initialization."""
        hippocampus = Hippocampus(db_path=temp_db_path)
        assert hippocampus.db_path == temp_db_path
        assert temp_db_path.exists()
    
    @pytest.mark.integration
    def test_store_multiple_seeds(self, temp_db_path):
        """Test storing multiple seeds."""
        hippocampus = Hippocampus(db_path=temp_db_path)
        
        seeds = [
            FractalSeed(concept="Love", frequency=528.0),
            FractalSeed(concept="Hope", frequency=852.0),
            FractalSeed(concept="Joy", frequency=600.0),
        ]
        
        for seed in seeds:
            hippocampus.store_seed(seed)
        
        # Verify all stored
        for seed in seeds:
            retrieved = hippocampus.retrieve_seed(seed.concept)
            assert retrieved is not None
    
    @pytest.mark.integration
    def test_seed_compression(self, temp_db_path, sample_seed):
        """Test that seeds are compressed when stored."""
        hippocampus = Hippocampus(db_path=temp_db_path)
        
        # Store seed
        hippocampus.store_seed(sample_seed)
        
        # Get storage size
        import os
        db_size = os.path.getsize(temp_db_path)
        
        # Should be small due to compression
        assert db_size < 10000  # Less than 10KB for a single seed
```

---

## 🚀 Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/Core/test_fractal_concept.py

# Run specific test class
pytest tests/Core/test_fractal_concept.py::TestFractalSeed

# Run specific test
pytest tests/Core/test_fractal_concept.py::TestFractalSeed::test_seed_creation

# Run tests matching pattern
pytest -k "seed and creation"

# Run tests with specific marker
pytest -m unit
pytest -m integration
pytest -m "not slow"

# Run tests with verbose output
pytest -v

# Run tests with detailed output
pytest -vv

# Stop at first failure
pytest -x

# Show local variables in tracebacks
pytest -l

# Run tests in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest -n auto
```

### Coverage Reports

```bash
# Run tests with coverage
pytest --cov=Core --cov-report=html --cov-report=term

# View HTML coverage report
# Open htmlcov/index.html in browser

# Show missing line numbers
pytest --cov=Core --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=Core --cov-fail-under=80
```

### Watching for Changes

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests automatically on file changes
ptw
ptw -- -v  # with verbose output
ptw -- -m unit  # only unit tests
```

---

## 🎭 Mocking and Patching

### Mocking External Dependencies

```python
import pytest
from unittest.mock import Mock, patch, MagicMock

class TestGeminiAPI:
    """Test Gemini API integration."""
    
    @pytest.mark.unit
    @patch('google.generativeai.configure')
    @patch('google.generativeai.GenerativeModel')
    def test_api_initialization(self, mock_model, mock_configure, mock_api_key):
        """Test API initialization with mocked Gemini."""
        from Core.Evolution.gemini_api import GeminiAPI
        
        api = GeminiAPI()
        
        # Verify API was configured
        mock_configure.assert_called_once()
        mock_model.assert_called_once()
    
    @pytest.mark.unit
    @patch('Core.Evolution.gemini_api.GeminiAPI.think')
    def test_thought_generation(self, mock_think):
        """Test thought generation with mocked API."""
        # Set up mock return value
        mock_think.return_value = "This is a test thought"
        
        from Core.Evolution.gemini_api import GeminiAPI
        api = GeminiAPI()
        
        result = api.think("What is love?")
        
        assert result == "This is a test thought"
        mock_think.assert_called_once_with("What is love?")

class TestDatabaseOperations:
    """Test database operations with mocking."""
    
    @pytest.mark.unit
    def test_database_connection(self, mocker):
        """Test database connection with mocker fixture."""
        # Mock sqlite3.connect
        mock_connect = mocker.patch('sqlite3.connect')
        mock_cursor = Mock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        from Core.Foundation.Memory.hippocampus import Hippocampus
        hippocampus = Hippocampus(db_path=":memory:")
        
        # Verify connection was made
        mock_connect.assert_called()
```

---

## 🔄 Continuous Integration

### GitHub Actions Configuration

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.12']
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pytest-asyncio
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=Core --cov-report=xml --cov-report=term
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
        fail_ci_if_error: true
```

---

## 📊 Test Metrics

### Coverage Goals

- **Overall**: 70%+ coverage
- **Core Systems**: 80%+ coverage
- **Critical Paths**: 90%+ coverage

### Test Execution Targets

- **Unit Tests**: < 100ms per test
- **Integration Tests**: < 1s per test
- **E2E Tests**: < 10s per test
- **Total Suite**: < 5 minutes

### Quality Metrics

Track these metrics:
- Test count over time
- Coverage percentage over time
- Failed test ratio
- Flaky test count
- Test execution time

---

## 🐛 Debugging Tests

### Using pytest debugger

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of test
pytest --trace

# Show local variables on failure
pytest -l
```

### Using print statements

```python
def test_something():
    result = calculate()
    print(f"DEBUG: result = {result}")  # Will be captured
    assert result > 0

# Show captured output
pytest -s  # or --capture=no
```

### Using logging

```python
import logging

def test_with_logging(caplog):
    """Test with log capturing."""
    caplog.set_level(logging.DEBUG)
    
    # Code that logs
    function_that_logs()
    
    # Check logs
    assert "Expected message" in caplog.text
```

---

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Test-Driven Development (TDD)](https://en.wikipedia.org/wiki/Test-driven_development)

---

*Last Updated: 2025-12-02*
*Version: 1.0*
