"""Tests for the AnkiToday use case."""

from unittest.mock import Mock

from src.core.ports import CardRepository, ReviewPresenter
from src.core.entities import DeckCards, TodayReview
from src.application.use_cases.today_review import AnkiToday


def test_execute_with_empty_review():
    """Test executing use case when there are no cards to review."""
    repository = Mock(spec=CardRepository)
    presenter = Mock(spec=ReviewPresenter)
    repository.get_today_review.return_value = TodayReview([])

    use_case = AnkiToday(repository, presenter)
    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with(TodayReview([]))


def test_execute_with_cards_to_review():
    """Test executing use case when there are cards to review."""
    repository = Mock(spec=CardRepository)
    presenter = Mock(spec=ReviewPresenter)
    
    deck = DeckCards(
        deck_name="Test Deck",
        new_cards=["New card"],
        learning_cards=["Learning card"],
        review_cards=["Review card"]
    )
    review = TodayReview([deck])
    
    repository.get_today_review.return_value = review

    use_case = AnkiToday(repository, presenter)
    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with(review) 