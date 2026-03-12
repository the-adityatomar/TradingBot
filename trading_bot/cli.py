"""Command-line interface for the trading bot."""

import sys
import argparse
import os
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import OrderValidator

logger = setup_logging("trading_bot")


def get_api_credentials() -> tuple:
    """
    Get API credentials from environment variables.
    
    Returns:
        Tuple of (api_key, api_secret)
        
    Raises:
        ValueError: If credentials are not set
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("API credentials not found in environment variables")
        logger.error("Please set BINANCE_API_KEY and BINANCE_API_SECRET")
        raise ValueError("Missing API credentials")
    
    return api_key, api_secret


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure argument parser.
    
    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Binance Futures Trading Bot (Testnet)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  
  # Place a limit order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 1.0 --price 2000
  
  # Place a stop-limit order
  python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.01 --price 40000 --stop-price 39000
        """
    )
    
    parser.add_argument(
        "-s", "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)"
    )
    
    parser.add_argument(
        "-S", "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL"
    )
    
    parser.add_argument(
        "-t", "--type",
        required=True,
        choices=["MARKET", "LIMIT", "STOP_LIMIT"],
        help="Order type: MARKET, LIMIT, or STOP_LIMIT"
    )
    
    parser.add_argument(
        "-q", "--quantity",
        required=True,
        help="Order quantity (as a decimal number)"
    )
    
    parser.add_argument(
        "-p", "--price",
        help="Order price (required for LIMIT and STOP_LIMIT orders)"
    )
    
    parser.add_argument(
        "--stop-price",
        help="Stop price (required for STOP_LIMIT orders)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser


def validate_args(args: argparse.Namespace) -> tuple:
    """
    Validate command-line arguments.
    
    Args:
        args: Parsed arguments
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    validator = OrderValidator()
    
    # Validate symbol
    is_valid, error = validator.validate_symbol(args.symbol)
    if not is_valid:
        return False, f"Symbol validation failed: {error}"
    
    # Validate side
    is_valid, error = validator.validate_side(args.side)
    if not is_valid:
        return False, f"Side validation failed: {error}"
    
    # Validate quantity
    is_valid, error, _ = validator.validate_quantity(args.quantity)
    if not is_valid:
        return False, f"Quantity validation failed: {error}"
    
    # Type-specific validation
    if args.type == "LIMIT":
        if not args.price:
            return False, "Price is required for LIMIT orders"
        is_valid, error, _ = validator.validate_price(args.price)
        if not is_valid:
            return False, f"Price validation failed: {error}"
    
    elif args.type == "STOP_LIMIT":
        if not args.price:
            return False, "Price is required for STOP_LIMIT orders"
        if not args.stop_price:
            return False, "Stop price is required for STOP_LIMIT orders"
        
        is_valid, error, _ = validator.validate_price(args.price)
        if not is_valid:
            return False, f"Price validation failed: {error}"
        
        is_valid, error, _ = validator.validate_price(args.stop_price)
        if not is_valid:
            return False, f"Stop price validation failed: {error}"
    
    return True, ""


def print_summary(args: argparse.Namespace) -> None:
    """
    Print order summary before placing.
    
    Args:
        args: Parsed arguments
    """
    print("\n" + "="*60)
    print("ORDER REQUEST SUMMARY")
    print("="*60)
    print(f"Symbol:       {args.symbol.upper()}")
    print(f"Side:         {args.side.upper()}")
    print(f"Type:         {args.type.upper()}")
    print(f"Quantity:     {args.quantity}")
    if args.price:
        print(f"Price:        {args.price}")
    if args.stop_price:
        print(f"Stop Price:   {args.stop_price}")
    print("="*60 + "\n")


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Validate arguments
        is_valid, error = validate_args(args)
        if not is_valid:
            logger.error(f"Argument validation failed: {error}")
            print(f"\n❌ Error: {error}\n")
            return 1
        
        # Get API credentials
        api_key, api_secret = get_api_credentials()
        
        # Print order summary
        print_summary(args)
        
        # Initialize client and manager
        logger.info("Initializing Binance Futures client...")
        client = BinanceFuturesClient(api_key, api_secret)
        manager = OrderManager(client)
        
        # Convert quantity to float
        quantity = float(args.quantity)
        
        # Place order based on type
        if args.type == "MARKET":
            logger.info(f"Placing MARKET order: {args.side} {quantity} {args.symbol}")
            response = manager.place_market_order(args.symbol, args.side, quantity)
        
        elif args.type == "LIMIT":
            price = float(args.price)
            logger.info(f"Placing LIMIT order: {args.side} {quantity} {args.symbol} @ {price}")
            response = manager.place_limit_order(args.symbol, args.side, quantity, price)
        
        elif args.type == "STOP_LIMIT":
            price = float(args.price)
            stop_price = float(args.stop_price)
            logger.info(f"Placing STOP_LIMIT order: {args.side} {quantity} {args.symbol}")
            response = manager.place_stop_limit_order(args.symbol, args.side, quantity, price, stop_price)
        
        # Print response
        print("\n" + "="*60)
        print("ORDER RESPONSE DETAILS")
        print("="*60)
        print(f"✓ ORDER PLACED SUCCESSFULLY")
        print(f"  Order ID:              {response.get('orderId')}")
        print(f"  Status:                {response.get('status')}")
        print(f"  Symbol:                {response.get('symbol')}")
        print(f"  Side:                  {response.get('side')}")
        print(f"  Type:                  {response.get('type')}")
        print(f"  Quantity:              {response.get('origQty')}")
        print(f"  Executed Quantity:     {response.get('executedQty')}")
        print(f"  Price:                 {response.get('price')}")
        print(f"  Average Price:         {response.get('avgPrice')}")
        print(f"  Time in Force:         {response.get('timeInForce')}")
        print("="*60 + "\n")
        
        logger.info("Order placement completed successfully")
        return 0
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        print(f"\n❌ Validation Error: {str(e)}\n")
        return 1
    
    except Exception as e:
        logger.error(f"Error placing order: {str(e)}")
        print(f"\n❌ Error: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
