"""Integration tests for CLI commands."""

from unittest.mock import patch
import pytest
from typer.testing import CliRunner

from src.cli import app
from tests.fixtures.decks import TEST_DECKS, TEST_DECKS_MANY_CARDS
from tests.integration.utils import mock_container  # Updated import path


@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()


@pytest.mark.parametrize('mock_container', [TEST_DECKS], indirect=True)
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


@pytest.mark.parametrize('mock_container', [TEST_DECKS_MANY_CARDS], indirect=True)
def test_list_command_with_limit(mock_container, runner):
    """Test the list command with a limit parameter."""
    # Execute command with limit=10
    result = runner.invoke(app, ["list", "--limit", "10"])
    
    # Print output for debugging
    print("\nCommand output:")
    print(result.output)
    
    # Verify command executed successfully
    assert result.exit_code == 0
    
    # Verify first 10 programming questions are present
    for i in range(1, 11):
        assert f"Programming Question {i}" in result.output
        assert f"Programming Answer {i}" in result.output
    
    # Verify programming question 11 is NOT present (beyond limit)
    assert "Programming Question 11" not in result.output
    
    # Verify first 10 history questions are present
    for i in range(16, 26):
        assert f"History Question {i}" in result.output
        assert f"History Answer {i}" in result.output
    
    # Verify history question 26 is NOT present (beyond limit)
    assert "History Question 26" not in result.output