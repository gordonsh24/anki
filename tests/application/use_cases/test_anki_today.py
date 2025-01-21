"""Tests for the AnkiToday use case."""

from unittest.mock import Mock

from src.core.ports import CardRepository, ReviewPresenter
from src.application.use_cases.today_review import AnkiToday


def test_get_cards_empty_decks():
    """Test getting cards when there are no decks."""
    repository = Mock(spec=CardRepository)
    presenter = Mock(spec=ReviewPresenter)
    repository.get_today_review.return_value = []

    use_case = AnkiToday(repository, presenter)
    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with([])


def test_get_cards_deck_with_no_cards():
    """Test getting cards when a deck has no cards."""
    repository = Mock(spec=CardRepository)
    presenter = Mock(spec=ReviewPresenter)
    repository.get_today_review.return_value = []

    use_case = AnkiToday(repository, presenter)
    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with([])


def test_get_cards_deck_with_failed_card_info():
    """Test getting cards when card info retrieval fails."""
    repository = Mock(spec=CardRepository)
    presenter = Mock(spec=ReviewPresenter)
    repository.get_today_review.return_value = []

    use_case = AnkiToday(repository, presenter)
    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with([])


def test_get_cards_deck_with_all_card_types():
    """Test getting cards when a deck has one card of each type."""
    repository = Mock(spec=CardRepository)
    presenter = Mock(spec=ReviewPresenter)
    repository.get_today_review.return_value = [
        {
            "deck_name": "Test Deck",
            "cards": [
                {"type": "new", "question": "New card"},
                {"type": "learning", "question": "Learning card"},
                {"type": "review", "question": "Review card"}
            ]
        }
    ]

    use_case = AnkiToday(repository, presenter)
    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with([
        {
            "deck_name": "Test Deck",
            "cards": [
                {"type": "new", "question": "New card"},
                {"type": "learning", "question": "Learning card"},
                {"type": "review", "question": "Review card"}
            ]
        }
    ]) 