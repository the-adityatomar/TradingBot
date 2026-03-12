@echo off
REM GitHub Setup and Push Script for Trading Bot
REM This script initializes git and pushes to GitHub

setlocal enabledelayedexpansion

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  Trading Bot - GitHub Setup & Push                       ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Get the project directory
set PROJECT_DIR=%CD%

echo Project Directory: %PROJECT_DIR%
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Error: Git is not installed
    echo   Please install Git from https://git-scm.com/
    exit /b 1
)

echo ✓ Git is installed
git --version
echo.

REM Check if already a git repository
if exist "%PROJECT_DIR%\.git" (
    echo ✓ Git repository already initialized
    echo.
    echo Current remote:
    git remote -v
) else (
    echo Initializing git repository...
    
    REM Initialize git
    git init
    
    echo.
    echo Configure git user (leave blank to skip):
    set /p GIT_USER="Git Username (e.g., First Last): "
    
    if not "!GIT_USER!"=="" (
        set /p GIT_EMAIL="Git Email (e.g., your@email.com): "
        git config user.name "!GIT_USER!"
        git config user.email "!GIT_EMAIL!"
        echo ✓ Git user configured
    )
    
    echo ✓ Git repository initialized
    echo.
)

REM Stage files
echo Staging files...
git add .
echo ✓ Files staged

REM Create initial commit if needed
git diff --cached --quiet
if errorlevel 1 (
    echo.
    set /p COMMIT_MSG="Commit message (default: Initial commit): "
    if "!COMMIT_MSG!"=="" set "COMMIT_MSG=Initial commit: Production-ready Binance Futures Trading Bot"
    
    git commit -m "!COMMIT_MSG!"
    echo ✓ Changes committed
) else (
    echo ℹ No changes to commit
)

REM Add remote
echo.
set /p REPO_URL="GitHub Repository URL (e.g., https://github.com/username/TradingBot.git): "

if not "!REPO_URL!"=="" (
    git remote remove origin 2>nul
    git remote add origin !REPO_URL!
    echo ✓ Remote added: !REPO_URL!
) else (
    echo ℹ No repository URL provided
    echo   To add later, run: git remote add origin your-repo-url
    exit /b 0
)

REM Rename branch to main
echo.
echo Checking branch name...
for /f "tokens=*" %%A in ('git rev-parse --abbrev-ref HEAD') do set CURRENT_BRANCH=%%A
echo Current branch: !CURRENT_BRANCH!

if not "!CURRENT_BRANCH!"=="main" (
    echo Renaming branch to main...
    git branch -M main
    echo ✓ Branch renamed to main
)

REM Push to GitHub
echo.
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║  Ready to Push to GitHub                                 ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Repository URL: !REPO_URL!
echo Branch: main
echo.
set /p CONFIRM="Ready to push? (y/n): "

if /i "!CONFIRM!"=="y" (
    echo.
    echo Pushing to GitHub...
    git push -u origin main
    
    if errorlevel 1 (
        echo.
        echo ✗ Push failed. Common solutions:
        echo.
        echo 1. Authentication Issue:
        echo    - Use GitHub CLI: gh auth login
        echo    - Or use Personal Access Token for HTTPS
        echo.
        echo 2. Check remote URL:
        echo    git remote -v
        echo.
        echo 3. Retry:
        echo    git push -u origin main
        exit /b 1
    ) else (
        echo.
        echo ╔══════════════════════════════════════════════════════════╗
        echo ║  ✓ Successfully Pushed to GitHub!                        ║
        echo ╚══════════════════════════════════════════════════════════╝
        echo.
        echo Next steps:
        echo   1. Go to: !REPO_URL!
        echo   2. Settings ^> Secrets and variables ^> Actions
        echo   3. Add BINANCE_API_KEY secret
        echo   4. Add BINANCE_API_SECRET secret
        echo   5. Your CI/CD pipeline will run automatically
        echo.
    )
) else (
    echo.
    echo ℹ Push cancelled
    echo   To push later, run: git push -u origin main
)

echo.
