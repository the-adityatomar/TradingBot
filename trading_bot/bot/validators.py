"""Input validation for trading parameters."""

import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class OrderValidator:
    """Validates trading order parameters."""
    
    VALID_SIDES = {"BUY", "SELL"}
    VALID_ORDER_TYPES = {"MARKET", "LIMIT"}
    MIN_QUANTITY = 0.001
    MIN_PRICE = 0.00000001
    
    @classmethod
    def validate_symbol(cls, symbol: str) -> Tuple[bool, str]:
        """
        Validate trading symbol.
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not symbol:
            return False, "Symbol cannot be empty"
        
        symbol = symbol.upper()
        if len(symbol) < 6:
            return False, "Symbol too short (minimum 6 characters like BTCUSDT)"
        
        if not symbol.endswith("USDT"):
            return False, "Currently only USDT trading pairs are supported"
        
        return True, ""
    
    @classmethod
    def validate_side(cls, side: str) -> Tuple[bool, str]:
        """
        Validate order side.
        
        Args:
            side: BUY or SELL
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not side:
            return False, "Side cannot be empty"
        
        side = side.upper()
        if side not in cls.VALID_SIDES:
            return False, f"Side must be one of {cls.VALID_SIDES}, got {side}"
        
        return True, ""
    
    @classmethod
    def validate_order_type(cls, order_type: str) -> Tuple[bool, str]:
        """
        Validate order type.
        
        Args:
            order_type: MARKET or LIMIT
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not order_type:
            return False, "Order type cannot be empty"
        
        order_type = order_type.upper()
        if order_type not in cls.VALID_ORDER_TYPES:
            return False, f"Order type must be one of {cls.VALID_ORDER_TYPES}, got {order_type}"
        
        return True, ""
    
    @classmethod
    def validate_quantity(cls, quantity: str) -> Tuple[bool, str, float]:
        """
        Validate order quantity.
        
        Args:
            quantity: String representation of quantity
            
        Returns:
            Tuple of (is_valid, error_message, parsed_quantity)
        """
        try:
            qty = float(quantity)
        except ValueError:
            return False, f"Quantity must be a valid number, got {quantity}", 0.0
        
        if qty <= 0:
            return False, f"Quantity must be positive, got {qty}", 0.0
        
        if qty < cls.MIN_QUANTITY:
            return False, f"Quantity must be at least {cls.MIN_QUANTITY}, got {qty}", 0.0
        
        return True, "", qty
    
    @classmethod
    def validate_price(cls, price: str) -> Tuple[bool, str, float]:
        """
        Validate limit order price.
        
        Args:
            price: String representation of price
            
        Returns:
            Tuple of (is_valid, error_message, parsed_price)
        """
        try:
            p = float(price)
        except ValueError:
            return False, f"Price must be a valid number, got {price}", 0.0
        
        if p <= 0:
            return False, f"Price must be positive, got {p}", 0.0
        
        if p < cls.MIN_PRICE:
            return False, f"Price must be at least {cls.MIN_PRICE}, got {p}", 0.0
        
        return True, "", p
    
    @classmethod
    def validate_full_order(cls, symbol: str, side: str, order_type: str, 
                           quantity: str, price: str = None) -> Tuple[bool, str]:
        """
        Validate a complete order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate symbol
        is_valid, error = cls.validate_symbol(symbol)
        if not is_valid:
            return False, f"Symbol validation failed: {error}"
        
        # Validate side
        is_valid, error = cls.validate_side(side)
        if not is_valid:
            return False, f"Side validation failed: {error}"
        
        # Validate order type
        is_valid, error = cls.validate_order_type(order_type)
        if not is_valid:
            return False, f"Order type validation failed: {error}"
        
        # Validate quantity
        is_valid, error, _ = cls.validate_quantity(quantity)
        if not is_valid:
            return False, f"Quantity validation failed: {error}"
        
        # Validate price for LIMIT orders
        if order_type.upper() == "LIMIT":
            if not price:
                return False, "Price is required for LIMIT orders"
            is_valid, error, _ = cls.validate_price(price)
            if not is_valid:
                return False, f"Price validation failed: {error}"
        
        return True, ""
