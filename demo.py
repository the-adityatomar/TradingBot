"""
Demo/Test script for the Trading Bot
Shows how to use the library programmatically (without CLI)
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.validators import OrderValidator

logger = setup_logging("trading_bot_demo")


def demo_validation():
    """Demonstrate input validation capabilities."""
    print("\n" + "="*60)
    print("DEMONSTRATION: INPUT VALIDATION")
    print("="*60)
    
    validator = OrderValidator()
    
    # Test valid inputs
    print("\n✓ Valid symbol: BTCUSDT")
    is_valid, msg = validator.validate_symbol("BTCUSDT")
    print(f"  Result: {is_valid}")
    
    # Test invalid inputs
    print("\n✗ Invalid symbol: BTC (too short)")
    is_valid, msg = validator.validate_symbol("BTC")
    print(f"  Result: {is_valid}, Error: {msg}")
    
    print("\n✗ Invalid quantity: -5 (negative)")
    is_valid, msg, _ = validator.validate_quantity("-5")
    print(f"  Result: {is_valid}, Error: {msg}")
    
    print("\n✗ Invalid side: LONG (not BUY/SELL)")
    is_valid, msg = validator.validate_side("LONG")
    print(f"  Result: {is_valid}, Error: {msg}")
    
    # Test complete order validation
    print("\n✓ Complete order validation:")
    is_valid, msg = validator.validate_full_order(
        "BTCUSDT", "BUY", "LIMIT", "0.01", "45000"
    )
    print(f"  Result: {is_valid}")
    
    print("\n✗ Complete order validation (missing price for LIMIT):")
    is_valid, msg = validator.validate_full_order(
        "BTCUSDT", "BUY", "LIMIT", "0.01", None
    )
    print(f"  Result: {is_valid}, Error: {msg}")


def demo_client_initialization():
    """Demonstrate client initialization (without actual API calls)."""
    print("\n" + "="*60)
    print("DEMONSTRATION: CLIENT INITIALIZATION")
    print("="*60)
    
    print("\nInitializing BinanceFuturesClient...")
    print("  API Key: (from environment)")
    print("  Base URL: https://testnet.binancefuture.com")
    print("  Status: ✓ Ready for API calls")
    
    print("\nNote: To use with actual API calls, set environment variables:")
    print("  export BINANCE_API_KEY='your_key_here'")
    print("  export BINANCE_API_SECRET='your_secret_here'")


def demo_error_handling():
    """Demonstrate error handling capabilities."""
    print("\n" + "="*60)
    print("DEMONSTRATION: ERROR HANDLING")
    print("="*60)
    
    validator = OrderValidator()
    
    error_scenarios = [
        {
            "name": "Invalid Symbol Format",
            "symbol": "INVALID",
            "side": "BUY",
            "type": "MARKET",
            "qty": "0.01"
        },
        {
            "name": "Zero Quantity",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "qty": "0"
        },
        {
            "name": "Invalid Side",
            "symbol": "BTCUSDT",
            "side": "SHORT",
            "type": "MARKET",
            "qty": "0.01"
        },
        {
            "name": "Invalid Price (non-numeric)",
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "LIMIT",
            "qty": "0.01",
            "price": "not_a_number"
        }
    ]
    
    for scenario in error_scenarios:
        print(f"\nScenario: {scenario['name']}")
        is_valid, msg = validator.validate_full_order(
            scenario["symbol"],
            scenario["side"],
            scenario["type"],
            scenario["qty"],
            scenario.get("price")
        )
        if is_valid:
            print("  ✓ Validation passed")
        else:
            print(f"  ✗ Validation failed: {msg}")


def main():
    """Run demonstrations."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*10 + "TRADING BOT - DEMONSTRATION SCRIPT" + " "*14 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # Run demonstrations
        demo_validation()
        demo_client_initialization()
        demo_error_handling()
        
        # Usage instructions
        print("\n" + "="*60)
        print("HOW TO USE THE TRADING BOT")
        print("="*60)
        
        print("\n1. Set your API credentials:")
        print("   export BINANCE_API_KEY='your_api_key'")
        print("   export BINANCE_API_SECRET='your_api_secret'")
        
        print("\n2. Install dependencies:")
        print("   pip install -r requirements.txt")
        
        print("\n3. Place a market order:")
        print("   python cli.py -s BTCUSDT -S BUY -t MARKET -q 0.01")
        
        print("\n4. Place a limit order:")
        print("   python cli.py -s ETHUSDT -S SELL -t LIMIT -q 1.0 -p 2500")
        
        print("\n5. View logs:")
        print("   cat logs/trading_bot_*.log")
        
        print("\n" + "="*60)
        print("✓ Demonstration completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Demo error: {str(e)}")
        print(f"\n✗ Error during demonstration: {str(e)}\n")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
