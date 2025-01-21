"""Tests for the AnkiConnectCardRepository."""

from unittest import TestCase
from unittest.mock import Mock

from src.infrastructure import AnkiConnectCardRepository, AnkiConnectClient
from src.infrastructure.persistence.anki_connect.mapper import AnkiCardMapper
from src.core.entities import TodayReview


class TestAnkiConnectCardRepository(TestCase):
    """Test cases for AnkiConnectCardRepository."""

    def setUp(self):
        """Set up test cases."""
        self.mock_client = Mock(spec=AnkiConnectClient)
        self.mock_mapper = Mock(spec=AnkiCardMapper)
        self.repository = AnkiConnectCardRepository(self.mock_client, self.mock_mapper)

    def test_get_cards_empty_decks(self):
        """Test getting cards when there are no decks."""
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
        self.mock_client.find_cards.assert_called_once_with("deck:Test Deck")
        self.mock_client.get_cards_info.assert_not_called()

    def test_get_cards_deck_with_failed_card_info(self):
        """Test getting cards when card info retrieval fails."""
        self.mock_client.get_deck_names.return_value = ["Test Deck"]
        self.mock_client.find_cards.return_value = [1, 2, 3]
        self.mock_client.get_cards_info.return_value = []

        result = self.repository.get_today_review()

        self.assertIsInstance(result, TodayReview)
        self.assertEqual(len(result.decks), 0)
        self.mock_client.get_deck_names.assert_called_once()
        self.mock_client.find_cards.assert_called_once_with("deck:Test Deck")
        self.mock_client.get_cards_info.assert_called_once_with([1, 2, 3])

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
        self.mock_client.find_cards.assert_called_once_with("deck:Test Deck")
        self.mock_client.get_cards_info.assert_called_once_with([1, 2, 3])
        self.mock_mapper.to_deck_cards.assert_called_once_with(
            "Test Deck",
            [{"id": 1, "type": 0}, {"id": 2, "type": 1}, {"id": 3, "type": 2}]
        ) 