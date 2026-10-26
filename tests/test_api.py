import unittest

from server import create_app


class FixedWordManager:
    """Small test double that makes API tests deterministic."""

    words = {"easy": "apple", "medium": "banana", "hard": "chrysanthemum"}

    def choose_word(self, difficulty):
        normalized = difficulty.strip().lower() if isinstance(difficulty, str) else ""
        if normalized not in self.words:
            from word_manager import InvalidDifficultyError

            raise InvalidDifficultyError("Difficulty must be easy, medium, or hard.")
        return self.words[normalized]


class HangmanApiTests(unittest.TestCase):
    def setUp(self):
        app = create_app(FixedWordManager())
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def create_game(self, difficulty="easy"):
        response = self.client.post("/api/games", json={"difficulty": difficulty})
        self.assertEqual(201, response.status_code)
        return response.get_json()

    def test_creates_games_for_all_difficulties_without_exposing_words(self):
        for difficulty in ("easy", "medium", "hard"):
            with self.subTest(difficulty=difficulty):
                response = self.client.post("/api/games", json={"difficulty": difficulty})
                data = response.get_json()
                self.assertEqual(201, response.status_code)
                self.assertEqual("playing", data["status"])
                self.assertNotIn("word", data)
                self.assertTrue(data["game_id"])

    def test_separate_games_keep_separate_state(self):
        first = self.create_game("easy")
        second = self.create_game("medium")
        self.assertNotEqual(first["game_id"], second["game_id"])

        guess_response = self.client.post(f"/api/games/{first['game_id']}/guess", json={"letter": "a"})
        self.assertEqual(200, guess_response.status_code)
        self.assertEqual("a _ _ _ _", guess_response.get_json()["pattern"])

        second_state = self.client.get(f"/api/games/{second['game_id']}").get_json()
        self.assertEqual("_ _ _ _ _ _", second_state["pattern"])
        self.assertEqual([], second_state["guessed_letters"])

    def test_active_game_responses_never_expose_word(self):
        game = self.create_game()
        game_id = game["game_id"]
        responses = [
            game,
            self.client.get(f"/api/games/{game_id}").get_json(),
            self.client.post(f"/api/games/{game_id}/guess", json={"letter": "z"}).get_json(),
        ]
        for response in responses:
            with self.subTest(response=response):
                self.assertNotIn("word", response)
                self.assertNotIn("apple", str(response).lower())

    def test_win_and_loss_return_completed_state(self):
        game = self.create_game()
        for letter in "aple":
            response = self.client.post(f"/api/games/{game['game_id']}/guess", json={"letter": letter})
        self.assertEqual(200, response.status_code)
        self.assertEqual("won", response.get_json()["status"])
        self.assertEqual("apple", response.get_json()["word"])

        game = self.create_game()
        for letter in "bcdfgh":
            response = self.client.post(f"/api/games/{game['game_id']}/guess", json={"letter": letter})
        self.assertEqual("lost", response.get_json()["status"])
        self.assertEqual("apple", response.get_json()["word"])

    def test_invalid_requests_and_unknown_games_return_errors(self):
        invalid_creates = [
            self.client.post("/api/games"),
            self.client.post("/api/games", json={}),
            self.client.post("/api/games", json={"difficulty": "expert"}),
        ]
        for response in invalid_creates:
            self.assertEqual(400, response.status_code)
            self.assertIn("error", response.get_json())

        game = self.create_game()
        invalid_guesses = [
            self.client.post(f"/api/games/{game['game_id']}/guess"),
            self.client.post(f"/api/games/{game['game_id']}/guess", json={"letter": "ab"}),
        ]
        for response in invalid_guesses:
            self.assertEqual(400, response.status_code)
            self.assertIn("error", response.get_json())

        for url in ("/api/games/missing", "/api/games/missing/guess"):
            response = self.client.post(url, json={"letter": "a"}) if url.endswith("guess") else self.client.get(url)
            self.assertEqual(404, response.status_code)
            self.assertIn("error", response.get_json())

    def test_duplicate_and_finished_guesses_are_rejected(self):
        game = self.create_game()
        game_id = game["game_id"]
        self.client.post(f"/api/games/{game_id}/guess", json={"letter": "z"})
        duplicate = self.client.post(f"/api/games/{game_id}/guess", json={"letter": "z"})
        self.assertEqual(400, duplicate.status_code)
        self.assertEqual(5, duplicate.get_json()["remaining_guesses"])

        for letter in "aple":
            self.client.post(f"/api/games/{game_id}/guess", json={"letter": letter})
        finished = self.client.post(f"/api/games/{game_id}/guess", json={"letter": "q"})
        self.assertEqual(409, finished.status_code)
        self.assertIn("error", finished.get_json())


if __name__ == "__main__":
    unittest.main()
