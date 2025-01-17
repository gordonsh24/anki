import unittest
from typing import Dict, Any

from src.domain.models import TodayReview
from src.domain.query import Query
from src.domain.service import AnkiTodayService
from tests.domain.test_query import MockAnkiConnect

class TestAnkiTodayService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_client = MockAnkiConnect()
        self.query = Query(self.mock_client)
        self.service = AnkiTodayService(self.query)
    
    def test_get_cards_empty_decks(self):
        """Test get_cards with no decks available."""
        self.mock_client.deck_response = {
            "result": [],
            "error": None
        }
        
        result = self.service.get_cards()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.assertEqual(result.total_cards, 0)
    
    def test_get_cards_deck_with_no_cards(self):
        """Test get_cards with a deck that has no cards due."""
        self.mock_client.deck_response = {
            "result": ["Test Deck"],
            "error": None
        }
        self.mock_client.find_response = {
            "result": [],
            "error": None
        }
        
        result = self.service.get_cards()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)  # Deck should not be included if it has no cards
        self.assertEqual(result.total_cards, 0)
    
    def test_get_cards_deck_with_failed_card_info(self):
        """Test get_cards with a deck where getting card info fails."""
        self.mock_client.deck_response = {
            "result": ["Test Deck"],
            "error": None
        }
        # Mock finding some card IDs
        self.mock_client.find_response = {
            "result": [1, 2, 3],
            "error": None
        }
        # Mock failure to get card info
        self.mock_client.cards_response = {
            "result": None,
            "error": "Failed to get card info"
        }
        
        result = self.service.get_cards()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)  # Deck should not be included if we can't get card info
        self.assertEqual(result.total_cards, 0)
    
    def test_get_cards_deck_with_all_card_types(self):
        """Test get_cards with a deck containing one card of each type."""
        # Mock deck response
        self.mock_client.deck_response = {
            "result": ["Test Deck"],
            "error": None
        }
        # Mock finding card IDs
        self.mock_client.find_response = {
            "result": [1, 2, 3],
            "error": None
        }
        # Mock card info with one card of each type
        self.mock_client.cards_response = {
            "result": [
                {
                    "id": 1,
                    "queue": 0,  # New card
                    "type": 0,
                    "question": "New Question",
                    "fields": {
                        "Front": {"value": "New Question", "order": 0},
                        "Back": {"value": "New Answer", "order": 1}
                    }
                },
                {
                    "id": 2,
                    "queue": 1,  # Learning card
                    "type": 1,
                    "question": "Learning Question",
                    "fields": {
                        "Front": {"value": "Learning Question", "order": 0},
                        "Back": {"value": "Learning Answer", "order": 1}
                    }
                },
                {
                    "id": 3,
                    "queue": 2,  # Review card
                    "type": 2,
                    "question": "Review Question",
                    "fields": {
                        "Front": {"value": "Review Question", "order": 0},
                        "Back": {"value": "Review Answer", "order": 1}
                    }
                }
            ],
            "error": None
        }
        
        result = self.service.get_cards()
        
        # Verify overall structure
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 1)
        self.assertEqual(result.total_cards, 3)
        
        # Verify deck contents
        deck = result.decks[0]
        self.assertEqual(deck.deck_name, "Test Deck")
        
        # Verify new cards
        self.assertEqual(len(deck.new_cards), 1)
        self.assertEqual(deck.new_cards[0], "New Question")
        
        # Verify learning cards
        self.assertEqual(len(deck.learning_cards), 1)
        self.assertEqual(deck.learning_cards[0], "Learning Question")
        
        # Verify review cards
        self.assertEqual(len(deck.review_cards), 1)
        self.assertEqual(deck.review_cards[0], "Review Question") 