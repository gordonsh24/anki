"""Port interface for Anki Connect integration."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class AnkiConnectPort(ABC):
    """Interface for communicating with Anki via AnkiConnect."""

    @abstractmethod
    def request(self, action: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a request to AnkiConnect."""
        pass 