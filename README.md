# Anki Today

A simple Python script that shows all cards due for review today in your Anki decks.

## Requirements

- Python 3.x
- Anki with AnkiConnect add-on installed
- `requests` library

## Installation

1. Make sure you have AnkiConnect add-on installed in Anki (add-on code: 2055492159)
2. Install the required Python package:
   ```bash
   pip install requests
   ```

## Usage

1. Make sure Anki is running
2. Run the script:
   ```bash
   python3 anki_today.py
   ```

The script will show all cards that need to be reviewed today, organized by deck and card type (new, learning, and review cards). 