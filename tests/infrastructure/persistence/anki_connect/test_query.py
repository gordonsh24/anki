"""Tests for the AnkiConnect query implementation."""

import unittest
from unittest.mock import Mock
from src.infrastructure import AnkiConnectQuery


class TestAnkiConnectQuery(unittest.TestCase):
    """Test cases for AnkiConnectQuery."""

    def setUp(self):
        """Set up test cases."""
        self.mock_client = Mock()
        self.query = AnkiConnectQuery(self.mock_client)

    def test_get_deck_names_success(self):
        """Test getting deck names when request succeeds."""
        expected = ["Deck1", "Deck2"]
        self.mock_client.request.return_value = {"result": expected}
        
        result = self.query.get_deck_names()
        
        self.assertEqual(result, expected)
        self.mock_client.request.assert_called_once_with("deckNames")

    def test_get_deck_names_error(self):
        """Test getting deck names when request fails."""
        self.mock_client.request.return_value = None
        
        result = self.query.get_deck_names()
        
        self.assertIsNone(result)
        self.mock_client.request.assert_called_once_with("deckNames")

    def test_find_cards_due_today_success(self):
        """Test finding due cards when request succeeds."""
        expected = [1, 2, 3]
        self.mock_client.request.return_value = {"result": expected}
        
        result = self.query.find_cards_due_today()
        
        self.assertEqual(result, expected)
        self.mock_client.request.assert_called_once_with("findCards", {"query": "is:due"})

    def test_find_cards_due_today_error(self):
        """Test finding due cards when request fails."""
        self.mock_client.request.return_value = None
        
        result = self.query.find_cards_due_today()
        
        self.assertIsNone(result)
        self.mock_client.request.assert_called_once_with("findCards", {"query": "is:due"})

    def test_get_card_info_success(self):
        """Test getting card info when request succeeds."""
        card_ids = [1, 2]
        expected = [{"id": 1}, {"id": 2}]
        self.mock_client.request.return_value = {"result": expected}
        
        result = self.query.get_card_info(card_ids)
        
        self.assertEqual(result, expected)
        self.mock_client.request.assert_called_once_with("cardsInfo", {"cards": card_ids})

    def test_get_card_info_error(self):
        """Test getting card info when request fails."""
        card_ids = [1, 2]
        self.mock_client.request.return_value = None
        
        result = self.query.get_card_info(card_ids)
        
        self.assertIsNone(result)
        self.mock_client.request.assert_called_once_with("cardsInfo", {"cards": card_ids})

    def test_get_card_info_empty_list(self):
        """Test getting card info with empty list."""
        result = self.query.get_card_info([])
        
        self.assertEqual(result, []) 