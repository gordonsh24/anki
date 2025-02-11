"""Integration tests for CLI commands."""

from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from src.cli import app
from tests.fixtures.decks import TEST_DECKS
from tests.integration.utils import mock_container  # Updated import path


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.fixture
def test_decks_fixture():
    """Predefined test decks and their cards."""
    return TEST_DECKS


def test_list_command_default_params(mock_container, runner):
    """Test the list command with default parameters."""
    # Execute command
    result = runner.invoke(app, ["list"])
    
    # Print output for debugging
    print("\nCommand output:")
    print(result.output)
    
    # Verify command executed successfully
    assert result.exit_code == 0
    
    # Verify output contains expected deck names
    assert "Programming" in result.output
    assert "History" in result.output
    
    # Verify output contains expected cards
    assert "What is Python?" in result.output
    assert "A programming language" in result.output
    assert "What is a decorator?" in result.output
    assert "A function that modifies other functions" in result.output
    assert "Who was Julius Caesar?" in result.output
    assert "A Roman emperor" in result.output
    
    # Verify cards are categorized correctly
    assert "New cards" in result.output
    assert "Learning cards" in result.output
    assert "Review cards" in result.output 