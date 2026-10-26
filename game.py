"""Hangman game rules with no web-framework or user-interface dependency."""

from __future__ import annotations


class GameFinishedError(ValueError):
    """Raised when a guess is submitted after the game has ended."""


class HangmanGame:
    """Manage one server-authoritative game of Hangman."""

    MAX_INCORRECT_GUESSES = 6

    def __init__(self, word: str, max_incorrect_guesses: int = MAX_INCORRECT_GUESSES):
        normalized_word = word.strip().lower()
        if not normalized_word.isalpha():
            raise ValueError("The game word must contain alphabetic characters only.")
        if max_incorrect_guesses < 1:
            raise ValueError("max_incorrect_guesses must be at least 1.")

        self._word = normalized_word
        self.max_incorrect_guesses = max_incorrect_guesses
        self.guessed_letters: set[str] = set()
        self.incorrect_letters: set[str] = set()
        self.status = "playing"

    @property
    def remaining_guesses(self) -> int:
        return self.max_incorrect_guesses - len(self.incorrect_letters)

    @property
    def pattern(self) -> str:
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self._word)

    def guess(self, letter: str) -> dict:
        """Submit one letter and return its effect plus safe game state."""
        if self.status != "playing":
            raise GameFinishedError("This game has already ended.")

        normalized_letter = self._validate_letter(letter)
        if normalized_letter in self.guessed_letters:
            return {"accepted": False, "duplicate": True, "state": self.client_state()}

        self.guessed_letters.add(normalized_letter)
        correct = normalized_letter in self._word
        if not correct:
            self.incorrect_letters.add(normalized_letter)

        self._update_status()
        return {
            "accepted": True,
            "duplicate": False,
            "correct": correct,
            "state": self.client_state(),
        }

    def client_state(self) -> dict:
        """Return only data that may be sent to a client."""
        state = {
            "pattern": self.pattern,
            "guessed_letters": sorted(self.guessed_letters),
            "incorrect_letters": sorted(self.incorrect_letters),
            "remaining_guesses": self.remaining_guesses,
            "status": self.status,
        }
        if self.status != "playing":
            state["word"] = self._word
        return state

    @staticmethod
    def _validate_letter(letter: str) -> str:
        if not isinstance(letter, str):
            raise ValueError("A guess must be a single letter.")
        normalized_letter = letter.strip().lower()
        if len(normalized_letter) != 1 or not normalized_letter.isalpha():
            raise ValueError("A guess must be a single letter.")
        return normalized_letter

    def _update_status(self) -> None:
        if all(letter in self.guessed_letters for letter in self._word):
            self.status = "won"
        elif self.remaining_guesses == 0:
            self.status = "lost"
