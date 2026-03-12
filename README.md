# Binance Futures Trading Bot (Testnet)

A simplified Python trading bot for placing orders on Binance Futures Testnet (USDT-M). This application provides a clean, reusable structure with proper logging, error handling, and input validation.

## Features

- **Market Orders**: Place market orders with instant execution
- **Limit Orders**: Place limit orders with custom price levels
- **Stop-Limit Orders**: Place stop-limit orders (bonus feature)
- **Structured Code**: Separate layers for API client, order management, and CLI
- **Comprehensive Logging**: Detailed logging of all API interactions and errors
- **Input Validation**: Robust validation of all user inputs
- **Error Handling**: Proper exception handling for network and API errors
- **CLI Interface**: User-friendly command-line interface with argparse

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance Futures API client wrapper
│   ├── orders.py                # Order placement logic
│   ├── validators.py            # Input validation utilities
│   └── logging_config.py        # Logging configuration
├── cli.py                       # CLI entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── logs/                        # Log files directory (auto-created)
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Binance Futures Testnet account with API credentials

### Step 1: Register on Binance Futures Testnet

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Create an account or log in
3. Go to API Management section
4. Create new API key and API secret
5. Enable futures trading on your testnet account

### Step 2: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd trading_bot

# Or extract the zip folder and navigate to it
cd trading_bot
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

### Step 4: Set Environment Variables

Set your API credentials as environment variables:

**On Windows (PowerShell):**
```powershell
$env:BINANCE_API_KEY = "your_api_key_here"
$env:BINANCE_API_SECRET = "your_api_secret_here"
```

**On Windows (Command Prompt):**
```cmd
set BINANCE_API_KEY=your_api_key_here
set BINANCE_API_SECRET=your_api_secret_here
```

**On macOS/Linux:**
```bash
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"
```

Or create a `.env` file in the project root and load it:

```bash
# Create .env file
echo "BINANCE_API_KEY=your_api_key_here" > .env
echo "BINANCE_API_SECRET=your_api_secret_here" >> .env

# Load environment variables (Unix/macOS)
set -a && source .env && set +a
```

## Usage

### Basic Usage

```bash
# Place a market order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Place a limit order
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 1.0 --price 2000

# Place a stop-limit order
python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.01 --price 40000 --stop-price 39000
```

### Command Line Options

```
-s, --symbol SYMBOL           Trading pair symbol (required, e.g., BTCUSDT)
-S, --side {BUY,SELL}        Order side (required)
-t, --type {MARKET,LIMIT,STOP_LIMIT}  Order type (required)
-q, --quantity QUANTITY       Order quantity (required)
-p, --price PRICE            Order price (required for LIMIT and STOP_LIMIT)
--stop-price STOP_PRICE      Stop price (required for STOP_LIMIT)
-v, --verbose                Enable verbose logging
-h, --help                   Show help message
```

### Examples

**Example 1: Market Buy Order**
```bash
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01
```

**Example 2: Limit Sell Order**
```bash
python cli.py -s ETHUSDT -S SELL -t LIMIT -q 1.0 -p 2500
```

**Example 3: Stop-Limit Order**
```bash
python cli.py -s BNBUSDT -S BUY -t STOP_LIMIT -q 0.1 -p 300 --stop-price 295
```

## Output

The application provides clear, structured output:

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

## Logging

All activities are logged to files in the `logs/` directory with timestamps:

- **Log File Format:** `trading_bot_YYYYMMDD_HHMMSS.log`
- **Log Levels:**
  - `DEBUG`: Detailed information for debugging (file only)
  - `INFO`: General information about order placement and API interactions
  - `ERROR`: Error messages and failures
  - `CRITICAL`: Critical failures

Sample log entry:
```
2024-03-09 10:30:45 - trading_bot - INFO - [cli.py:142] - Placing MARKET order: BUY 0.01 BTCUSDT
2024-03-09 10:30:45 - trading_bot - DEBUG - [client.py:89] - Making POST request to /fapi/v1/order
2024-03-09 10:30:46 - trading_bot - INFO - [client.py:107] - Order placed successfully: 1234567890
2024-03-09 10:30:46 - trading_bot - INFO - [orders.py:78] - === MARKET ORDER ===
```

