class Player:
    """Encapsulates the state of a single trivia player."""

    STARTING_POSITION = 1

    def __init__(self, name: str) -> None:
        self.name = name
        self.position: int = self.STARTING_POSITION
        self.coins: int = 0
        self.in_penalty_box: bool = False

    def move(self, roll: int, board_size: int) -> None:
        self.position += roll
        if self.position > board_size:
            self.position -= board_size

    def add_coin(self) -> None:
        self.coins += 1

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return (
            f"Player(name={self.name!r}, position={self.position}, "
            f"coins={self.coins}, in_penalty_box={self.in_penalty_box})"
        )
