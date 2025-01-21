"""Tests for the AnkiConnect repository implementation."""

from unittest import TestCase
from unittest.mock import Mock
from src.infrastructure import AnkiConnectCardRepository, AnkiConnectClient
from src.core.entities import TodayReview


class TestAnkiConnectCardRepository(TestCase):
    """Test cases for AnkiConnectCardRepository."""

    def setUp(self):
        """Set up test cases."""
        self.mock_client = Mock(spec=AnkiConnectClient)
        self.repository = AnkiConnectCardRepository(self.mock_client)

    def test_get_cards_empty_decks(self):
        """Test getting cards when there are no decks."""
        self.mock_client.get_deck_names.return_value = []
        
        result = self.repository.get_today_review()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.assertEqual(result.total_cards, 0)

    def test_get_cards_deck_with_no_cards(self):
        """Test getting cards when deck exists but has no cards."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = []
        
        result = self.repository.get_today_review()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.assertEqual(result.total_cards, 0)

    def test_get_cards_deck_with_failed_card_info(self):
        """Test getting cards when card info request fails."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = []
        
        result = self.repository.get_today_review()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.assertEqual(result.total_cards, 0)

    def test_get_cards_deck_with_all_card_types(self):
        """Test getting cards with one of each type."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = [
            {
                'deckName': 'Test Deck',
                'queue': 0,  # New card
                'fields': {'Front': {'value': 'New Card'}}
            },
            {
                'deckName': 'Test Deck',
                'queue': 1,  # Learning card
                'fields': {'Front': {'value': 'Learning Card'}}
            },
            {
                'deckName': 'Test Deck',
                'queue': 2,  # Review card
                'fields': {'Front': {'value': 'Review Card'}}
            }
        ]
        
        result = self.repository.get_today_review()
        
        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 1)
        self.assertEqual(result.total_cards, 3)
        
        deck = result.decks[0]
        self.assertEqual(deck.deck_name, "Test Deck")
        self.assertEqual(len(deck.new_cards), 1)
        self.assertEqual(len(deck.learning_cards), 1)
        self.assertEqual(len(deck.review_cards), 1)
        self.assertEqual(deck.new_cards[0], "New Card")
        self.assertEqual(deck.learning_cards[0], "Learning Card")
        self.assertEqual(deck.review_cards[0], "Review Card") 