"""Tests for the ConsolePresenter."""

from unittest.mock import patch, call
from src.core.entities import TodayReview, DeckCards
from src.infrastructure.presentation.console import ConsolePresenter


def test_present_no_cards():
    """Test presenting when there are no cards to review."""
    presenter = ConsolePresenter()
    review = TodayReview([])

    with patch('builtins.print') as mock_print:
        presenter.present(review)
        mock_print.assert_called_once_with("\nNo cards to review today!")


def test_present_single_new_card():
    """Test presenting a deck with one new card."""
    presenter = ConsolePresenter()
    deck = DeckCards("Test Deck", new_cards=["What is Python?"], learning_cards=[], review_cards=[])
    review = TodayReview([deck])

    with patch('builtins.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 1"),
            call("Test Deck:"),
            call("  New cards (1):"),
            call("    - What is Python?")
        ])


def test_present_single_learning_card():
    """Test presenting a deck with one learning card."""
    presenter = ConsolePresenter()
    deck = DeckCards("Test Deck", new_cards=[], learning_cards=["What is a decorator?"], review_cards=[])
    review = TodayReview([deck])

    with patch('builtins.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 1"),
            call("Test Deck:"),
            call("  Learning cards (1):"),
            call("    - What is a decorator?")
        ])


def test_present_single_review_card():
    """Test presenting a deck with one review card."""
    presenter = ConsolePresenter()
    deck = DeckCards("Test Deck", new_cards=[], learning_cards=[], review_cards=["What is dependency injection?"])
    review = TodayReview([deck])

    with patch('builtins.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 1"),
            call("Test Deck:"),
            call("  Review cards (1):"),
            call("    - What is dependency injection?")
        ])


def test_present_multiple_decks_with_mixed_cards():
    """Test presenting multiple decks with mixed card types."""
    presenter = ConsolePresenter()
    
    python_deck = DeckCards(
        "Python",
        new_cards=["What is a list comprehension?"],
        learning_cards=["How to use decorators?"],
        review_cards=["What is the GIL?"]
    )
    
    design_patterns_deck = DeckCards(
        "Design Patterns",
        new_cards=["What is the Factory pattern?"],
        learning_cards=["When to use the Observer pattern?"],
        review_cards=["Explain dependency injection."]
    )
    
    review = TodayReview([python_deck, design_patterns_deck])

    with patch('builtins.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 6"),
            call("Python:"),
            call("  New cards (1):"),
            call("    - What is a list comprehension?"),
            call("  Learning cards (1):"),
            call("    - How to use decorators?"),
            call("  Review cards (1):"),
            call("    - What is the GIL?"),
            call("Design Patterns:"),
            call("  New cards (1):"),
            call("    - What is the Factory pattern?"),
            call("  Learning cards (1):"),
            call("    - When to use the Observer pattern?"),
            call("  Review cards (1):"),
            call("    - Explain dependency injection.")
        ]) 