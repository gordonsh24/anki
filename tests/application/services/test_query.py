"""Tests for the Query service."""

import unittest
from typing import Dict, Any, Optional

from src.core.ports import AnkiConnectPort
from src.application.services import Query

class MockAnkiConnect(AnkiConnectPort):
    """Mock implementation of AnkiConnectPort for testing."""
    
    def __init__(self):
        self.deck_response = None
        self.find_response = None
        self.cards_response = None
    
    def request(self, action: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """Mock request implementation that returns predefined responses."""
        if action == "deckNames":
            return self.deck_response
        elif action == "findCards":
            return self.find_response
        elif action == "cardsInfo":
            return self.cards_response
        return None

class TestQuery(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_client = MockAnkiConnect()
        self.query = Query(self.mock_client)
    
    def test_get_deck_names_success(self):
        """Test get_deck_names with successful response."""
        self.mock_client.deck_response = {
            "result": ["Deck1", "Deck2"],
            "error": None
        }
        
        result = self.query.get_deck_names()
        
        self.assertEqual(result, ["Deck1", "Deck2"])
    
    def test_get_deck_names_error(self):
        """Test get_deck_names with error response."""
        self.mock_client.deck_response = {
            "result": None,
            "error": "Failed to get decks"
        }
        
        result = self.query.get_deck_names()
        
        self.assertIsNone(result)
    
    def test_find_cards_due_today_success(self):
        """Test find_cards_due_today with successful response."""
        self.mock_client.find_response = {
            "result": [1, 2, 3],
            "error": None
        }
        
        result = self.query.find_cards_due_today("Test Deck")
        
        self.assertEqual(result, [1, 2, 3])
    
    def test_find_cards_due_today_error(self):
        """Test find_cards_due_today with error response."""
        self.mock_client.find_response = {
            "result": None,
            "error": "Failed to find cards"
        }
        
        result = self.query.find_cards_due_today("Test Deck")
        
        self.assertIsNone(result)
    
    def test_get_card_info_success(self):
        """Test get_card_info with successful response."""
        expected_cards = [
            {"id": 1, "question": "Q1"},
            {"id": 2, "question": "Q2"}
        ]
        self.mock_client.cards_response = {
            "result": expected_cards,
            "error": None
        }
        
        result = self.query.get_card_info([1, 2])
        
        self.assertEqual(result, expected_cards)
    
    def test_get_card_info_error(self):
        """Test get_card_info with error response."""
        self.mock_client.cards_response = {
            "result": None,
            "error": "Failed to get card info"
        }
        
        result = self.query.get_card_info([1, 2])
        
        self.assertIsNone(result) 