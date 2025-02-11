"""Repository implementation using AnkiConnect."""

from typing import List, Optional
import random as random_module

from src.core.ports import CardRepository
from src.core.entities import DeckCards, TodayReview
from .client import AnkiConnectClient
from .mapper import AnkiCardMapper


class AnkiConnectCardRepository(CardRepository):
    """Repository for retrieving cards from Anki using AnkiConnect."""

    def __init__(self, client: AnkiConnectClient, mapper: AnkiCardMapper):
        """Initialize the repository.
        
        Args:
            client: AnkiConnect client for making requests
            mapper: Mapper for converting AnkiConnect data to domain entities
        """
        self._client = client
        self._mapper = mapper

    def get_today_review(self, deck_name: Optional[str] = None) -> TodayReview:
        """Get today's review cards.
        
        Args:
            deck_name: Optional deck name to filter by
            
        Returns:
            TodayReview containing the decks and their cards
        """
        if deck_name:
            deck_names = [deck_name]
        else:
            all_deck_names = self._client.get_deck_names()
            deck_names = self._filter_main_decks(all_deck_names)

        decks = []
        for name in deck_names:
            # Only get cards from the main deck that are due today
            query = f'deck:"{name}" is:due'  # Exact match for deck name and due today
            card_ids = self._client.find_cards(query)
            
            if not card_ids:
                continue
                
            cards = self._client.get_cards_info(card_ids)
            
            if not cards:
                continue
                
            deck_cards = self._mapper.to_deck_cards(name, cards)
            
            if deck_cards.total_cards > 0:
                decks.append(deck_cards)

        return TodayReview(decks)

    def get_all_cards(self, limit: int = 20, offset: int = 0, deck_name: Optional[str] = None, random: bool = False) -> TodayReview:
        """Get all cards, optionally filtered by deck.

        Args:
            limit: Maximum number of cards per deck to fetch
            offset: Number of cards to skip
            deck_name: Optional deck name to filter by
            random: Whether to randomize the order of cards

        Returns:
            A TodayReview entity containing the cards

        Raises:
            RuntimeError: If there's an error communicating with Anki
        """
        if deck_name:
            deck_names = [deck_name]
        else:
            deck_names = self._client.get_deck_names()
            deck_names = self._filter_main_decks(deck_names)

        decks = []
        for name in deck_names:
            # Find all cards in the deck
            card_ids = self._client.find_cards(f'deck:"{name}"')
            if not card_ids:
                continue

            # Randomize if requested
            if random:
                random_module.shuffle(card_ids)

            # Apply limit and offset
            card_ids = card_ids[offset:offset + limit]
            if not card_ids:
                continue

            # Get detailed information about the cards
            cards_info = self._client.get_cards_info(card_ids)
            if not cards_info:
                continue

            deck = self._mapper.to_deck_cards(name, cards_info)
            if deck.total_cards > 0:
                decks.append(deck)

        return TodayReview(decks=decks)

    @staticmethod
    def _filter_main_decks(deck_names: List[str]) -> List[str]:
        """Filter out sub-decks and return only main deck names.
        
        Args:
            deck_names: List of all deck names including sub-decks
            
        Returns:
            List of main deck names
        """
        main_decks = set()
        
        for deck_name in deck_names:
            # Get the top-level deck name (before first ::)
            main_deck = deck_name.split("::")[0]
            main_decks.add(main_deck)
            
        return sorted(main_decks) 