"""Tests for the AnkiList use case."""

from unittest.mock import Mock
import pytest

from src.application.use_cases.list_cards import AnkiList
from src.core.entities import TodayReview


@pytest.fixture
def repository():
    """Create a mock repository."""
    return Mock()


@pytest.fixture
def presenter():
    """Create a mock presenter."""
    return Mock()


@pytest.fixture
def use_case(repository, presenter):
    """Create an instance of AnkiList use case."""
    return AnkiList(repository=repository, presenter=presenter)


def test_execute_with_default_parameters(use_case, repository, presenter):
    """Test executing the use case with default parameters."""
    review = TodayReview([])
    repository.get_all_cards.return_value = review

    use_case.execute()

    repository.get_all_cards.assert_called_once_with(limit=20, offset=0, deck_name=None, random=False)
    presenter.present.assert_called_once_with(review)


def test_execute_with_custom_parameters(use_case, repository, presenter):
    """Test executing the use case with custom parameters."""
    review = TodayReview([])
    repository.get_all_cards.return_value = review

    use_case.execute(limit=10, offset=5, deck="Test Deck", random=True)

    repository.get_all_cards.assert_called_once_with(limit=10, offset=5, deck_name="Test Deck", random=True)
    presenter.present.assert_called_once_with(review) 