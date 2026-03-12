"""Binance Futures client wrapper for API interactions."""

import logging
import requests
import hmac
import hashlib
import time
from urllib.parse import urlencode
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class BinanceFuturesClient:
    """
    Client for interacting with Binance Futures Testnet API.
    Handles authentication and API communication.
    """
    
    def __init__(self, api_key: str, api_secret: str, 
                 base_url: str = "https://testnet.binancefuture.com"):
        """
        Initialize Binance Futures client.
        
        Args:
            api_key: Binance Futures Testnet API key
            api_secret: Binance Futures Testnet API secret
            base_url: Base URL for the API (testnet by default)
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})
        
        logger.info(f"BinanceFuturesClient initialized with base URL: {base_url}")
    
    def _generate_signature(self, data: Dict[str, Any]) -> str:
        """
        Generate HMAC SHA256 signature for API request.
        
        Args:
            data: Request parameters
            
        Returns:
            Signature string
        """
        query_string = urlencode(data)
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _make_request(self, method: str, endpoint: str, params: Dict[str, Any] = None,
                     signed: bool = True) -> Dict[str, Any]:
        """
        Make an API request to Binance Futures.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Request parameters
            signed: Whether to sign the request
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.RequestException: If request fails
        """
        params = params or {}
        url = f"{self.base_url}{endpoint}"
        
        headers = {"X-MBX-APIKEY": self.api_key}
        
        try:
            if signed:
                params["timestamp"] = int(time.time() * 1000)
                params["recvWindow"] = 5000
                signature = self._generate_signature(params)
                params["signature"] = signature
            
            logger.debug(f"Making {method} request to {endpoint}")
            logger.debug(f"Parameters: {params}")
            
            if method.upper() == "GET":
                response = self.session.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, data=params, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            result = response.json()
            
            logger.debug(f"API Response: {result}")
            return result
            
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout: {endpoint}"
            logger.error(error_msg)
            raise requests.RequestException(error_msg)
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Connection error: {str(e)}"
            logger.error(error_msg)
            raise requests.RequestException(error_msg)
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {response.status_code}: {response.text}"
            logger.error(error_msg)
            raise requests.RequestException(error_msg)
        except ValueError as e:
            error_msg = f"Invalid JSON response: {str(e)}"
            logger.error(error_msg)
            raise requests.RequestException(error_msg)
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
        """
        Place an order on Binance Futures Testnet.
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Price (required for LIMIT orders)
            
        Returns:
            Order response from API
            
        Raises:
            requests.RequestException: If API request fails
            ValueError: If order parameters are invalid
        """
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity
        }
        
        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Cancel
        
        logger.info(f"Placing {order_type} order: {side} {quantity} {symbol} @ {price if price else 'market price'}")
        
        try:
            response = self._make_request("POST", endpoint, params, signed=True)
            logger.info(f"Order placed successfully: {response.get('orderId')}")
            return response
        except Exception as e:
            logger.error(f"Failed to place order: {str(e)}")
            raise
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.
        
        Returns:
            Account information from API
        """
        endpoint = "/fapi/v2/account"
        logger.debug("Fetching account information")
        return self._make_request("GET", endpoint, signed=True)
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get status of a specific order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID
            
        Returns:
            Order status from API
        """
        endpoint = "/fapi/v1/orders"
        params = {
            "symbol": symbol.upper(),
            "orderId": order_id
        }
        logger.debug(f"Fetching order status for {symbol} order {order_id}")
        return self._make_request("GET", endpoint, params, signed=True)
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Cancel an existing order.
        
        Args:
            symbol: Trading pair
            order_id: Order ID to cancel
            
        Returns:
            Canceled order response from API
        """
        endpoint = "/fapi/v1/order"
        params = {
            "symbol": symbol.upper(),
            "orderId": order_id
        }
        logger.info(f"Canceling order {order_id} for {symbol}")
        return self._make_request("DELETE", endpoint, params, signed=True)
