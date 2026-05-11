"""
test_game.py — pytest suite for the Python Trivia Kata.

Covers:
  - Player: creation, movement, wrapping, coin tracking, penalty box
  - QuestionDeck: category serving and exhaustion
  - Game: full integration (correct answer, wrong answer, win condition,
          Geography category, penalty box mechanics)
"""
import io
import sys
from contextlib import contextmanager

import pytest

from game import Game
from player import Player
from question_deck import QuestionDeck


# ────────────────────────────────────────────────────────────────────────
# Helpers
# ────────────────────────────────────────────────────────────────────────

@contextmanager
def captured_output():
    """Context manager: capture stdout and return it as a string."""
    buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    try:
        yield buf
    finally:
        sys.stdout = old_stdout


def make_game(*player_names: str) -> Game:
    """Factory: build a game with the given players."""
    game = Game()
    for name in player_names:
        game.add(name)
    return game


# ────────────────────────────────────────────────────────────────────────
# Player tests
# ────────────────────────────────────────────────────────────────────────

class TestPlayer:
    def test_initial_state(self):
        p = Player("Alice")
        assert p.name == "Alice"
        assert p.position == 1
        assert p.coins == 0
        assert p.in_penalty_box is False

    def test_str_returns_name(self):
        assert str(Player("Bob")) == "Bob"

    def test_add_coin_increments(self):
        p = Player("Alice")
        p.add_coin()
        p.add_coin()
        assert p.coins == 2

    def test_move_advances_position(self):
        p = Player("Alice")
        p.move(3, board_size=12)
        assert p.position == 4

    def test_move_wraps_around_board(self):
        p = Player("Alice")
        p.position = 11
        p.move(4, board_size=12)   # 11 + 4 = 15 → 15 - 12 = 3
        assert p.position == 3

    def test_move_exactly_at_board_size_does_not_wrap(self):
        p = Player("Alice")
        p.position = 9
        p.move(3, board_size=12)   # 9 + 3 = 12 — should NOT wrap
        assert p.position == 12


# ────────────────────────────────────────────────────────────────────────
# QuestionDeck tests
# ────────────────────────────────────────────────────────────────────────

class TestQuestionDeck:
    def test_first_pop_question(self):
        deck = QuestionDeck()
        assert deck.next_question("Pop") == "Pop Question 0"

    def test_first_geography_question(self):
        deck = QuestionDeck()
        assert deck.next_question("Geography") == "Geography Question 0"

    def test_questions_are_sequential(self):
        deck = QuestionDeck()
        assert deck.next_question("Science") == "Science Question 0"
        assert deck.next_question("Science") == "Science Question 1"
        assert deck.next_question("Science") == "Science Question 2"

    def test_all_five_categories_exist(self):
        deck = QuestionDeck()
        for cat in ("Pop", "Science", "Sports", "Geography", "Rock"):
            assert deck.next_question(cat).startswith(cat)

    def test_deck_has_50_questions_per_category(self):
        deck = QuestionDeck()
        for _ in range(50):
            deck.next_question("Rock")
        with pytest.raises((IndexError, KeyError)):
            deck.next_question("Rock")


# ────────────────────────────────────────────────────────────────────────
# Game integration tests
# ────────────────────────────────────────────────────────────────────────

class TestGameSetup:
    def test_add_players(self):
        game = Game()
        game.add("Chet")
        game.add("Pat")
        assert game.how_many_players() == 2

    def test_has_enough_players_requires_two(self):
        game = Game()
        assert game.has_enough_players() is False
        game.add("Chet")
        assert game.has_enough_players() is False
        game.add("Pat")
        assert game.has_enough_players() is True


