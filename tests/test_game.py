import unittest

from game import GameFinishedError, HangmanGame


class HangmanGameTests(unittest.TestCase):
    def test_initial_state_masks_word_and_hides_answer(self):
        game = HangmanGame("apple")
        state = game.client_state()

        self.assertEqual("_ _ _ _ _", state["pattern"])
        self.assertEqual(6, state["remaining_guesses"])
        self.assertEqual("playing", state["status"])
        self.assertNotIn("word", state)

    def test_correct_guess_reveals_all_matching_positions(self):
        game = HangmanGame("apple")
        result = game.guess("P")

        self.assertTrue(result["accepted"])
        self.assertTrue(result["correct"])
        self.assertEqual("_ p p _ _", result["state"]["pattern"])
        self.assertEqual(6, result["state"]["remaining_guesses"])

    def test_incorrect_guess_reduces_remaining_guesses(self):
        game = HangmanGame("apple")
        result = game.guess("z")

        self.assertFalse(result["correct"])
        self.assertEqual(["z"], result["state"]["incorrect_letters"])
        self.assertEqual(5, result["state"]["remaining_guesses"])

    def test_duplicate_guess_does_not_change_state(self):
        game = HangmanGame("apple")
        game.guess("z")
        result = game.guess("z")

        self.assertFalse(result["accepted"])
        self.assertTrue(result["duplicate"])
        self.assertEqual(5, result["state"]["remaining_guesses"])

    def test_invalid_guesses_are_rejected(self):
        game = HangmanGame("apple")
        for invalid_guess in ("", "ab", "1", "?", None):
            with self.subTest(invalid_guess=invalid_guess):
                with self.assertRaises(ValueError):
                    game.guess(invalid_guess)

    def test_win_reveals_word_only_after_completion(self):
        game = HangmanGame("aba")
        game.guess("a")
        result = game.guess("b")

        self.assertEqual("won", result["state"]["status"])
        self.assertEqual("a b a", result["state"]["pattern"])
        self.assertEqual("aba", result["state"]["word"])
        with self.assertRaises(GameFinishedError):
            game.guess("c")

    def test_loss_reveals_word_after_six_incorrect_guesses(self):
        game = HangmanGame("a")
        for letter in "bcdefg":
            result = game.guess(letter)

        self.assertEqual("lost", result["state"]["status"])
        self.assertEqual(0, result["state"]["remaining_guesses"])
        self.assertEqual("a", result["state"]["word"])

    def test_invalid_game_word_is_rejected(self):
        for word in ("", "two words", "hi-ya", "123"):
            with self.subTest(word=word):
                with self.assertRaises(ValueError):
                    HangmanGame(word)


if __name__ == "__main__":
    unittest.main()
