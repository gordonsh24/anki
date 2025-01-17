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