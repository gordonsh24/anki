import unittest
from src.core.entities import DeckCards, TodayReview

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