class TestGameRoll:
    def test_roll_prints_player_info(self):
        game = make_game("Chet", "Pat")
        with captured_output() as buf:
            game.roll(3)
        output = buf.getvalue()
        assert "Chet is the current player" in output
        assert "They have rolled a 3" in output

    def test_roll_prints_category(self):
        game = make_game("Chet", "Pat")
        with captured_output() as buf:
            game.roll(3)          # position 1 + 3 = 4 → category Geography
        assert "The category is Geography" in buf.getvalue()

    def test_roll_geography_category(self):
        game = make_game("Chet", "Pat")
        with captured_output() as buf:
            game.roll(3)          # position 1 → 4 (Pop)
            game.handle_correct_answer()   # advance to Pat
            game.roll(3)          # Pat: position 1 → 4 (Pop)
            game.handle_correct_answer()   # advance to Chet
            game.roll(3)          # Chet: 4 → 7 (Sports) -- adjust to hit Geography
        # Use a fresh game to land directly on Geography (position 4)
        g2 = make_game("Alice", "Bob")
        # Alice starts at 1; roll 3 → position 4 → Geography
        with captured_output() as out2:
            g2.roll(3)
        assert "Geography" in out2.getvalue()


class TestCorrectAnswer:
    def test_correct_answer_awards_coin(self):
        game = make_game("Chet", "Pat")
        with captured_output():
            game.roll(1)
            game.handle_correct_answer()
        # After Chet's turn, rotate back and inspect
        # Re-roll so Chet is current again after Pat's turn
        with captured_output():
            game.roll(1)
            game.handle_correct_answer()
        # Chet should have 1 coin after his first correct answer
        assert game._players[0].coins == 1

    def test_correct_answer_prints_correct_text(self):
        game = make_game("Chet", "Pat")
        with captured_output() as buf:
            game.roll(1)
            game.handle_correct_answer()
        assert "Answer was correct!!!!" in buf.getvalue()

    def test_correct_answer_advances_turn(self):
        game = make_game("Chet", "Pat")
        with captured_output():
            game.roll(1)
            game.handle_correct_answer()
        # After Chet answers, Pat should be current
        assert str(game._current_player()) == "Pat"


class TestWrongAnswer:
    def test_wrong_answer_sends_to_penalty_box(self):
        game = make_game("Chet", "Pat")
        with captured_output():
            game.roll(1)
            game.wrong_answer()
        assert game._players[0].in_penalty_box is True

    def test_wrong_answer_advances_turn(self):
        game = make_game("Chet", "Pat")
        with captured_output():
            game.roll(1)
            game.wrong_answer()
        assert str(game._current_player()) == "Pat"

    def test_wrong_answer_returns_true(self):
        game = make_game("Chet", "Pat")
        with captured_output():
            game.roll(1)
            result = game.wrong_answer()
        assert result is True


class TestPenaltyBox:
    def _send_to_penalty(self, game: Game) -> None:
        with captured_output():
            game.roll(1)
            game.wrong_answer()     # Chet is now in penalty box

    def test_even_roll_stays_in_penalty_box(self):
        game = make_game("Chet", "Pat")
        self._send_to_penalty(game)
        # Pat's turn
        with captured_output():
            game.roll(1)
            game.handle_correct_answer()
        # Chet's turn — even roll stays in box
        with captured_output() as buf:
            game.roll(2)
        assert "not getting out of the penalty box" in buf.getvalue()

    def test_odd_roll_gets_out_of_penalty_box(self):
        game = make_game("Chet", "Pat")
        self._send_to_penalty(game)
        with captured_output():
            game.roll(1)
            game.handle_correct_answer()
        # Chet's turn — odd roll escapes
        with captured_output() as buf:
            game.roll(1)
        assert "is getting out of the penalty box" in buf.getvalue()


class TestWinCondition:
    def test_player_wins_after_six_coins(self):
        game = make_game("Chet", "Pat")
        not_a_winner = True
        with captured_output():
            while not_a_winner:
                game.roll(1)
                not_a_winner = game.handle_correct_answer()
                if not not_a_winner:
                    break
                game.roll(1)
                not_a_winner = game.handle_correct_answer()
        # Winner found — at least one player must have 6 coins
        assert any(p.coins == 6 for p in game._players)

    def test_handle_correct_returns_false_on_win(self):
        """handle_correct_answer returns False when the game ends."""
        game = make_game("Chet", "Pat")
        # Give Chet 5 coins manually, then win on the next correct answer
        game._players[0].coins = 5
        results = []
        with captured_output():
            game.roll(1)
            results.append(game.handle_correct_answer())
        assert results[-1] is False
