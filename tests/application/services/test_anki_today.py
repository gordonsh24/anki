"""Tests for the AnkiToday service."""

import unittest
from unittest.mock import Mock
from src.core.ports import CardRepository
from src.core.entities import DeckCards, TodayReview
from src.application.services import AnkiTodayService


class TestAnkiTodayService(unittest.TestCase):
    """Test cases for AnkiTodayService."""

    def setUp(self):
        """Set up test cases."""
        self.mock_repository = Mock(spec=CardRepository)
        self.service = AnkiTodayService(self.mock_repository)

    def test_get_cards_empty_decks(self):
        """Test getting cards when no decks have cards due."""
        expected = TodayReview([])
        self.mock_repository.get_due_cards.return_value = expected
        
        result = self.service.get_cards()
        
        self.assertEqual(result, expected)
        self.mock_repository.get_due_cards.assert_called_once()

    def test_get_cards_with_content(self):
        """Test getting cards when decks have cards due."""
        deck = DeckCards(
            deck_name="Test Deck",
            new_cards=["New Card 1"],
            learning_cards=["Learning Card 1"],
            review_cards=["Review Card 1"]
        )
        expected = TodayReview([deck])
        self.mock_repository.get_due_cards.return_value = expected
        
        result = self.service.get_cards()
        
        self.assertEqual(result, expected)
        self.mock_repository.get_due_cards.assert_called_once()

    def test_get_cards_deck_with_no_cards(self):
        """Test get_cards with a deck that has no cards due."""
        self.mock_repository.get_due_cards.return_value = TodayReview([])
        
        result = self.service.get_cards()
        
        self.assertEqual(result, TodayReview([]))
        self.mock_repository.get_due_cards.assert_called_once()
    
    def test_get_cards_deck_with_failed_card_info(self):
        """Test get_cards with a deck where getting card info fails."""
        self.mock_repository.get_due_cards.return_value = TodayReview([])
        
        result = self.service.get_cards()
        
        self.assertEqual(result, TodayReview([]))
        self.mock_repository.get_due_cards.assert_called_once()
    
    def test_get_cards_deck_with_all_card_types(self):
        """Test get_cards with a deck containing one card of each type."""
        deck = DeckCards(
            deck_name="Test Deck",
            new_cards=["New Question"],
            learning_cards=["Learning Question"],
            review_cards=["Review Question"]
        )
        self.mock_repository.get_due_cards.return_value = TodayReview([deck])
        
        result = self.service.get_cards()
        
        self.assertEqual(result, TodayReview([deck]))
        self.mock_repository.get_due_cards.assert_called_once() 