#!/bin/bash
# Unix/Linux/macOS Setup Script for Trading Bot

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Trading Bot - Unix Setup                                ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Error: Python 3 is not installed"
    echo "  Please install Python 3.7 or higher"
    exit 1
fi

echo "✓ Python is installed"
python3 --version

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "✗ Error: pip3 is not installed"
    exit 1
fi

echo "✓ pip3 is installed"

# Install requirements
echo ""
echo "Installing dependencies..."
pip3 install -r trading_bot/requirements.txt

if [ $? -ne 0 ]; then
    echo "✗ Error: Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"

# Setup complete
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Setup Complete!                                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and fill in your API credentials"
echo "  2. Set environment variables:"
echo "     export BINANCE_API_KEY='your_key'"
echo "     export BINANCE_API_SECRET='your_secret'"
echo "  3. Run the trading bot:"
echo "     python3 trading_bot/cli.py --help"
echo ""
