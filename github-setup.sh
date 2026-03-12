#!/bin/bash
# GitHub Setup and Push Script for Trading Bot

set -e  # Exit on error

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Trading Bot - GitHub Setup & Push                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR=$(pwd)
echo "Project Directory: $PROJECT_DIR"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "✗ Error: Git is not installed"
    echo "  Please install Git: https://git-scm.com/"
    exit 1
fi

echo "✓ Git is installed"
git --version
echo ""

# Check if already a git repository
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "✓ Git repository already initialized"
    echo ""
    echo "Current remote:"
    git remote -v
else
    echo "Initializing git repository..."
    
    # Initialize git
    git init
    
    echo ""
    read -p "Git Username (e.g., First Last): " GIT_USER
    if [ -n "$GIT_USER" ]; then
        read -p "Git Email (e.g., your@email.com): " GIT_EMAIL
        git config user.name "$GIT_USER"
        git config user.email "$GIT_EMAIL"
        echo "✓ Git user configured"
    fi
    
    echo "✓ Git repository initialized"
    echo ""
fi

# Stage files
echo "Staging files..."
git add .
echo "✓ Files staged"

# Create initial commit if needed
if git diff --cached --quiet; then
    echo "ℹ No changes to commit"
else
    echo ""
    read -p "Commit message (default: Initial commit): " COMMIT_MSG
    if [ -z "$COMMIT_MSG" ]; then
        COMMIT_MSG="Initial commit: Production-ready Binance Futures Trading Bot"
    fi
    
    git commit -m "$COMMIT_MSG"
    echo "✓ Changes committed"
fi

# Add remote
echo ""
read -p "GitHub Repository URL (e.g., https://github.com/username/TradingBot.git): " REPO_URL

if [ -n "$REPO_URL" ]; then
    git remote remove origin 2>/dev/null || true
    git remote add origin "$REPO_URL"
    echo "✓ Remote added: $REPO_URL"
else
    echo "ℹ No repository URL provided"
    echo "  To add later, run: git remote add origin your-repo-url"
    exit 0
fi

# Rename branch to main
echo ""
echo "Checking branch name..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo "Current branch: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Renaming branch to main..."
    git branch -M main
    echo "✓ Branch renamed to main"
fi

# Push to GitHub
echo ""
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Ready to Push to GitHub                                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Repository URL: $REPO_URL"
echo "Branch: main"
echo ""
read -p "Ready to push? (y/n): " CONFIRM

if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    echo ""
    echo "Pushing to GitHub..."
    if git push -u origin main; then
        echo ""
        echo "╔══════════════════════════════════════════════════════════╗"
        echo "║  ✓ Successfully Pushed to GitHub!                        ║"
        echo "╚══════════════════════════════════════════════════════════╝"
        echo ""
        echo "Next steps:"
        echo "  1. Go to: $REPO_URL"
        echo "  2. Settings > Secrets and variables > Actions"
        echo "  3. Add BINANCE_API_KEY secret"
        echo "  4. Add BINANCE_API_SECRET secret"
        echo "  5. Your CI/CD pipeline will run automatically"
        echo ""
    else
        echo ""
        echo "✗ Push failed. Common solutions:"
        echo ""
        echo "1. Authentication Issue:"
        echo "   - Use GitHub CLI: gh auth login"
        echo "   - Or use Personal Access Token for HTTPS"
        echo ""
        echo "2. Check remote URL:"
        echo "   git remote -v"
        echo ""
        echo "3. Retry:"
        echo "   git push -u origin main"
        exit 1
    fi
else
    echo ""
    echo "ℹ Push cancelled"
    echo "  To push later, run: git push -u origin main"
fi

echo ""
