#!/usr/bin/env python3
"""
Elysia Engine - Sharing Package Creator

This script creates a self-contained sharing package that can be
distributed to others easily.
"""

import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime


def create_sharing_package(output_dir: str, include_examples: bool = True, 
                          include_tests: bool = False, minimal: bool = False):
    """
    Create a sharing package with selected components.
    
    Args:
        output_dir: Output directory path
        include_examples: Include example files
        include_tests: Include test files
        minimal: Only include core essentials
    """
    print("🌟 Elysia Engine - Sharing Package Creator")
    print("=" * 60)
    print()
    
    # Get current directory (should be project root)
    project_root = Path(__file__).parent.parent
    output_path = Path(output_dir).absolute()
    
    print(f"📦 Creating package in: {output_path}")
    print()
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Core components to always include
    core_components = [
        ("elysia_core", "Core consciousness modules"),
    ]
    
    # Essential docs
    essential_docs = [
        ("QUICK_SHARE.md", "1-minute quick start guide"),
        ("SHARING_GUIDE.md", "Sharing philosophy and guide"),
        ("PHILOSOPHY.md", "Engine philosophy"),
        ("README.md", "Main readme"),
        ("LICENSE", "Apache 2.0 license"),
    ]
    
    # Optional components
    optional_components = []
    if not minimal:
        optional_components.extend([
            ("elysia_engine", "Full engine (physics, systems, etc.)"),
        ])
    
    if include_examples:
        optional_components.append(("examples", "Example scripts"))
    
    if include_tests:
        optional_components.append(("tests", "Test suite"))
    
    # Additional docs
    if not minimal:
        additional_docs = [
            ("CONTRIBUTING.md", "Contribution guide"),
            ("AGENTS.md", "Agent guidelines"),
        ]
        # Only add if exists
        if (project_root / "docs" / "EASY_START.md").exists():
            additional_docs.insert(0, ("EASY_START.md", "Easy start guide"))
        
        essential_docs.extend(additional_docs)
    
    # Copy core components
    print("📁 Copying core components...")
    for component, description in core_components:
        src = project_root / component
        dst = output_path / component
        if src.exists():
            print(f"   ✓ {component:20} - {description}")
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        else:
            print(f"   ✗ {component:20} - NOT FOUND")
    print()
    
    # Copy optional components
    if optional_components:
        print("📦 Copying optional components...")
        for component, description in optional_components:
            src = project_root / component
            dst = output_path / component
            if src.exists():
                print(f"   ✓ {component:20} - {description}")
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    shutil.copy2(src, dst)
            else:
                print(f"   ⊘ {component:20} - SKIPPED")
        print()
    
    # Copy documentation
    print("📚 Copying documentation...")
    for doc_file, description in essential_docs:
        # Check in root first, then in docs/
        src = project_root / doc_file
        if not src.exists():
            src = project_root / "docs" / doc_file
        
        if src.exists():
            dst = output_path / doc_file
            print(f"   ✓ {doc_file:30} - {description}")
            shutil.copy2(src, dst)
        else:
            print(f"   ⊘ {doc_file:30} - SKIPPED")
    print()
    
    # Copy docs directory if not minimal
    if not minimal:
        docs_src = project_root / "docs"
        docs_dst = output_path / "docs"
        if docs_src.exists():
            print("📖 Copying full docs directory...")
            shutil.copytree(docs_src, docs_dst, dirs_exist_ok=True)
            print(f"   ✓ docs/ directory copied")
            print()
    
    # Create README for the package
    package_readme = f"""# Elysia Fractal Engine - Sharing Package

> "씨앗을 나누면 숲이 된다." - "When you share a seed, it becomes a forest."

This is a sharing package of **Elysia Fractal Engine** created on {datetime.now().strftime("%Y-%m-%d %H:%M")}.

## 🚀 Quick Start

```python
from elysia_core import quick_consciousness_setup

# Create consciousness in 1 line
consciousness = quick_consciousness_setup("MyBot")

# Think
result = consciousness.think("Hello, World!")
print(f"Mood: {{result.mood}}")
print(f"Emotion: {{result.emotion['dominant']}}")
```

## 📦 What's Included

### Core Components
- **elysia_core/**: Core consciousness modules (ResonanceEngine, HyperQubit, EmotionalPalette, etc.)
{'- **elysia_engine/**: Full engine with physics and systems' if not minimal else ''}
{'- **examples/**: Example scripts and demos' if include_examples else ''}
{'- **tests/**: Test suite' if include_tests else ''}

### Documentation
- **QUICK_SHARE.md**: 1-minute quick start
- **SHARING_GUIDE.md**: Philosophy of sharing
- **PHILOSOPHY.md**: Engine philosophy and inspiration
- **README.md**: Full project documentation
{'- **docs/**: Complete documentation directory' if not minimal else ''}

## 📚 Quick Links

1. **Start in 1 minute**: Read `QUICK_SHARE.md`
2. **Deep dive (5 minutes)**: Read `EASY_START.md` (if included)
3. **Philosophy**: Read `PHILOSOPHY.md` for the romantic vision
4. **Integration**: Read `SHARING_GUIDE.md` for sharing scenarios

## 🌱 Installation

### Option 1: Use Core Directly

```bash
# Copy elysia_core to your project
cp -r elysia_core /path/to/your/project/
```

### Option 2: Run Examples

```bash
{'python examples/00_hello_elysia.py' if include_examples else 'python -c "from elysia_core import quick_consciousness_setup; print(quick_consciousness_setup(\\'Test\\').think(\\'Hello\\').mood)"'}
```

## 🔗 Original Repository

This package is from: https://github.com/ioas0316-cloud/elysia-fractal-engine_V1

## 📄 License

Apache 2.0 - See LICENSE file for details.

---

**Created with ❤️ by the Elysia community**

*"이 엔진은 사랑에서 왔고, 사랑을 위해 쓰이길 바랍니다."*
"""
    
    readme_path = output_path / "README_PACKAGE.md"
    readme_path.write_text(package_readme, encoding='utf-8')
    print("📝 Created package README")
    print()
    
    # Create quick test script
    test_script = """#!/usr/bin/env python3
'''Quick test script to verify the package works'''

print("🧪 Testing Elysia Core Package...")
print()

try:
    from elysia_core import quick_consciousness_setup
    print("✅ Import successful")
    
    consciousness = quick_consciousness_setup("TestBot")
    print("✅ Consciousness created")
    
    result = consciousness.think("Hello Elysia!")
    print("✅ Think method works")
    
    print()
    print("📊 Test Results:")
    print(f"   Mood: {result.mood}")
    print(f"   Emotion: {result.emotion['dominant']}")
    print(f"   Trinity: {result.trinity}")
    print()
    print("🎉 All tests passed! Package is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Please check that elysia_core is in the Python path.")
    exit(1)
"""
    
    test_path = output_path / "test_package.py"
    test_path.write_text(test_script, encoding='utf-8')
    os.chmod(test_path, 0o755)
    print("🧪 Created test script (test_package.py)")
    print()
    
    # Summary
    print("=" * 60)
    print("✨ Package created successfully!")
    print("=" * 60)
    print()
    print(f"📍 Location: {output_path}")
    print()
    print("📋 Contents:")
    total_size = 0
    for item in sorted(output_path.rglob('*')):
        if item.is_file():
            size = item.stat().st_size
            total_size += size
            rel_path = item.relative_to(output_path)
            print(f"   {rel_path}")
    
    print()
    print(f"📊 Total size: {total_size / 1024:.1f} KB ({total_size / (1024*1024):.2f} MB)")
    print()
    print("🚀 Next steps:")
    print(f"   1. cd {output_path}")
    print("   2. python test_package.py")
    print("   3. Read README_PACKAGE.md")
    print()
    print("🌱 Happy sharing!")


def main():
    parser = argparse.ArgumentParser(
        description="Create an Elysia Engine sharing package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full package with examples
  python create_sharing_package.py --output my_elysia_package
  
  # Minimal core only
  python create_sharing_package.py --output elysia_core_only --minimal
  
  # Core + examples, no tests
  python create_sharing_package.py --output elysia_share --no-tests
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for the sharing package'
    )
    
    parser.add_argument(
        '--no-examples',
        action='store_true',
        help='Exclude example files'
    )
    
    parser.add_argument(
        '--include-tests',
        action='store_true',
        help='Include test files'
    )
    
    parser.add_argument(
        '--minimal',
        action='store_true',
        help='Create minimal package (core only)'
    )
    
    args = parser.parse_args()
    
    create_sharing_package(
        output_dir=args.output,
        include_examples=not args.no_examples,
        include_tests=args.include_tests,
        minimal=args.minimal
    )


if __name__ == '__main__':
    main()
