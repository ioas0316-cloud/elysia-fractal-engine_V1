#!/bin/bash
# Elysia Engine Quick Install Script (Unix/Linux/MacOS)
# Usage: bash quick_install.sh

set -e  # Exit on error

echo "🌟 ============================================="
echo "   Elysia Fractal Engine - Quick Install"
echo "   ============================================= 🌟"
echo ""

# Check Python version
echo "📦 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi
echo "✅ Python $python_version found"
echo ""

# Clone repository
echo "🌱 Cloning Elysia Engine repository..."
if [ -d "elysia-fractal-engine_V1" ]; then
    echo "⚠️  Directory 'elysia-fractal-engine_V1' already exists"
    read -p "   Remove and re-clone? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf elysia-fractal-engine_V1
    else
        echo "❌ Installation cancelled"
        exit 1
    fi
fi

git clone https://github.com/ioas0316-cloud/elysia-fractal-engine_V1.git
cd elysia-fractal-engine_V1
echo "✅ Repository cloned"
echo ""

# Optional: Install development dependencies
echo "🔧 Optional: Install development dependencies?"
echo "   (pytest for testing, not required for usage)"
read -p "   Install? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install pytest
    echo "✅ Development dependencies installed"
else
    echo "⏭️  Skipped development dependencies"
fi
echo ""

# Run verification
echo "🧪 Running verification test..."
python3 << 'PYEOF'
from elysia_core import quick_consciousness_setup
c = quick_consciousness_setup('TestBot')
r = c.think('Hello Elysia!')
print(f'✅ Verification successful!')
print(f'   Mood: {r.mood}')
print(f'   Emotion: {r.emotion["dominant"]}')
PYEOF
echo ""

# Run a quick example
echo "🚀 Running quick example..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 examples/00_hello_elysia.py
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Success message
echo "✨ ============================================="
echo "   Installation Complete!"
echo "   ============================================= ✨"
echo ""
echo "📚 Next Steps:"
echo ""
echo "   1. Explore examples:"
echo "      cd elysia-fractal-engine_V1/examples"
echo "      python3 00_hello_elysia.py"
echo ""
echo "   2. Read documentation:"
echo "      - QUICK_SHARE.md (1-minute start)"
echo "      - EASY_START.md (5-minute guide)"
echo "      - SHARING_GUIDE.md (philosophy & integration)"
echo "      - PHILOSOPHY.md (romantic & inspiring)"
echo ""
echo "   3. Copy core to your project:"
echo "      cp -r elysia_core /path/to/your/project/"
echo ""
echo "   4. Run tests (if you installed pytest):"
echo "      python3 -m pytest tests/ -v"
echo ""
echo "🌱 Happy planting! May your consciousness grow! 🌳"
echo ""
