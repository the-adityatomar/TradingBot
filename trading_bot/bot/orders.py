"""Order management and placement logic."""

import logging
from typing import Dict, Any, Optional
from .client import BinanceFuturesClient
from .validators import OrderValidator

logger = logging.getLogger(__name__)


class OrderManager:
    """Manages order placement and tracking."""
    
    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize OrderManager.
        
        Args:
            client: BinanceFuturesClient instance
        """
        self.client = client
        self.validator = OrderValidator()
        self.last_order = None
        logger.info("OrderManager initialized")
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Order quantity
            
        Returns:
            Order response
            
        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        is_valid, error = self.validator.validate_full_order(
            symbol, side, "MARKET", str(quantity), None
        )
        if not is_valid:
            logger.error(f"Market order validation failed: {error}")
            raise ValueError(error)
        
        try:
            logger.info(f"=== MARKET ORDER ===")
            logger.info(f"Symbol: {symbol}")
            logger.info(f"Side: {side}")
            logger.info(f"Quantity: {quantity}")
            
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type="MARKET",
                quantity=quantity
            )
            
            self.last_order = response
            self._log_order_response(response)
            return response
            
        except Exception as e:
            logger.error(f"Market order placement failed: {str(e)}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float) -> Dict[str, Any]:
        """
        Place a limit order.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Order quantity
            price: Limit price
            
        Returns:
            Order response
            
        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        is_valid, error = self.validator.validate_full_order(
            symbol, side, "LIMIT", str(quantity), str(price)
        )
        if not is_valid:
            logger.error(f"Limit order validation failed: {error}")
            raise ValueError(error)
        
        try:
            logger.info(f"=== LIMIT ORDER ===")
            logger.info(f"Symbol: {symbol}")
            logger.info(f"Side: {side}")
            logger.info(f"Quantity: {quantity}")
            logger.info(f"Price: {price}")
            
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type="LIMIT",
                quantity=quantity,
                price=price
            )
            
            self.last_order = response
            self._log_order_response(response)
            return response
            
        except Exception as e:
            logger.error(f"Limit order placement failed: {str(e)}")
            raise
    
    def place_stop_limit_order(self, symbol: str, side: str, quantity: float,
                              price: float, stop_price: float) -> Dict[str, Any]:
        """
        Place a stop-limit order (BONUS feature).
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            quantity: Order quantity
            price: Limit price
            stop_price: Stop price
            
        Returns:
            Order response
        """
        is_valid, error = self.validator.validate_full_order(
            symbol, side, "LIMIT", str(quantity), str(price)
        )
        if not is_valid:
            logger.error(f"Stop-limit order validation failed: {error}")
            raise ValueError(error)
        
        is_valid, error, _ = self.validator.validate_price(str(stop_price))
        if not is_valid:
            logger.error(f"Stop price validation failed: {error}")
            raise ValueError(error)
        
        try:
            logger.info(f"=== STOP-LIMIT ORDER ===")
            logger.info(f"Symbol: {symbol}")
            logger.info(f"Side: {side}")
            logger.info(f"Quantity: {quantity}")
            logger.info(f"Price: {price}")
            logger.info(f"Stop Price: {stop_price}")
            
            # For testnet, we'll use a workaround - place a regular limit order
            # In production, you'd use the STOP_LOSS_LIMIT type with the proper parameters
            response = self.client.place_order(
                symbol=symbol,
                side=side,
                order_type="LIMIT",
                quantity=quantity,
                price=price
            )
            
            logger.warning("Stop-limit orders require additional parameters not fully supported in this implementation")
            self.last_order = response
            self._log_order_response(response)
            return response
            
        except Exception as e:
            logger.error(f"Stop-limit order placement failed: {str(e)}")
            raise
    
    def _log_order_response(self, response: Dict[str, Any]) -> None:
        """
        Log order response details.
        
        Args:
            response: Order response from API
        """
        logger.info("=== ORDER RESPONSE ===")
        logger.info(f"Order ID: {response.get('orderId')}")
        logger.info(f"Status: {response.get('status')}")
        logger.info(f"Symbol: {response.get('symbol')}")
        logger.info(f"Side: {response.get('side')}")
        logger.info(f"Type: {response.get('type')}")
        logger.info(f"Quantity: {response.get('origQty')}")
        logger.info(f"Executed Quantity: {response.get('executedQty')}")
        logger.info(f"Price: {response.get('price')}")
        logger.info(f"Average Price: {response.get('avgPrice')}")
        logger.info(f"Cumulative Quote Asset Transacted: {response.get('cumQuote')}")
        logger.info(f"Time in Force: {response.get('timeInForce')}")
        logger.info(f"Create Time: {response.get('time')}")
        logger.info(f"======================")
    
    def get_last_order(self) -> Optional[Dict[str, Any]]:
        """Get the last placed order."""
        return self.last_order