## Error Handling

The application handles various error scenarios:

### Input Validation Errors
- Empty or invalid symbols
- Invalid order sides (not BUY/SELL)
- Invalid order types
- Negative or zero quantities
- Missing prices for limit orders
- Non-numeric price/quantity values

### API Errors
- Invalid API credentials
- Insufficient balance
- Network connectivity issues
- API rate limiting
- Invalid order parameters

### Example Error Output
```
❌ Error: Price validation failed: Price must be a valid number, got invalid_price
```

## Assumptions

1. **Testnet Only**: This application is configured to use Binance Futures Testnet by default. For production trading, modify the `base_url` in `client.py`.

2. **USDT Margin**: Only USDT-M (margin) trading pairs are supported (e.g., BTCUSDT, ETHUSDT).

3. **Environment Variables**: API credentials must be set via `BINANCE_API_KEY` and `BINANCE_API_SECRET` environment variables for security.

4. **GTC Orders**: Limit orders use "Good Till Cancel" (GTC) time in force by default.

5. **Synchronous Execution**: The application makes synchronous API calls. For high-frequency trading, consider implementing async operations.

6. **Single Symbol Format**: The application assumes standard Binance symbol format (e.g., BTCUSDT, ETHUSDT, BNBUSDT).

7. **No Portfolio Management**: This is a simple order placement tool. It doesn't track positions or provide portfolio management features.

## API Authentication

The application uses HMAC-SHA256 signatures for API authentication as required by Binance:

1. Requests include timestamp and recvWindow parameters
2. Signature is computed from query string using API secret
3. API key is included in request headers
4. All signed requests have a 5-second recvWindow

## Security Considerations

- **Never hardcode API credentials** in your code
- Use environment variables to store sensitive information
- Consider using a secrets manager in production
- Restrict API key permissions in Binance dashboard (trading only)
- Use testnet accounts for development and testing
- Keep your API secret safe; never share it

## Testing

To test the application:

1. Start with small quantities on testnet
2. Test each order type (MARKET, LIMIT, STOP_LIMIT)
3. Test error scenarios (invalid input, insufficient balance)
4. Check log files for detailed execution information

Example test sequence:
```bash
# Test market order
python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.001

# Test limit order
python cli.py -s ETHUSDT -S SELL -t LIMIT -q 0.01 -p 2000

# Test invalid input (should fail gracefully)
python cli.py -s BTCUSDT -S INVALID -t MARKET -q 0.01
```

## Log Files

Sample log files are provided in the `logs/` directory showcasing:

1. **Market Order Log**: Example of a successful market order placement
2. **Limit Order Log**: Example of a successful limit order placement

These demonstrate the expected log output and API interaction details.

## Troubleshooting

### "API credentials not found in environment variables"
- Ensure `BINANCE_API_KEY` and `BINANCE_API_SECRET` are set
- Check that environment variables are properly exported
- Restart your terminal/IDE after setting variables

### "Connection error" or timeout errors
- Verify internet connection
- Check if testnet is accessible (https://testnet.binancefuture.com)
- Check firewall/proxy settings
- Verify API key has futures trading enabled

### "Invalid API key" error
- Verify API credentials are correct
- Ensure API key is for Binance Futures Testnet, not spot trading
- Regenerate API credentials if necessary

### "Insufficient balance" error
- Deposit more USDT to your testnet account
- Reduced order quantity
- Testnet balances are sometimes reset

## Contributing

For improvements or bug reports, please submit issues or pull requests.

## License

This project is provided as-is for educational and testing purposes.

## Support

For issues specific to:
- **Binance API**: Visit [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- **Trading Bot**: Check the logs/ directory for detailed error information

## Version

Application Version: 1.0.0
Last Updated: March 2024
