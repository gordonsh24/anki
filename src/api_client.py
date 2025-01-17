import json
import requests
from typing import Any, Dict, Optional

class ApiClient:
    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
    
    def invoke(self, action: str, **params) -> Dict[str, Any]:
        """
        Make a request to the Anki Connect API.
        
        Args:
            action: The API action to perform
            **params: Additional parameters for the action
            
        Returns:
            Dict containing the response with 'result' and 'error' keys
        """
        request_data = {
            "action": action,
            "version": 6,
            "params": params
        }
        response = requests.post(self.base_url, json=request_data)
        return response.json()
    
    def test_connection(self) -> Optional[str]:
        """
        Test the connection to Anki and return the version if successful.
        
        Returns:
            Version string if connected, None if connection failed
        """
        try:
            version = self.invoke('version')
            if version.get('error'):
                return None
            return version['result']
        except requests.exceptions.ConnectionError:
            return None 