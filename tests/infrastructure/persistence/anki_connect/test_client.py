"""Tests for AnkiConnectClient."""

import json
import pytest
from unittest.mock import patch
from requests.exceptions import RequestException

from src.infrastructure.persistence.anki_connect.client import AnkiConnectClient


@pytest.fixture
def client():
    """Create an instance of AnkiConnectClient."""
    return AnkiConnectClient()


def test_get_deck_names_success(client):
    """Test successful retrieval of deck names."""
    expected_decks = ["Default", "Test::Deck1", "Test::Deck2"]
    mock_response = {"result": expected_decks, "error": None}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        result = client.get_deck_names()

        assert result == expected_decks
        mock_post.assert_called_once_with(
            "http://localhost:8765",
            json={"action": "deckNames", "version": 6, "params": {}}
        )


def test_get_deck_names_empty(client):
    """Test when there are no decks."""
    mock_response = {"result": [], "error": None}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        result = client.get_deck_names()

        assert result == []


def test_get_deck_names_anki_error(client):
    """Test when AnkiConnect returns an error."""
    mock_response = {"result": None, "error": "Failed to connect to Anki"}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        with pytest.raises(RuntimeError) as exc_info:
            client.get_deck_names()

        assert "AnkiConnect error: Failed to connect to Anki" in str(exc_info.value)


def test_get_deck_names_network_error(client):
    """Test when there's a network error."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = RequestException("Network error")

        with pytest.raises(RuntimeError) as exc_info:
            client.get_deck_names()

        assert "Failed to communicate with Anki: Network error" in str(exc_info.value)


def test_get_deck_names_invalid_response(client):
    """Test when AnkiConnect returns invalid JSON."""
    with patch("requests.post") as mock_post:
        mock_post.return_value.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_post.return_value.raise_for_status.return_value = None

        with pytest.raises(RuntimeError) as exc_info:
            client.get_deck_names()

        assert "Invalid response from Anki" in str(exc_info.value)


def test_find_cards_success(client):
    """Test successful card search."""
    expected_cards = [1234, 5678]
    mock_response = {"result": expected_cards, "error": None}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        result = client.find_cards("deck:Test")

        assert result == expected_cards
        mock_post.assert_called_once_with(
            "http://localhost:8765",
            json={"action": "findCards", "version": 6, "params": {"query": "deck:Test"}}
        )


def test_find_cards_empty(client):
    """Test when no cards match the query."""
    mock_response = {"result": [], "error": None}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        result = client.find_cards("deck:NonExistent")

        assert result == []


def test_find_cards_anki_error(client):
    """Test when AnkiConnect returns an error during card search."""
    mock_response = {"result": None, "error": "Invalid search query"}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        with pytest.raises(RuntimeError) as exc_info:
            client.find_cards("invalid:query")

        assert "AnkiConnect error: Invalid search query" in str(exc_info.value)


def test_find_cards_network_error(client):
    """Test when there's a network error during card search."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = RequestException("Network error")

        with pytest.raises(RuntimeError) as exc_info:
            client.find_cards("deck:Test")

        assert "Failed to communicate with Anki: Network error" in str(exc_info.value)


def test_get_cards_info_success(client):
    """Test successful retrieval of cards info."""
    card_ids = [1234, 5678]
    expected_info = [
        {
            "cardId": 1234,
            "deckName": "Test",
            "fields": {"Front": {"value": "Question 1"}},
            "type": 0,
            "queue": 0
        },
        {
            "cardId": 5678,
            "deckName": "Test",
            "fields": {"Front": {"value": "Question 2"}},
            "type": 1,
            "queue": 1
        }
    ]
    mock_response = {"result": expected_info, "error": None}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        result = client.get_cards_info(card_ids)

        assert result == expected_info
        mock_post.assert_called_once_with(
            "http://localhost:8765",
            json={"action": "cardsInfo", "version": 6, "params": {"cards": card_ids}}
        )


def test_get_cards_info_empty(client):
    """Test when no cards are found."""
    mock_response = {"result": [], "error": None}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        result = client.get_cards_info([])

        assert result == []


def test_get_cards_info_anki_error(client):
    """Test when AnkiConnect returns an error during cards info retrieval."""
    mock_response = {"result": None, "error": "Invalid card IDs"}

    with patch("requests.post") as mock_post:
        mock_post.return_value.json.return_value = mock_response
        mock_post.return_value.raise_for_status.return_value = None

        with pytest.raises(RuntimeError) as exc_info:
            client.get_cards_info([99999])

        assert "AnkiConnect error: Invalid card IDs" in str(exc_info.value)


def test_get_cards_info_network_error(client):
    """Test when there's a network error during cards info retrieval."""
    with patch("requests.post") as mock_post:
        mock_post.side_effect = RequestException("Network error")

        with pytest.raises(RuntimeError) as exc_info:
            client.get_cards_info([1234])

        assert "Failed to communicate with Anki: Network error" in str(exc_info.value) 