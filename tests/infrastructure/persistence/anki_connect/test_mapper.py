"""Tests for AnkiCardMapper."""

import pytest

from src.infrastructure.persistence.anki_connect.mapper import AnkiCardMapper
from src.core.entities import DeckCards, Card


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
            "fields": {
                "Front": {"value": "new card 1"},
                "Back": {"value": "answer 1"}
            }
        },
        {
            "queue": 0,
            "type": 1,
            "fields": {
                "Front": {"value": "new card 2"},
                "Back": {"value": "answer 2"}
            }
        },
        {
            "queue": 1,
            "type": 1,
            "fields": {
                "Front": {"value": "learning card 1"},
                "Back": {"value": "answer 3"}
            }
        },
        {
            "queue": 3,
            "type": 1,
            "fields": {
                "Front": {"value": "learning card 2"},
                "Back": {"value": "answer 4"}
            }
        },
        {
            "queue": 2,
            "type": 2,
            "fields": {
                "Front": {"value": "review card"},
                "Back": {"value": "answer 5"}
            }
        }
    ]
    
    result = mapper.to_deck_cards("Test Deck", cards)
    assert result.deck_name == "Test Deck"
    assert [(card.front, card.back) for card in result.new_cards] == [
        ("new card 1", "answer 1"),
        ("new card 2", "answer 2")
    ]
    assert [(card.front, card.back) for card in result.learning_cards] == [
        ("learning card 1", "answer 3"),
        ("learning card 2", "answer 4")
    ]
    assert [(card.front, card.back) for card in result.review_cards] == [
        ("review card", "answer 5")
    ]


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
    assert [(card.front, card.back) for card in result.new_cards] == [("", "")]
    assert [(card.front, card.back) for card in result.learning_cards] == [("", "")]
    assert result.review_cards == []


def test_get_field_value_missing_field(mapper):
    """Test getting field value when the field doesn't exist."""
    card = {
        "fields": {
            "Front": {"value": "question"}
        }
    }
    assert mapper._get_field_value(card, "Back") == ""


def test_get_field_value_empty_fields(mapper):
    """Test getting field value when fields dict is empty."""
    card = {"fields": {}}
    assert mapper._get_field_value(card, "Front") == ""
    assert mapper._get_field_value(card, "Back") == ""


def test_get_field_value_no_fields(mapper):
    """Test getting field value when fields key doesn't exist."""
    card = {}
    assert mapper._get_field_value(card, "Front") == ""
    assert mapper._get_field_value(card, "Back") == "" 