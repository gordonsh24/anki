import unittest
from src.domain.models import DeckCards, TodayReview

class TestDeckCards(unittest.TestCase):
    def test_total_cards_empty(self):
        """Test total_cards property with empty lists."""
        deck = DeckCards(
            deck_name="Test Deck",
            new_cards=[],
            learning_cards=[],
            review_cards=[]
        )
        self.assertEqual(deck.total_cards, 0)
    
    def test_total_cards_with_content(self):
        """Test total_cards property with some cards."""
        deck = DeckCards(
            deck_name="Test Deck",
            new_cards=["card1", "card2"],
            learning_cards=["card3"],
            review_cards=["card4", "card5", "card6"]
        )
        self.assertEqual(deck.total_cards, 6)
    
    def test_deck_name_stored(self):
        """Test that deck_name is properly stored."""
        deck_name = "Test Deck"
        deck = DeckCards(
            deck_name=deck_name,
            new_cards=[],
            learning_cards=[],
            review_cards=[]
        )
        self.assertEqual(deck.deck_name, deck_name)

class TestTodayReview(unittest.TestCase):
    def test_total_cards_empty(self):
        """Test total_cards property with no decks."""
        review = TodayReview(decks=[])
        self.assertEqual(review.total_cards, 0)
    
    def test_total_cards_single_deck(self):
        """Test total_cards property with a single deck."""
        deck = DeckCards(
            deck_name="Test Deck",
            new_cards=["card1"],
            learning_cards=["card2"],
            review_cards=["card3"]
        )
        review = TodayReview(decks=[deck])
        self.assertEqual(review.total_cards, 3)
    
    def test_total_cards_multiple_decks(self):
        """Test total_cards property with multiple decks."""
        deck1 = DeckCards(
            deck_name="Deck 1",
            new_cards=["card1"],
            learning_cards=[],
            review_cards=["card2"]
        )
        deck2 = DeckCards(
            deck_name="Deck 2",
            new_cards=[],
            learning_cards=["card3", "card4"],
            review_cards=["card5"]
        )
        review = TodayReview(decks=[deck1, deck2])
        self.assertEqual(review.total_cards, 5)

if __name__ == '__main__':
    unittest.main() 