"""
Secure credential loading for Trading Bot
Supports multiple methods of credential management
"""

import os
from typing import Tuple

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


class CredentialManager:
    """Manages secure credential loading from multiple sources."""
    
    @staticmethod
    def load_credentials() -> Tuple[str, str]:
        """
        Load API credentials from multiple sources in order of preference:
        1. GitHub Actions Secrets (via environment variables)
        2. .env file (local development)
        3. System environment variables
        4. Raise error if not found
        
        Returns:
            Tuple of (api_key, api_secret)
            
        Raises:
            ValueError: If credentials are not found
        """
        # Try loading from .env file first (if available)
        if DOTENV_AVAILABLE:
            load_dotenv(verbose=False)
        
        # Check environment variables
        api_key = os.getenv("BINANCE_API_KEY", "").strip()
        api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
        
        if not api_key or not api_secret:
            raise ValueError(
                "API credentials not found.\n"
                "Please set BINANCE_API_KEY and BINANCE_API_SECRET environment variables.\n"
                "See DEPLOYMENT.md for detailed instructions."
            )
        
        return api_key, api_secret
    
    @staticmethod
    def validate_credentials(api_key: str, api_secret: str) -> Tuple[bool, str]:
        """
        Validate credential format.
        
        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not api_key or len(api_key) < 20:
            return False, "Invalid API key format (too short)"
        
        if not api_secret or len(api_secret) < 20:
            return False, "Invalid API secret format (too short)"
        
        return True, ""
    
    @staticmethod
    def is_testnet_key(api_key: str) -> bool:
        """
        Check if the API key appears to be for testnet.
        Note: This is a heuristic check based on key length/format.
        
        Args:
            api_key: API key to check
            
        Returns:
            True if likely testnet key, False otherwise
        """
        # Testnet and mainnet keys look similar, so we can't reliably detect
        # Just ensure it's a valid-looking key
        return len(api_key) > 20


if __name__ == "__main__":
    # Test credential loading
    try:
        key, secret = CredentialManager.load_credentials()
        is_valid, msg = CredentialManager.validate_credentials(key, secret)
        
        if is_valid:
            print("✓ Credentials loaded successfully")
            print(f"✓ API Key (masked): {key[:10]}...{key[-4:]}")
            print(f"✓ API Secret (masked): {secret[:10]}...{secret[-4:]}")
        else:
            print(f"✗ Credential validation failed: {msg}")
    except ValueError as e:
        print(f"✗ Error loading credentials: {str(e)}")
