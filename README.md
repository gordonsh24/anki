# Anki Today

A simple Python script that shows all cards due for review today in your Anki decks.

## Requirements

- Python 3.x
- Anki with AnkiConnect add-on installed

## Installation

1. Make sure you have AnkiConnect add-on installed in Anki (add-on code: 2055492159)
2. Clone this repository
3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

This will install all required dependencies and create the `anki` command-line tool.

## Usage

1. Make sure Anki is running
2. Run the command:
   ```bash
   anki today
   ```

Additional options:
- Filter by deck name: `anki today --deck "My Deck"`
- Show detailed information: `anki today --verbose` or `anki today -v`

The command will show all cards that need to be reviewed today, organized by deck and card type (new, learning, and review cards).

## Tests

To run tests, make sure you have installed the package in development mode as described in the Installation section.

### Running all tests
```bash
pytest
```

### Running only unit tests
```bash
pytest tests/core tests/application tests/infrastructure
```

### Running only integration tests
```bash
pytest tests/integration
```

## How it works

The `anki` command is created during installation through Python's entry points system. When you run `pip install -e .`, it creates an executable script that runs the CLI application. You don't need to run any Python files directly. 