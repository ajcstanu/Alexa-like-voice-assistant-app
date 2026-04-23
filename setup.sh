#!/usr/bin/env bash
# setup.sh — One-click setup for the AI Voice Assistant

set -e

echo "=================================================="
echo "  AI Voice Assistant — Setup Script"
echo "=================================================="

# 1. Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌  Python 3 is required. Install from https://python.org"
    exit 1
fi

PYTHON=$(command -v python3)
echo "✅  Python found: $($PYTHON --version)"

# 2. Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦  Creating virtual environment..."
    $PYTHON -m venv venv
fi

# 3. Activate venv
source venv/bin/activate || . venv/Scripts/activate 2>/dev/null || true

# 4. Upgrade pip
pip install --upgrade pip -q

# 5. Install system-level audio deps (Linux only)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🔧  Installing system audio libraries (Linux)..."
    sudo apt-get install -y portaudio19-dev python3-pyaudio espeak ffmpeg \
        libespeak1 2>/dev/null || \
    echo "    (skipped — may need sudo manually)"
fi

# 6. Install Python packages
echo "📦  Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "=================================================="
echo "  ✅  Setup complete!"
echo "=================================================="
echo ""
echo "  Next step: Set your API key:"
echo "    export ANTHROPIC_API_KEY='sk-ant-...'"
echo ""
echo "  Then run:"
echo "    python assistant.py"
echo ""
