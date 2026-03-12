# Quick Start Guide

## 5 Minute Quick Start

### 1. Setup Environment (1 minute)

**Windows:**
```bash
# Run setup script
setup.bat

# Or manually:
pip install -r trading_bot/requirements.txt
```

**macOS/Linux:**
```bash
# Make script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Or manually:
pip3 install -r trading_bot/requirements.txt
```

### 2. Configure API Credentials (2 minutes)

**Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY = "your_api_key_here"
$env:BINANCE_API_SECRET = "your_api_secret_here"
```

**Windows (Command Prompt):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

**macOS/Linux:**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

### 3. Place Your First Order (2 minutes)

**Market Order:**
```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**Limit Order:**
```bash
python trading_bot/cli.py -s ETHUSDT -S SELL -t LIMIT -q 1.0 -p 2500
```

## Demo (No API Credentials Required)

Run the demo script to see validation and error handling in action:

```bash
python demo.py
```

## Expected Output

```
============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:       BTCUSDT
Side:         BUY
Type:         MARKET
Quantity:     0.01
============================================================

============================================================
ORDER RESPONSE DETAILS
============================================================
✓ ORDER PLACED SUCCESSFULLY
  Order ID:              1234567890
  Status:                FILLED
  Symbol:                BTCUSDT
  Side:                  BUY
  Type:                  MARKET
  Quantity:              0.01
  Executed Quantity:     0.01
  Price:                 45000.00
  Average Price:         45000.00
  Time in Force:         GTC
============================================================
```

## Check Logs

All orders are logged to the `logs/` directory:

```bash
# View latest log
cat logs/trading_bot_*.log
```

## Troubleshooting

### "API credentials not found"
- Make sure environment variables are set
- For PowerShell: $env:BINANCE_API_KEY, $env:BINANCE_API_SECRET
- For Bash: echo $BINANCE_API_KEY

### "Connection refused"
- Check internet connection
- Verify testnet is accessible: https://testnet.binancefuture.com
- Check firewall/VPN settings

### "Invalid API key"
- Verify API key is from Binance Futures Testnet
- Check for trailing spaces in credentials
- Regenerate credentials if needed

## View Full Documentation

See [README.md](README.md) for complete documentation.
