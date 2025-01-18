"""Port interface for presenting review data."""

from typing import Dict, Any
from ..entities import TodayReview

class ReviewPresenter:
    """Interface for presenting review information."""

    def present(self, review: TodayReview) -> Dict[str, Any]:
        """Present the review data in a format suitable for display."""
        pass 