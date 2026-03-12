@echo off
REM Windows Setup Script for Trading Bot
REM This script sets up the environment and installs dependencies

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  Trading Bot - Windows Setup                             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Error: Python is not installed or not in PATH
    echo   Please install Python 3.7 or higher from https://www.python.org/
    exit /b 1
)

echo ✓ Python is installed
python --version

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Error: pip is not installed
    exit /b 1
)

echo ✓ pip is installed

REM Install requirements
echo.
echo Installing dependencies...
pip install -r trading_bot/requirements.txt

if errorlevel 1 (
    echo ✗ Error: Failed to install dependencies
    exit /b 1
)

echo ✓ Dependencies installed successfully

REM Setup complete
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  Setup Complete!                                         ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo   1. Copy .env.example to .env and fill in your API credentials
echo   2. Set environment variables:
echo      set BINANCE_API_KEY=your_key
echo      set BINANCE_API_SECRET=your_secret
echo   3. Run the trading bot:
echo      python trading_bot/cli.py --help
echo.
