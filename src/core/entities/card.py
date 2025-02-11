"""
Card entity representing a single Anki flashcard.
"""

from dataclasses import dataclass

@dataclass
class Card:
    """Represents a single Anki flashcard."""
    front: str 