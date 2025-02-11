"""Tests for the AnkiToday use case."""

from unittest.mock import Mock
import pytest

from src.core.ports import CardRepository, ReviewPresenter
from src.core.entities import DeckCards, TodayReview
from src.application.use_cases.today_review import AnkiToday


@pytest.fixture
def repository():
    """Create a mock repository."""
    return Mock(spec=CardRepository)


@pytest.fixture
def presenter():
    """Create a mock presenter."""
    return Mock(spec=ReviewPresenter)


@pytest.fixture
def use_case(repository, presenter):
    """Create an instance of AnkiToday use case."""
    return AnkiToday(repository=repository, presenter=presenter)


def test_execute_with_empty_review(use_case, repository, presenter):
    """Test executing use case when there are no cards to review."""
    repository.get_today_review.return_value = TodayReview([])

    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with(TodayReview([]))


def test_execute_with_cards_to_review(use_case, repository, presenter):
    """Test executing use case when there are cards to review."""
    deck = DeckCards(
        deck_name="Test Deck",
        new_cards=["New card"],
        learning_cards=["Learning card"],
        review_cards=["Review card"]
    )
    review = TodayReview([deck])
    
    repository.get_today_review.return_value = review

    use_case.execute()

    repository.get_today_review.assert_called_once()
    presenter.present.assert_called_once_with(review)


def test_execute_without_deck_filter(use_case, repository, presenter):
    """Test executing the use case without deck filter."""
    review = TodayReview([])
    repository.get_today_review.return_value = review

    use_case.execute()

    repository.get_today_review.assert_called_once_with(deck_name=None)
    presenter.present.assert_called_once_with(review)


def test_execute_with_deck_filter(use_case, repository, presenter):
    """Test executing the use case with deck filter."""
    review = TodayReview([])
    repository.get_today_review.return_value = review

    use_case.execute(deck_name="Test Deck")

    repository.get_today_review.assert_called_once_with(deck_name="Test Deck")
    presenter.present.assert_called_once_with(review) 