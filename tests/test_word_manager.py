import tempfile
import unittest
from pathlib import Path

from word_manager import InvalidDifficultyError, WordListError, WordManager


class WordManagerTests(unittest.TestCase):
    def test_loads_each_difficulty_and_selects_a_member(self):
        manager = WordManager()
        for difficulty in WordManager.DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                words = manager.words_for(difficulty)
                self.assertGreater(len(words), 0)
                self.assertIn(manager.choose_word(difficulty), words)

    def test_difficulty_is_case_insensitive(self):
        manager = WordManager()
        self.assertEqual(manager.words_for("easy"), manager.words_for(" EASY "))

    def test_invalid_difficulty_is_rejected(self):
        manager = WordManager()
        for difficulty in ("expert", "", None):
            with self.subTest(difficulty=difficulty):
                with self.assertRaises(InvalidDifficultyError):
                    manager.choose_word(difficulty)

    def test_loader_normalizes_and_deduplicates_words(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            for difficulty in WordManager.DIFFICULTIES:
                (directory / f"{difficulty}.txt").write_text("Apple\n apple \nBANANA\n", encoding="utf-8")

            manager = WordManager(directory)
            self.assertEqual(("apple", "banana"), manager.words_for("easy"))

    def test_loader_rejects_non_alphabetic_word(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            directory = Path(temporary_directory)
            for difficulty in WordManager.DIFFICULTIES:
                (directory / f"{difficulty}.txt").write_text("valid\n", encoding="utf-8")
            (directory / "hard.txt").write_text("not-valid\n", encoding="utf-8")

            with self.assertRaises(WordListError):
                WordManager(directory)


if __name__ == "__main__":
    unittest.main()
