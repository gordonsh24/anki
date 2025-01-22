"""Tests for AnkiCardMapper."""

import pytest

from src.infrastructure.persistence.anki_connect.mapper import AnkiCardMapper
from src.core.entities import DeckCards


@pytest.fixture
def mapper():
    """Create an instance of AnkiCardMapper."""
    return AnkiCardMapper()


def test_to_deck_cards_empty_list(mapper):
    """Test converting empty card list."""
    result = mapper.to_deck_cards("Test Deck", [])
    assert isinstance(result, DeckCards)
    assert result.deck_name == "Test Deck"
    assert result.new_cards == []
    assert result.learning_cards == []
    assert result.review_cards == []


def test_to_deck_cards_mixed_types(mapper):
    """Test converting cards of different types."""
    cards = [
        {
            "queue": 0,
            "type": 0,
            "fields": {"Front": {"value": "new card 1"}}
        },
        {
            "queue": 0,
            "type": 1,
            "fields": {"Front": {"value": "new card 2"}}
        },
        {
            "queue": 1,
            "type": 1,
            "fields": {"Front": {"value": "learning card 1"}}
        },
        {
            "queue": 3,
            "type": 1,
            "fields": {"Front": {"value": "learning card 2"}}
        },
        {
            "queue": 2,
            "type": 2,
            "fields": {"Front": {"value": "review card"}}
        }
    ]
    
    result = mapper.to_deck_cards("Test Deck", cards)
    assert result.deck_name == "Test Deck"
    assert result.new_cards == ["new card 1", "new card 2"]
    assert result.learning_cards == ["learning card 1", "learning card 2"]
    assert result.review_cards == ["review card"]


def test_to_deck_cards_with_missing_fields(mapper):
    """Test converting cards with missing or empty fields."""
    cards = [
        {
            "queue": 0,
            "type": 0,
            "fields": {}
        },
        {
            "queue": 1,
            "type": 1
        }
    ]
    
    result = mapper.to_deck_cards("Test Deck", cards)
    assert result.deck_name == "Test Deck"
    assert result.new_cards == [""]
    assert result.learning_cards == [""]
    assert result.review_cards == [] 