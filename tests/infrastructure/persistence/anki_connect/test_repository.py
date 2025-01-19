"""Tests for the AnkiConnect repository implementation."""

import unittest
from unittest.mock import Mock
from src.infrastructure import AnkiConnectCardRepository, AnkiConnectQuery
from src.core.entities import DeckCards, TodayReview


class TestAnkiConnectCardRepository(unittest.TestCase):
    """Test cases for AnkiConnectCardRepository."""

    def setUp(self):
        """Set up test cases."""
        self.mock_query = Mock(spec=AnkiConnectQuery)
        self.repository = AnkiConnectCardRepository(self.mock_query)

    def test_get_decks_success(self):
        """Test getting deck names when query succeeds."""
        expected = ["Deck1", "Deck2"]
        self.mock_query.get_deck_names.return_value = expected
        
        result = self.repository.get_decks()
        
        self.assertEqual(result, expected)
        self.mock_query.get_deck_names.assert_called_once()

    def test_get_decks_error(self):
        """Test getting deck names when query fails."""
        self.mock_query.get_deck_names.return_value = None
        
        with self.assertRaises(RuntimeError):
            self.repository.get_decks()

    def test_get_due_cards_empty(self):
        """Test getting due cards when no cards are due."""
        self.mock_query.find_cards_due_today.return_value = []
        
        result = self.repository.get_due_cards()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.mock_query.find_cards_due_today.assert_called_once()
        self.mock_query.get_card_info.assert_not_called()

    def test_get_due_cards_error_finding_cards(self):
        """Test getting due cards when finding cards fails."""
        self.mock_query.find_cards_due_today.return_value = None
        
        with self.assertRaises(RuntimeError):
            self.repository.get_due_cards()

    def test_get_due_cards_error_getting_info(self):
        """Test getting due cards when getting card info fails."""
        self.mock_query.find_cards_due_today.return_value = [1, 2]
        self.mock_query.get_card_info.return_value = None
        
        with self.assertRaises(RuntimeError):
            self.repository.get_due_cards()

    def test_get_due_cards_success(self):
        """Test getting due cards when query succeeds."""
        self.mock_query.find_cards_due_today.return_value = [1, 2]
        self.mock_query.get_card_info.return_value = [
            {
                'deckName': 'Test Deck',
                'fields': {'Front': {'value': 'Question 1'}},
                'queue': 0,  # New card
                'type': 0
            },
            {
                'deckName': 'Test Deck',
                'fields': {'Front': {'value': 'Question 2'}},
                'queue': 2,  # Review card
                'type': 2
            }
        ]
        
        result = self.repository.get_due_cards()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 1)
        
        deck = result.decks[0]
        self.assertEqual(deck.deck_name, 'Test Deck')
        self.assertEqual(len(deck.new_cards), 1)
        self.assertEqual(len(deck.review_cards), 1)
        self.assertEqual(len(deck.learning_cards), 0)
        
        self.assertEqual(deck.new_cards[0], 'Question 1')
        self.assertEqual(deck.review_cards[0], 'Question 2') 