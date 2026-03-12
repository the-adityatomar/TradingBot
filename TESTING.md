# Testing Guide for Trading Bot

## Test Scenarios

### ✓ Test 1: Market Buy Order

```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**Expected Results:**
- Order placed successfully
- Status: FILLED
- Executed quantity matches order quantity
- Log file created in `logs/` directory

### ✓ Test 2: Market Sell Order

```bash
python trading_bot/cli.py -s ETHUSDT -S SELL -t MARKET -q 0.5
```

**Expected Results:**
- Order placed successfully
- Status: FILLED
- Side: SELL
- Log entry shows order details

### ✓ Test 3: Limit Buy Order

```bash
python trading_bot/cli.py -s BNBUSDT -S BUY -t LIMIT -q 0.1 -p 300.00
```

**Expected Results:**
- Order placed successfully
- Status: NEW (not filled immediately)
- Price: 300.00
- Executed quantity: 0 (until price matches)

### ✓ Test 4: Limit Sell Order

```bash
python trading_bot/cli.py -s BTCUSDT -S SELL -t LIMIT -q 0.01 -p 50000
```

**Expected Results:**
- Order placed successfully
- Status: NEW
- Time in Force: GTC (Good Till Cancel)

### ✓ Test 5: Stop-Limit Order

```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t STOP_LIMIT -q 0.01 -p 40000 --stop-price 39000
```

**Expected Results:**
- Order placed successfully
- Price: 40000
- Stop Price: 39000

---

## Validation Tests (Should Fail Gracefully)

### ✗ Test 6: Invalid Symbol

```bash
python trading_bot/cli.py -s INVALID -S BUY -t MARKET -q 0.01
```

**Expected Error:**
```
❌ Symbol validation failed: Symbol too short (minimum 6 characters like BTCUSDT)
```

### ✗ Test 7: Invalid Side

```bash
python trading_bot/cli.py -s BTCUSDT -S INVALID -t MARKET -q 0.01
```

**Expected Error:**
```
❌ Side validation failed: Side must be one of {'BUY', 'SELL'}, got INVALID
```

### ✗ Test 8: Invalid Quantity

```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0
```

**Expected Error:**
```
❌ Quantity validation failed: Quantity must be positive, got 0
```

### ✗ Test 9: Missing Price for LIMIT Order

```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t LIMIT -q 0.01
```

**Expected Error:**
```
❌ Price is required for LIMIT orders
```

### ✗ Test 10: Invalid Price

```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t LIMIT -q 0.01 -p abc
```

**Expected Error:**
```
❌ Price validation failed: Price must be a valid number, got abc
```

### ✗ Test 11: Negative Quantity

```bash
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q -0.5
```

**Expected Error:**
```
❌ Quantity validation failed: Quantity must be positive, got -0.5
```

### ✗ Test 12: Non-USDT Trading Pair

```bash
python trading_bot/cli.py -s BTCBNB -S BUY -t MARKET -q 0.01
```

**Expected Error:**
```
❌ Symbol validation failed: Currently only USDT trading pairs are supported
```

---

## Demo Test

```bash
python demo.py
```

**Expected Results:**
- Shows input validation examples
- Demonstrates error handling
- Validates various scenarios
- No API credentials required
- Output shows validation results

---

## Log File Verification

After running orders, verify logs:

```bash
# List all log files
ls -la logs/

# View latest log
cat logs/trading_bot_*.log | tail -50

# Search for specific order
grep "Order ID:" logs/trading_bot_*.log
```

**Log Should Contain:**
- Order request details (symbol, side, quantity, price)
- API request and response
- Order response with orderId and status
- Timestamps for each action

---

## Error Scenarios

### ✗ Test 13: Missing API Credentials

```bash
# Don't set environment variables
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**Expected Error:**
```
❌ API credentials not found in environment variables
Please set BINANCE_API_KEY and BINANCE_API_SECRET
```

### ✗ Test 14: Network Connection Error

```bash
# Simulate network error by using invalid API key
export BINANCE_API_KEY=invalid_key
export BINANCE_API_SECRET=invalid_secret
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**Expected Result:**
- API error with proper error message
- Log file captures the error
- Application exits gracefully

---

## Programmatic Usage Test

```python
from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.validators import OrderValidator

# Test validation
validator = OrderValidator()
is_valid, msg = validator.validate_symbol("BTCUSDT")
print(f"Validation result: {is_valid}")

# Test with API (if credentials available)
api_key = "your_key"
api_secret = "your_secret"
client = BinanceFuturesClient(api_key, api_secret)
manager = OrderManager(client)

# Place order
response = manager.place_market_order("BTCUSDT", "BUY", 0.01)
print(f"Order ID: {response.get('orderId')}")
```

---

## Testing Checklist

- [ ] Market orders execute successfully
- [ ] Limit orders are placed and show NEW status
- [ ] Stop-limit orders can be placed
- [ ] Invalid symbols are rejected
- [ ] Invalid sides are rejected
- [ ] Invalid quantities are rejected
- [ ] Missing prices for limit orders are caught
- [ ] Non-numeric prices are rejected
- [ ] Log files are created correctly
- [ ] Log files contain complete order information
- [ ] Demo script runs without errors
- [ ] CLI help works: `python trading_bot/cli.py --help`
- [ ] All error messages are clear and actionable
- [ ] API credentials are properly required
- [ ] Timeout and connection errors are handled

---

## Performance Testing

Test with various quantity sizes:

```bash
# Minimum quantity
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001

# Large quantity
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 10.0

# Decimal precision
python trading_bot/cli.py -s BTCUSDT -S BUY -t MARKET -q 0.00123456
```

---

## Environment Testing

Test with different environment setups:

```bash
# Windows PowerShell
$env:BINANCE_API_KEY = "test_key"
$env:BINANCE_API_SECRET = "test_secret"

# Windows CMD
set BINANCE_API_KEY=test_key

# Linux/macOS
export BINANCE_API_KEY="test_key"
export BINANCE_API_SECRET="test_secret"
```

---

## Logging Verification

Check that logs contain:

```bash
# Check for timestamp format
grep "^2024-" logs/trading_bot_*.log

# Check for all log levels
grep "INFO\|DEBUG\|ERROR" logs/trading_bot_*.log

# Check for API interaction logs
grep "Making.*request\|API Response" logs/trading_bot_*.log

# Check for order details
grep "Order ID:\|Status:\|Quantity:" logs/trading_bot_*.log
```

All sample log files are provided:
- `logs/trading_bot_20240309_103045_market_order.log`
- `logs/trading_bot_20240309_114530_limit_order.log`
