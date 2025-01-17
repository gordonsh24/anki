#!/usr/bin/env python3

import json
import requests
from datetime import datetime

def invoke(action, **params):
    request_data = {
        "action": action,
        "version": 6,
        "params": params
    }
    response = requests.post('http://localhost:8765', json=request_data)
    return response.json()

def get_deck_names():
    """Get a list of parent deck names from Anki."""
    decks = invoke('deckNames')
    if decks.get('error'):
        print(f"Error: {decks['error']}")
        return None
    
    # Filter out sub-decks by keeping only decks without "::"
    parent_decks = [deck for deck in decks['result'] if "::" not in deck]
    return parent_decks

def get_card_info(card_ids):
    """Get detailed information about specific cards."""
    result = invoke('cardsInfo', cards=card_ids)
    if result.get('error'):
        print(f"Error getting card info: {result['error']}")
        return []
    return result['result']

def get_first_field_value(card):
    """Get the value of the first field in the card, regardless of its name."""
    if not card['fields']:
        return "Empty card"
    # Get the first field's value
    first_field = next(iter(card['fields'].values()))
    return first_field['value']

def get_today_reviews():
    # Get all deck names first
    decks = get_deck_names()
    if decks is None:
        return
    
    print("\nDecks found:", decks)
    print("\nCards due today by deck:")
    print("-" * 50)
    
    total_cards = 0
    
    for deck in decks:
        # Find cards due today in this deck
        query = f'deck:"{deck}" (is:due or is:new)'
        result = invoke('findCards', query=query)
        
        if result.get('error'):
            print(f"Error finding cards in {deck}: {result['error']}")
            continue
            
        card_ids = result['result']
        if not card_ids:
            continue
            
        cards_info = get_card_info(card_ids)
        if not cards_info:
            continue
            
        print(f"\n{deck}:")
        
        # Group cards by type
        new_cards = []
        review_cards = []
        learning_cards = []
        
        for card in cards_info:
            question = get_first_field_value(card)
            if card['type'] == 0:  # New card
                new_cards.append(question)
            elif card['type'] == 1:  # Learning card
                learning_cards.append(question)
            elif card['type'] == 2:  # Review card
                review_cards.append(question)
        
        if new_cards:
            print("  New cards:")
            for q in new_cards:
                print(f"    - {q}")
        
        if learning_cards:
            print("  Learning cards:")
            for q in learning_cards:
                print(f"    - {q}")
        
        if review_cards:
            print("  Review cards:")
            for q in review_cards:
                print(f"    - {q}")
        
        deck_total = len(new_cards) + len(learning_cards) + len(review_cards)
        total_cards += deck_total
        print(f"  Total in deck: {deck_total}")
    
    print("\n" + "-" * 50)
    print(f"Total cards to review: {total_cards}")

if __name__ == "__main__":
    try:
        # Check if Anki is running and accessible
        version = invoke('version')
        if version.get('error'):
            print("Error: Could not connect to Anki.")
            print("Please make sure that:")
            print("1. Anki is running")
            print("2. AnkiConnect add-on is installed")
            print("3. No firewall is blocking the connection")
        else:
            print(f"Connected to AnkiConnect v{version['result']}")
            get_today_reviews()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Anki. Is it running?") 