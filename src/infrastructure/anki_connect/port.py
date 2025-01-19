"""Port interface for AnkiConnect protocol."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class AnkiConnectPort(ABC):
    """Interface for communicating with Anki via AnkiConnect protocol."""

    @abstractmethod
    def request(self, action: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a request to AnkiConnect.
        
        Args:
            action: The action to perform
            params: Parameters for the action
            
        Returns:
            Response from AnkiConnect if successful, None otherwise.
        """
        pass 