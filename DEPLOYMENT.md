# GitHub Deployment & Safe Credential Management

## Setup Instructions

### 1. Create a New GitHub Repository

1. Go to https://github.com/new
2. Create repository: `TradingBot`
3. Make it **Private** (for security)
4. Don't initialize with README (we already have one)
5. Copy the repository URL

### 2. Configure GitHub Secrets (Safe Credential Management)

GitHub Secrets are encrypted and never logged or exposed:

**Steps:**
1. Go to your repository: https://github.com/the-adityatomar/TradingBot
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add `BINANCE_API_KEY`
   - Name: `BINANCE_API_KEY`
   - Value: Your API key
   - Click **Add secret**
5. Add `BINANCE_API_SECRET`
   - Name: `BINANCE_API_SECRET`
   - Value: Your API secret
   - Click **Add secret**

**Security Features:**
- ✓ Encrypted at rest
- ✓ Never logged in CI/CD output
- ✓ Only accessible to workflows
- ✓ Masked in logs automatically
- ✓ No history exposure

### 3. Initialize Local Git Repository

```bash
cd "c:\Users\adity\OneDrive\Desktop\Studies\Projects\DataAnalytics Projects\PrimeTradeAI"

# Initialize git
git init

# Configure git user (use your GitHub account)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Or globally (one time):
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Production-ready Binance Futures Trading Bot"
```

### 4. Add Remote and Push to GitHub

```bash
# Add remote (replace with your repo URL)
git remote add origin https://github.com/the-adityatomar/TradingBot.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**You may need to authenticate:**
- Use GitHub Personal Access Token (recommended for security)
- Or GitHub CLI: `gh auth login`
- Or HTTPS with password

### 5. Access Secrets in Workflows

Secrets are only accessible to GitHub Actions workflows:

```yaml
- name: Use API Key
  env:
    BINANCE_API_KEY: ${{ secrets.BINANCE_API_KEY }}
    BINANCE_API_SECRET: ${{ secrets.BINANCE_API_SECRET }}
  run: |
    python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

The secrets are:
- ✓ Never printed in logs
- ✓ Automatically masked
- ✓ Only available to authorized workflows
- ✓ Different for each repository

---

## CI/CD Pipeline Overview

The `.github/workflows/test-deploy.yml` includes:

### 1. Test Job
- Installs Python 3.10
- Installs dependencies
- Runs linting (flake8)
- Runs demo script (no credentials needed)
- Validates core functionality

### 2. Deploy Job
- Runs only on pushes to `main` branch
- Installs dependencies
- Verifies credentials are configured
- Uploads logs as artifacts
- Runs only if tests pass

### 3. Security Check Job
- Scans for hardcoded secrets
- Uses Bandit for security analysis
- Checks for exposed credentials
- Prevents accidental credential commits

---

## Local Development with Credentials

### Option 1: Environment Variables (Recommended)

**Windows PowerShell:**
```powershell
$env:BINANCE_API_KEY = "your_key_here"
$env:BINANCE_API_SECRET = "your_secret_here"

# Run bot
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**Windows Command Prompt:**
```cmd
set BINANCE_API_KEY=your_key_here
set BINANCE_API_SECRET=your_secret_here

python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**macOS/Linux:**
```bash
export BINANCE_API_KEY="your_key_here"
export BINANCE_API_SECRET="your_secret_here"

python3 trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

### Option 2: .env File (Local Only - Never Commit)

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

3. Load in script (use `python-dotenv`):
```bash
pip install python-dotenv
```

4. Load in your code:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
```

**Important:** `.env` is in `.gitignore` - never committed to Git

### Option 3: System Environment Variables

**Windows (Permanent):**
1. Right-click **This PC** → **Properties**
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. Click **New** under User variables
5. Add `BINANCE_API_KEY` and `BINANCE_API_SECRET`
6. Restart terminal/IDE

**macOS/Linux (in ~/.bashrc or ~/.zshrc):**
```bash
export BINANCE_API_KEY="your_key_here"
export BINANCE_API_SECRET="your_secret_here"
```

---

## Security Best Practices

### 1. Credentials Management
- ✓ Never commit `.env` to Git
- ✓ Use GitHub Secrets for CI/CD
- ✓ Use environment variables locally
- ✓ Rotate credentials regularly

### 2. Repository Settings
- ✓ Keep repository Private
- ✓ Enable branch protection on `main`
- ✓ Require reviews for PRs
- ✓ Enable vulnerability alerts

### 3. API Key Management
- ✓ Create separate keys for different environments (Testnet vs Production)
- ✓ Use API key restrictions in Binance dashboard
- ✓ Rotate keys monthly
- ✓ Monitor API key usage

### 4. Git Configuration
```bash
# Prevent accidental commits of .env
git rm --cached .env 2>/dev/null || true

# Verify .gitignore works
git status  # .env should NOT be listed
```

---

## Troubleshooting

### Issue: "fatal: not a git repository"
**Solution:**
```bash
cd /path/to/project
git init
```

### Issue: "Permission denied (publickey)"
**Solution:** Set up SSH key or use HTTPS with Personal Access Token
```bash
git remote set-url origin https://github.com/the-adityatomar/TradingBot.git
```

### Issue: "Support for password authentication was removed"
**Solution:** Use GitHub CLI or Personal Access Token
```bash
# Install GitHub CLI
# Then authenticate
gh auth login

# Try push again
git push
```

### Issue: Secrets not appearing in logs during CI/CD
**This is expected!** GitHub automatically masks secrets in logs:
```
Run python trading_bot/cli.py -s BTCUSDT
***
Order placed successfully
```

---

## Verification Checklist

After setup:

- [ ] Repository created on GitHub
- [ ] GitHub Secrets configured (BINANCE_API_KEY, BINANCE_API_SECRET)
- [ ] Local git repository initialized
- [ ] Changes committed locally
- [ ] Pushed to GitHub successfully
- [ ] GitHub Actions workflow triggered
- [ ] Tests passed in Actions
- [ ] Security check passed (no hardcoded credentials)
- [ ] `.env` file is in `.gitignore`
- [ ] `.env.example` is documented

---

## Accessing the Deployed Bot

### View CI/CD Status
- Go to **Actions** tab on your repository
- View workflow runs and logs

### Download Artifacts
- After workflow completes, click **Artifacts**
- Download `trading-bot-logs`

### View Credentials
- Go to **Settings** → **Secrets and variables**
- See list of configured secrets (values are hidden)

---

## Workflow Triggers

The workflow runs automatically on:
- ✓ Push to `main` or `master` branch
- ✓ Push to `develop` branch
- ✓ Pull requests to any of these branches

Manual trigger (optional):
1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**

---

## Next Steps

1. **Generate new Binance credentials** (don't reuse old ones)
2. **Add credentials to GitHub Secrets**
3. **Initialize git and push** to GitHub
4. **Monitor Actions** for successful workflow
5. **Test locally** with environment variables
6. **Monitor API usage** on Binance dashboard

