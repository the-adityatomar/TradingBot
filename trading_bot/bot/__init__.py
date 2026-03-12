"""Trading Bot Package"""

__version__ = "1.0.0"
__author__ = "Trading Bot Developer"

from .client import BinanceFuturesClient
from .orders import OrderManager
from .validators import OrderValidator

__all__ = ["BinanceFuturesClient", "OrderManager", "OrderValidator"]
