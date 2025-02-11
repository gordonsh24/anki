"""Common test utilities for integration tests."""

from unittest.mock import patch
import pytest

from src.application.containers import Container


@pytest.fixture
def mock_container(request):
    """Mock the container to use test configuration.
    
    This fixture provides a mocked Container with AnkiConnectClient
    that returns predefined test data. It's useful for integration tests
    of CLI commands.
    
    Args:
        request: pytest request object to get the test_decks parameter
        
    Returns:
        A mocked Container instance with test configuration
    """
    # Get test_decks from the requesting test, defaulting to None
    test_decks = getattr(request, "param", None)
    
    with patch('src.cli.Container', autospec=True) as mock_container_class:
        # Create a real container instance
        container = Container()
        
        # Replace the client in the container with our mock
        with patch('src.infrastructure.persistence.anki_connect.client.AnkiConnectClient') as mock_client_class:
            mock_client = mock_client_class.return_value
            
            # Mock deck names
            mock_client.get_deck_names.return_value = [deck["name"] for deck in test_decks] if test_decks else []
            
            # Mock find_cards to return card IDs for each deck
            def mock_find_cards(query):
                if not test_decks:
                    return []
                deck_name = query.split('"')[1]  # Extract deck name from query
                for deck in test_decks:
                    if deck["name"] == deck_name:
                        return [card["id"] for card in deck["cards"]]
                return []
            mock_client.find_cards.side_effect = mock_find_cards

            # Mock get_cards_info to return card details
            def mock_get_cards_info(card_ids):
                if not test_decks:
                    return []
                all_cards = [card for deck in test_decks for card in deck["cards"]]
                return [card for card in all_cards if card["id"] in card_ids]
            mock_client.get_cards_info.side_effect = mock_get_cards_info
            
            # Update container to use our mock client
            container.client.override(mock_client)
            
            # Make the container class return our configured container
            mock_container_class.return_value = container
            
            yield container 