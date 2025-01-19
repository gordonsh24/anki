"""Client for interacting with the AnkiConnect API."""

import json
import requests
from typing import List, Dict, Any, Optional


class AnkiConnectClient:
    """Client for making requests to the AnkiConnect API."""

    def __init__(self, base_url: str = "http://localhost:8765"):
        """Initialize the client.
        
        Args:
            base_url: Base URL for the AnkiConnect API
        """
        self.base_url = base_url

    def _make_request(self, action: str, params: Dict[str, Any] = None) -> Optional[Any]:
        """Make a request to the AnkiConnect API.
        
        Args:
            action: The action to perform
            params: Parameters for the action
            
        Returns:
            Response data if successful, None otherwise
            
        Raises:
            RuntimeError: If there's an error communicating with Anki
        """
        if params is None:
            params = {}

        request_data = {
            "action": action,
            "version": 6,
            "params": params
        }

        try:
            response = requests.post(self.base_url, json=request_data)
            response.raise_for_status()
            result = response.json()
            
            if result.get("error") is not None:
                raise RuntimeError(f"AnkiConnect error: {result['error']}")
                
            return result.get("result")
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to communicate with Anki: {str(e)}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid response from Anki: {str(e)}")

    def get_deck_names(self) -> List[str]:
        """Get all available deck names.
        
        Returns:
            List of deck names
            
        Raises:
            RuntimeError: If there's an error communicating with Anki
        """
        return self._make_request("deckNames")

    def find_cards(self, query: str) -> List[int]:
        """Find cards matching a query.
        
        Args:
            query: The search query
            
        Returns:
            List of card IDs
            
        Raises:
            RuntimeError: If there's an error communicating with Anki
        """
        return self._make_request("findCards", {"query": query})

    def get_cards_info(self, card_ids: List[int]) -> List[Dict[str, Any]]:
        """Get detailed information about cards.
        
        Args:
            card_ids: List of card IDs to get info for
            
        Returns:
            List of card information dictionaries
            
        Raises:
            RuntimeError: If there's an error communicating with Anki
        """
        return self._make_request("cardsInfo", {"cards": card_ids}) 