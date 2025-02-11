"""Tests for AnkiConnectCardRepository."""

from unittest import TestCase
from unittest.mock import Mock, call
from src.core.entities import TodayReview, DeckCards, Card
from src.infrastructure.persistence.anki_connect import AnkiConnectCardRepository


class TestAnkiConnectCardRepository(TestCase):
    """Tests for AnkiConnectCardRepository."""

    def setUp(self):
        """Set up test dependencies."""
        self.mock_client = Mock()
        self.mock_mapper = Mock()
        self.repository = AnkiConnectCardRepository(self.mock_client, self.mock_mapper)

    def test_get_cards_empty_decks(self):
        """Test getting cards when no decks exist."""
        self.mock_client.get_deck_names.return_value = []

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_not_called()

    def test_get_cards_deck_with_no_cards(self):
        """Test getting cards when deck exists but has no cards."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = []

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_called_once_with('deck:"Test Deck" is:due')

    def test_get_cards_deck_with_failed_card_info(self):
        """Test getting cards when card info retrieval fails."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = []

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_called_once_with('deck:"Test Deck" is:due')

    def test_get_cards_deck_with_all_card_types(self):
        """Test getting cards when deck has all types of cards."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = [
            {"id": 1, "type": 0},
            {"id": 2, "type": 1},
            {"id": 3, "type": 2}
        ]
        self.mock_mapper.to_deck_cards.return_value = DeckCards(
            deck_name="Test Deck",
            new_cards=[Card(front="new")],
            learning_cards=[Card(front="learning")],
            review_cards=[Card(front="review")]
        )

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 1)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_called_once_with('deck:"Test Deck" is:due')

    def test_get_today_review_filters_subdecks(self):
        """Test that get_today_review filters sub-decks and shows cards under main decks."""
        # Setup
        self.mock_client.get_deck_names.return_value = [
            "Programming",
            "Programming::Python",
            "Programming::PHP",
            "Languages",
            "Languages::English"
        ]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = [
            {"id": 1, "deck": "Programming::Python"},
            {"id": 2, "deck": "Programming::PHP"},
            {"id": 3, "deck": "Languages::English"}
        ]
        
        # Set up mapper to return decks with cards
        programming_deck = DeckCards(
            deck_name="Programming",
            new_cards=[Card(front="Python basics")],
            learning_cards=[],
            review_cards=[]
        )
        languages_deck = DeckCards(
            deck_name="Languages",
            new_cards=[],
            learning_cards=[Card(front="English grammar")],
            review_cards=[]
        )
        self.mock_mapper.to_deck_cards.side_effect = [programming_deck, languages_deck]

        # Execute
        result = self.repository.get_today_review()

        # Verify
        self.assertGreater(len(result.decks), 0)
        # Verify we query for both main decks (order doesn't matter)
        expected_calls = [
            call('deck:"Programming" is:due'),
            call('deck:"Languages" is:due')
        ]
        actual_calls = self.mock_client.find_cards.call_args_list
        self.assertEqual(len(actual_calls), 2)
        self.assertCountEqual(expected_calls, actual_calls)
        # Verify the deck names in the result are main decks
        deck_names = [deck.deck_name for deck in result.decks]
        self.assertTrue(all("::" not in name for name in deck_names)) 
        self.assertTrue(all("::" not in name for name in deck_names)) 