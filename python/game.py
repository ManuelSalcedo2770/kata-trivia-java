from __future__ import annotations

from player import Player
from question_deck import QuestionDeck


class Game:
    """Trivia game — refactored, clean version with SRP and no parallel arrays."""

    WINNING_COINS = 6
    BOARD_SIZE = 12

    # Maps board position (1-based) to category name.
    _CATEGORY_MAP: dict[int, str] = {
        1: "Pop",    5: "Pop",    9:  "Pop",
        2: "Science",6: "Science",10: "Science",
        3: "Sports", 7: "Sports", 11: "Sports",
        4: "Geography", 8: "Geography", 12: "Geography",
    }

    def __init__(self) -> None:
        self._players: list[Player] = []
        self._question_deck = QuestionDeck()
        self._current_player_index: int = 0
        self._is_getting_out_of_penalty_box: bool = False

    # ------------------------------------------------------------------ #
    #  Public API (mirrors IGame)                                          #
    # ------------------------------------------------------------------ #

    def add(self, player_name: str) -> bool:
        self._players.append(Player(player_name))
        print(f"{player_name} was added")
        print(f"They are player number {len(self._players)}")
        return True

    def has_enough_players(self) -> bool:
        return self.how_many_players() >= 2

    def how_many_players(self) -> int:
        return len(self._players)

    def roll(self, roll: int) -> None:
        player = self._current_player()
        print(f"{player} is the current player")
        print(f"They have rolled a {roll}")

        if player.in_penalty_box:
            self._handle_penalty_box_turn(player, roll)
        else:
            self._handle_normal_turn(player, roll)

    def handle_correct_answer(self) -> bool:
        player = self._current_player()

        if player.in_penalty_box:
            if self._is_getting_out_of_penalty_box:
                self._award_coin(player)
                winner = self._player_has_won()
                self._advance_turn()
                return not winner
            else:
                self._advance_turn()
                return True
        else:
            self._award_coin(player)
            winner = self._player_has_won()
            self._advance_turn()
            return not winner

    def wrong_answer(self) -> bool:
        player = self._current_player()
        print("Question was incorrectly answered")
        print(f"{player} was sent to the penalty box")
        player.in_penalty_box = True
        self._advance_turn()
        return True

    # ------------------------------------------------------------------ #
    #  Private helpers                                                     #
    # ------------------------------------------------------------------ #

    def _current_player(self) -> Player:
        return self._players[self._current_player_index]

    def _handle_penalty_box_turn(self, player: Player, roll: int) -> None:
        if roll % 2 != 0:
            self._is_getting_out_of_penalty_box = True
            print(f"{player} is getting out of the penalty box")
            self._move_player(player, roll)
            self._ask_question()
        else:
            self._is_getting_out_of_penalty_box = False
            print(f"{player} is not getting out of the penalty box")

    def _handle_normal_turn(self, player: Player, roll: int) -> None:
        self._move_player(player, roll)
        self._ask_question()

    def _move_player(self, player: Player, roll: int) -> None:
        player.move(roll, self.BOARD_SIZE)
        print(f"{player}'s new location is {player.position}")
        print(f"The category is {self._current_category()}")

    def _ask_question(self) -> None:
        print(self._question_deck.next_question(self._current_category()))

    def _current_category(self) -> str:
        return self._CATEGORY_MAP.get(
            self._current_player().position, "Rock"
        )

    def _award_coin(self, player: Player) -> None:
        print("Answer was correct!!!!")
        player.add_coin()
        print(f"{player} now has {player.coins} Gold Coins.")

    def _player_has_won(self) -> bool:
        return self._current_player().coins == self.WINNING_COINS

    def _advance_turn(self) -> None:
        self._current_player_index = (
            self._current_player_index + 1
        ) % len(self._players)
