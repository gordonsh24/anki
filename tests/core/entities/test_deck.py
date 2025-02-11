import unittest
from src.core.entities import DeckCards, Card

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
            new_cards=[Card(front="card1"), Card(front="card2")],
            learning_cards=[Card(front="card3")],
            review_cards=[Card(front="card4"), Card(front="card5"), Card(front="card6")]
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

if __name__ == '__main__':
    unittest.main() 