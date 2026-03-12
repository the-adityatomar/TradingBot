# GitHub Secrets Setup Guide

## Overview

GitHub Secrets are encrypted environment variables that can be used in GitHub Actions workflows. They're perfect for storing sensitive credentials like API keys.

**Key Benefits:**
- ✓ Encrypted at rest
- ✓ Never logged or displayed
- ✓ Automatically masked in logs
- ✓ Accessible only to workflows
- ✓ Different per repository

---

## Step-by-Step Setup

### Step 1: Navigate to Repository Settings

1. Go to your GitHub repository: `https://github.com/the-adityatomar/TradingBot`
2. Click on the **Settings** tab at the top
3. In the left sidebar, click on **Secrets and variables**
4. Click on **Actions**

You should see a page titled "Secrets" with:
- "Repository secrets" section
- A "New repository secret" button

### Step 2: Create BINANCE_API_KEY Secret

1. Click **New repository secret**
2. Fill in the form:
   - **Name:** `BINANCE_API_KEY` (exactly this)
   - **Value:** Paste your Binance Futures Testnet API key
3. Click **Add secret**

### Step 3: Create BINANCE_API_SECRET Secret

1. Click **New repository secret**
2. Fill in the form:
   - **Name:** `BINANCE_API_SECRET` (exactly this)
   - **Value:** Paste your Binance Futures Testnet API secret
3. Click **Add secret**

### Step 4: Verify Secrets Are Set

You should now see both secrets listed:
- ✓ `BINANCE_API_KEY`
- ✓ `BINANCE_API_SECRET`

The values are hidden (shown as dots) after creation.

---

## Obtaining New Binance Credentials

If you haven't created API credentials yet:

### For Binance Futures Testnet:

1. Go to https://testnet.binancefuture.com/
2. Sign in with your account
3. Click on your profile icon (top right)
4. Select **API Management**
5. Create new API key by clicking **Create API key**
6. Choose API Type: **Testnet Trading**
7. Name it something like: `TradingBot-GitHub`
8. Click **Create**
9. You'll see:
   - **API Key** - Copy this to GitHub Secret `BINANCE_API_KEY`
   - **Secret Key** - Copy this to GitHub Secret `BINANCE_API_SECRET`

**Important:** For testnet, use https://testnet.binancefuture.com - NOT the main Binance site

---

## Using Secrets in GitHub Actions

The workflow file (`.github/workflows/test-deploy.yml`) automatically uses these secrets:

```yaml
- name: Run Trading Bot
  env:
    BINANCE_API_KEY: ${{ secrets.BINANCE_API_KEY }}
    BINANCE_API_SECRET: ${{ secrets.BINANCE_API_SECRET }}
  run: |
    python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

The `${{ secrets.BINANCE_API_KEY }}` syntax securely injects the secret.

---

## Security Features

### Automatic Masking
When your workflow runs, any output containing the secret value is automatically masked:

```
Run python trading_bot/cli.py
Placing order...
***  ← Secret is masked
Order placed successfully
```

### No History Exposure
- Secrets are never stored in git history
- Secrets can't be viewed once created (only edited/deleted)
- Each user can see which secrets are configured (not the values)
- Audit log shows who accessed/modified secrets

### Scope & Permissions
- Secrets are repository-specific
- Different repos can have different secrets
- Secrets only available to authorized workflows
- Branch protection can restrict who can modify workflows using secrets

---

## Accessing Secrets in Your Code

### For Local Development (using .env)

**Create `.env` file (local only, never commit):**
```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
```

**Load in Python:**
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
```

**Install python-dotenv:**
```bash
pip install python-dotenv
```

### For GitHub Actions (automatic)

GitHub Actions automatically makes secrets available as environment variables:

```python
import os

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
```

The secrets are injected by the workflow, no additional setup needed.

---

## Troubleshooting

### Issue: "Secret not found" in workflow

**Solution:**
1. Check the secret name matches exactly (case-sensitive)
2. Verify it's in the **Repository secrets** (not organization secrets)
3. Trigger a new workflow run after adding the secret

### Issue: Can't see the secret value

**This is normal!** GitHub doesn't show secret values for security. To verify:
1. Use the secret in a workflow
2. The masked output `***` indicates it was found

### Issue: Need to update secret

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Find the secret
3. Click **Update** on the right
4. Paste the new value
5. Click **Update secret**

### Issue: Accidentally exposed a secret

**Immediately:**
1. Delete the secret from GitHub
2. Regenerate the API key on Binance Testnet
3. Add the new credentials as a secret

**Long-term:**
- Monitor your Binance account for suspicious activity
- Review API key access logs on Binance

---

## Best Practices

### 1. Key Rotation
- Rotate API keys every 30 days
- Invalidate old keys immediately
- Create separate keys per environment (testnet vs production)

### 2. Principle of Least Privilege
- Use API key restrictions on Binance dashboard
- Restrict to Testnet Trading only
- Limit IP whitelist if possible

### 3. Monitoring
- Monitor for unauthorized access | Check GitHub Actions logs regularly
- Review Binance API key activity logs
- Set up alerts for unusual trading activity

### 4. Backup & Recovery
- Store backup credentials securely (not in git)
- Use a password manager to store backup credentials
- Document the process for regenerating credentials

### 5. Cleanup
- Remove secrets from repositories you no longer maintain
- Invalidate old API keys that aren't in use
- Archive old workflows that used credentials

---

## Workflow Trigger & Execution

### Automatic Triggers
Your workflow runs automatically when:
- ✓ Code is pushed to any branch
- ✓ Pull requests are created
- ✓ Manual trigger via Actions tab (optional)

### Manual Trigger
To manually run the workflow:
1. Go to your repository
2. Click **Actions** tab
3. Select **Trading Bot - Test & Deploy**
4. Click **Run workflow**
5. Select the branch
6. Click **Run workflow**

### View Logs
1. Go to **Actions** tab
2. Click on the workflow run
3. Click on the specific job
4. View step-by-step output

---

## Next Steps

1. ✓ Generate new Binance API credentials
2. ✓ Add secrets to GitHub repository
3. ✓ Push code to GitHub (triggers workflow)
4. ✓ Monitor **Actions** tab for workflow execution
5. ✓ Verify no errors in logs (secrets will be masked)

---

## Reference

- GitHub Secrets Documentation: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- GitHub Actions Documentation: https://docs.github.com/en/actions
- Binance Testnet: https://testnet.binancefuture.com
