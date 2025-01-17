from abc import ABC, abstractmethod
from .models import TodayReview

class ReviewPresenter(ABC):
    """Interface for presenting review information."""
    
    @abstractmethod
    def show_no_cards(self) -> None:
        """Display message when there are no cards to review."""
        pass
    
    @abstractmethod
    def show_deck_list(self, deck_names: list[str]) -> None:
        """Display list of decks."""
        pass
    
    @abstractmethod
    def show_deck_cards(self, deck_name: str, new_cards: list[str], 
                       learning_cards: list[str], review_cards: list[str], 
                       total: int) -> None:
        """Display cards in a deck."""
        pass
    
    @abstractmethod
    def show_total_cards(self, total: int) -> None:
        """Display total number of cards."""
        pass
    
    @abstractmethod
    def show_connection_error(self) -> None:
        """Display connection error message."""
        pass
    
    @abstractmethod
    def show_connection_success(self, version: str) -> None:
        """Display successful connection message."""
        pass 