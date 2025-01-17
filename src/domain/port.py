from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AnkiConnectPort(ABC):
    """Port (interface) for communicating with Anki."""
    
    @abstractmethod
    def invoke(self, action: str, **params) -> Dict[str, Any]:
        """
        Make a request to the Anki Connect API.
        
        Args:
            action: The API action to perform
            **params: Additional parameters for the action
            
        Returns:
            Dict containing the response with 'result' and 'error' keys
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> Optional[str]:
        """
        Test the connection to Anki and return the version if successful.
        
        Returns:
            Version string if connected, None if connection failed
        """
        pass 