import unittest
from typing import Dict, Any, Optional
from unittest.mock import Mock

from src.domain.port import AnkiConnectPort
from src.domain.query import Query

class MockAnkiConnect(AnkiConnectPort):
    """Mock implementation of AnkiConnectPort for testing."""
    
    def __init__(self, deck_response: Optional[Dict] = None, 
                 cards_response: Optional[Dict] = None,
                 find_response: Optional[Dict] = None):
        self.deck_response = deck_response or {"result": [], "error": None}
        self.cards_response = cards_response or {"result": [], "error": None}
        self.find_response = find_response or {"result": [], "error": None}
        
        # For tracking calls
        self.invoke_calls = []
    
    def invoke(self, action: str, **params) -> Dict[str, Any]:
        """Record the call and return mock response."""
        self.invoke_calls.append((action, params))
        
        if action == "deckNames":
            return self.deck_response
        elif action == "cardsInfo":
            return self.cards_response
        elif action == "findCards":
            return self.find_response
        return {"result": None, "error": "Unknown action"}
    
    def test_connection(self) -> Optional[str]:
        return "6"  # Mock version number

class TestQuery(unittest.TestCase):
    def test_get_deck_names_success(self):
        """Test successful retrieval of deck names."""
        mock_client = MockAnkiConnect(deck_response={
            "result": ["Deck1", "Deck1::SubDeck", "Deck2"],
            "error": None
        })
        query = Query(mock_client)
        
        result = query.get_deck_names()
        
        # Verify only parent decks are returned
        self.assertEqual(result, ["Deck1", "Deck2"])
        # Verify the correct API call was made
        self.assertEqual(mock_client.invoke_calls[0][0], "deckNames")
    
    def test_get_deck_names_error(self):
        """Test error handling in get_deck_names."""
        mock_client = MockAnkiConnect(deck_response={
            "result": None,
            "error": "Failed to get decks"
        })
        query = Query(mock_client)
        
        result = query.get_deck_names()
        
        self.assertIsNone(result)
    
    def test_get_card_info_success(self):
        """Test successful retrieval of card information."""
        mock_response = {
            "result": [
                {"id": 1, "fields": {"Front": {"value": "Question 1"}}},
                {"id": 2, "fields": {"Front": {"value": "Question 2"}}}
            ],
            "error": None
        }
        mock_client = MockAnkiConnect(cards_response=mock_response)
        query = Query(mock_client)
        
        result = query.get_card_info([1, 2])
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["id"], 1)
        # Verify the correct API call was made
        action, params = mock_client.invoke_calls[0]
        self.assertEqual(action, "cardsInfo")
        self.assertEqual(params["cards"], [1, 2])
    
    def test_get_card_info_error(self):
        """Test error handling in get_card_info."""
        mock_client = MockAnkiConnect(cards_response={
            "result": None,
            "error": "Failed to get card info"
        })
        query = Query(mock_client)
        
        result = query.get_card_info([1, 2])
        
        self.assertEqual(result, [])
    
    def test_find_cards_due_today_success(self):
        """Test successful finding of due cards."""
        mock_client = MockAnkiConnect(find_response={
            "result": [1, 2, 3],
            "error": None
        })
        query = Query(mock_client)
        
        result = query.find_cards_due_today("Test Deck")
        
        self.assertEqual(result, [1, 2, 3])
        # Verify the correct API call was made
        action, params = mock_client.invoke_calls[0]
        self.assertEqual(action, "findCards")
        self.assertEqual(params["query"], 'deck:"Test Deck" (is:due or is:new)')
    
    def test_find_cards_due_today_error(self):
        """Test error handling in find_cards_due_today."""
        mock_client = MockAnkiConnect(find_response={
            "result": None,
            "error": "Failed to find cards"
        })
        query = Query(mock_client)
        
        result = query.find_cards_due_today("Test Deck")
        
        self.assertEqual(result, []) 