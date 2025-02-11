"""Test fixtures for deck data."""

TEST_DECKS = [
    {
        "name": "Programming",
        "cards": [
            {
                "id": 1,
                "fields": {
                    "Front": {"value": "What is Python?"},
                    "Back": {"value": "A programming language"}
                },
                "type": 0,
                "queue": 0  # New card
            },
            {
                "id": 2,
                "fields": {
                    "Front": {"value": "What is a decorator?"},
                    "Back": {"value": "A function that modifies other functions"}
                },
                "type": 1,
                "queue": 1  # Learning card
            }
        ]
    },
    {
        "name": "History",
        "cards": [
            {
                "id": 3,
                "fields": {
                    "Front": {"value": "Who was Julius Caesar?"},
                    "Back": {"value": "A Roman emperor"}
                },
                "type": 2,
                "queue": 2  # Review card
            }
        ]
    }
] 