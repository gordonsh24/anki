"""Client implementation for AnkiConnect protocol."""

import json
import requests
from typing import Dict, Any, Optional
from .port import AnkiConnectPort


class AnkiConnectClient(AnkiConnectPort):
    """Client for communicating with Anki via AnkiConnect."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        """Initialize client with connection details.
        
        Args:
            host: Hostname where Anki is running
            port: Port number for AnkiConnect
        """
        self.url = f"http://{host}:{port}"

    def request(self, action: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a request to AnkiConnect.
        
        Args:
            action: The action to perform
            params: Parameters for the action
            
        Returns:
            Response from AnkiConnect if successful, None otherwise.
        """
        if params is None:
            params = {}

        request_data = {
            "action": action,
            "version": 6,
            "params": params
        }

        try:
            response = requests.post(self.url, json=request_data)
            return response.json()
        except (requests.RequestException, json.JSONDecodeError) as e:
            print(f"Error communicating with AnkiConnect: {e}")
            return None 