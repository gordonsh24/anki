import json
import requests
from ..core.ports import AnkiConnectPort
from typing import Dict, Any, Optional

class AnkiConnectClient(AnkiConnectPort):
    """Client for communicating with Anki via AnkiConnect."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.url = f"http://{host}:{port}"

    def request(self, action: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Send a request to AnkiConnect."""
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