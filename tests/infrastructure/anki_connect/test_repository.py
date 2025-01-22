"""Tests for AnkiConnectCardRepository."""

from unittest import TestCase
from unittest.mock import Mock, call

from src.infrastructure import AnkiConnectCardRepository
from src.core.entities import TodayReview, DeckCards


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
        self.mock_client.find_cards.assert_called_once_with("deck:Test Deck*")

    def test_get_cards_deck_with_failed_card_info(self):
        """Test getting cards when card info retrieval fails."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = []

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_called_once_with("deck:Test Deck*")

    def test_get_cards_deck_with_all_card_types(self):
        """Test getting cards when deck has all types of cards."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = [
            {"id": 1, "type": 0},
            {"id": 2, "type": 1},
            {"id": 3, "type": 2}
        ]
        self.mock_mapper.to_deck_cards.return_value = Mock(total_cards=3)

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 1)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_called_once_with("deck:Test Deck*")

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
        
        self.mock_mapper.to_deck_cards.return_value = DeckCards(
            deck_name="Programming",
            new_cards=["card1"],
            learning_cards=["card2"],
            review_cards=["card3"]
        )

        # Execute
        result = self.repository.get_today_review()

        # Verify
        self.assertGreater(len(result.decks), 0)
        # Verify we query for both main decks (order doesn't matter)
        expected_calls = [
            call("deck:Programming*"),
            call("deck:Languages*")
        ]
        actual_calls = self.mock_client.find_cards.call_args_list
        self.assertEqual(len(actual_calls), 2)
        self.assertCountEqual(expected_calls, actual_calls)
        # Verify the deck names in the result are main decks
        deck_names = [deck.deck_name for deck in result.decks]
        self.assertTrue(all("::" not in name for name in deck_names)) 