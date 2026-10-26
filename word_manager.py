"""Load and choose Hangman words independently of Flask and the game UI."""

from __future__ import annotations

from pathlib import Path
from random import choice


class InvalidDifficultyError(ValueError):
    """Raised when a requested difficulty is not supported."""


class WordListError(ValueError):
    """Raised when a word-list file is missing, empty, or invalid."""


class WordManager:
    DIFFICULTIES = ("easy", "medium", "hard")

    def __init__(self, words_directory: str | Path | None = None):
        self.words_directory = Path(words_directory) if words_directory else Path(__file__).parent / "words"
        self._words_by_difficulty = {
            difficulty: self._load_file(self.words_directory / f"{difficulty}.txt")
            for difficulty in self.DIFFICULTIES
        }

    def choose_word(self, difficulty: str) -> str:
        normalized_difficulty = self._validate_difficulty(difficulty)
        return choice(self._words_by_difficulty[normalized_difficulty])

    def words_for(self, difficulty: str) -> tuple[str, ...]:
        normalized_difficulty = self._validate_difficulty(difficulty)
        return self._words_by_difficulty[normalized_difficulty]

    @classmethod
    def _validate_difficulty(cls, difficulty: str) -> str:
        if not isinstance(difficulty, str) or difficulty.strip().lower() not in cls.DIFFICULTIES:
            raise InvalidDifficultyError("Difficulty must be easy, medium, or hard.")
        return difficulty.strip().lower()

    @staticmethod
    def _load_file(path: Path) -> tuple[str, ...]:
        if not path.is_file():
            raise WordListError(f"Word list not found: {path}")

        words: list[str] = []
        for line_number, raw_word in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            word = raw_word.strip().lower()
            if not word:
                continue
            if not word.isalpha():
                raise WordListError(f"Invalid word in {path.name} at line {line_number}: {raw_word!r}")
            if word not in words:
                words.append(word)

        if not words:
            raise WordListError(f"Word list is empty: {path}")
        return tuple(words)
