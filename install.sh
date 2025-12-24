#!/bin/bash

# SnapBase Installation Helper for Linux/macOS
# This script checks for Python and guides users through setup

echo ""
echo "========================================"
echo "  SnapBase Installation Helper"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo ""
    echo "Install Python 3 using:"
    echo ""
    echo "  macOS (Homebrew):"
    echo "    brew install python3"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get install python3 python3-pip python3-venv"
    echo ""
    echo "  Fedora/RHEL:"
    echo "    sudo dnf install python3 python3-pip"
    echo ""
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version)
echo "[OK] $PYTHON_VERSION detected"
echo ""

# Check if pip is available for this Python
if ! python3 -m pip --version &> /dev/null; then
    echo "[ERROR] pip is not available for this Python interpreter"
    echo ""
    echo "Install or upgrade pip using:"
    echo ""
    echo "  macOS:"
    echo "    python3 -m ensurepip --upgrade || python3 -m pip install --upgrade pip"
    echo ""
    echo "  Ubuntu/Debian:"
    echo "    sudo apt-get install python3-pip"
    echo ""
    exit 1
fi

PIP_VERSION=$(python3 -m pip --version)
echo "[OK] $PIP_VERSION"
echo ""

# Check if git is installed (optional but recommended)
if ! command -v git &> /dev/null; then
    echo "[WARNING] Git is not installed (optional)"
    echo "To use git: https://git-scm.com/download/linux"
    echo ""
else
    GIT_VERSION=$(git --version)
    echo "[OK] $GIT_VERSION"
    echo ""
fi

# Check for MySQL client libraries (might be needed)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v mysql &> /dev/null; then
        echo "[WARNING] MySQL client not found (optional)"
        echo "Install with: sudo apt-get install mysql-client"
        echo ""
    fi
fi

# Install SnapBase
pip3 install -e .
echo "Installing SnapBase..."
echo ""

python3 -m pip install -e .

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Installation failed"
    echo ""
    echo "Troubleshooting:"
    echo "1. Make sure you're in the correct directory (sql-bot-3)"
    echo "2. Try running: python3 -m pip install --upgrade pip"
    echo "3. Check your internet connection"
    echo "4. For permission issues, try: python3 -m pip install --user -e ."
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "   Installation Complete!"
echo "========================================"
echo ""
echo "You can now use: snapbase"
echo ""
