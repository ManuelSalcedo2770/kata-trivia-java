from collections import deque


class QuestionDeck:
    """Owns and serves questions for every category, including Geography."""

    QUESTIONS_PER_CATEGORY = 50
    CATEGORIES = ("Pop", "Science", "Sports", "Geography", "Rock")

    def __init__(self) -> None:
        self._deck: dict[str, deque[str]] = {
            category: deque(
                f"{category} Question {i}"
                for i in range(self.QUESTIONS_PER_CATEGORY)
            )
            for category in self.CATEGORIES
        }

    def next_question(self, category: str) -> str:
        """Return and remove the next question for the given category."""
        return self._deck[category].popleft()
