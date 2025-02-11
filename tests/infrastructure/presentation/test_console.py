"""Tests for the ConsolePresenter."""

from unittest.mock import patch, call
from src.core.entities import TodayReview, DeckCards, Card
from src.infrastructure.presentation.console import ConsolePresenter


def test_present_no_cards():
    """Test presenting when there are no cards to review."""
    presenter = ConsolePresenter()
    review = TodayReview([])

    with patch('src.infrastructure.presentation.console.print') as mock_print:
        presenter.present(review)
        mock_print.assert_called_once_with("\nNo cards to review today!")


def test_present_single_new_card():
    """Test presenting a deck with one new card."""
    presenter = ConsolePresenter()
    deck = DeckCards(
        "Test Deck",
        new_cards=[Card(front="What is Python?", back="A programming language")],
        learning_cards=[],
        review_cards=[]
    )
    review = TodayReview([deck])

    with patch('src.infrastructure.presentation.console.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 1"),
            call("Test Deck:"),
            call("  New cards (1):"),
            call("    - Front: What is Python?"),
            call("      Back:  A programming language")
        ])


def test_present_single_learning_card():
    """Test presenting a deck with one learning card."""
    presenter = ConsolePresenter()
    deck = DeckCards(
        "Test Deck",
        new_cards=[],
        learning_cards=[Card(front="What is a decorator?", back="A function that modifies other functions")],
        review_cards=[]
    )
    review = TodayReview([deck])

    with patch('src.infrastructure.presentation.console.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 1"),
            call("Test Deck:"),
            call("  Learning cards (1):"),
            call("    - Front: What is a decorator?"),
            call("      Back:  A function that modifies other functions")
        ])


def test_present_single_review_card():
    """Test presenting a deck with one review card."""
    presenter = ConsolePresenter()
    deck = DeckCards(
        "Test Deck",
        new_cards=[],
        learning_cards=[],
        review_cards=[Card(front="What is dependency injection?", back="A design pattern that implements IoC")]
    )
    review = TodayReview([deck])

    with patch('src.infrastructure.presentation.console.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 1"),
            call("Test Deck:"),
            call("  Review cards (1):"),
            call("    - Front: What is dependency injection?"),
            call("      Back:  A design pattern that implements IoC")
        ])


def test_present_multiple_decks_with_mixed_cards():
    """Test presenting multiple decks with mixed card types."""
    presenter = ConsolePresenter()
    
    python_deck = DeckCards(
        "Python",
        new_cards=[Card(front="What is a list comprehension?", back="A concise way to create lists")],
        learning_cards=[Card(front="How to use decorators?", back="Use @ syntax above functions")],
        review_cards=[Card(front="What is the GIL?", back="Global Interpreter Lock")]
    )
    
    design_patterns_deck = DeckCards(
        "Design Patterns",
        new_cards=[Card(front="What is the Factory pattern?", back="Creates objects without specifying exact class")],
        learning_cards=[Card(front="When to use the Observer pattern?", back="When you need one-to-many dependencies")],
        review_cards=[Card(front="Explain dependency injection.", back="Passing dependencies instead of creating them")]
    )
    
    review = TodayReview([python_deck, design_patterns_deck])

    with patch('src.infrastructure.presentation.console.print') as mock_print:
        presenter.present(review)
        mock_print.assert_has_calls([
            call("\nTotal cards to review today: 6"),
            call("Python:"),
            call("  New cards (1):"),
            call("    - Front: What is a list comprehension?"),
            call("      Back:  A concise way to create lists"),
            call("  Learning cards (1):"),
            call("    - Front: How to use decorators?"),
            call("      Back:  Use @ syntax above functions"),
            call("  Review cards (1):"),
            call("    - Front: What is the GIL?"),
            call("      Back:  Global Interpreter Lock"),
            call("Design Patterns:"),
            call("  New cards (1):"),
            call("    - Front: What is the Factory pattern?"),
            call("      Back:  Creates objects without specifying exact class"),
            call("  Learning cards (1):"),
            call("    - Front: When to use the Observer pattern?"),
            call("      Back:  When you need one-to-many dependencies"),
            call("  Review cards (1):"),
            call("    - Front: Explain dependency injection."),
            call("      Back:  Passing dependencies instead of creating them")
        ]) 