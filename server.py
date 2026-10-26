"""Flask REST API for server-authoritative Hangman games."""

from __future__ import annotations

from uuid import uuid4

from flask import Flask, jsonify, request

from game import GameFinishedError, HangmanGame
from word_manager import InvalidDifficultyError, WordManager


def create_app(word_manager: WordManager | None = None) -> Flask:
    """Create an application with isolated in-memory game storage."""
    app = Flask(__name__)
    app.config["WORD_MANAGER"] = word_manager or WordManager()
    app.config["GAMES"] = {}

    def error_response(message: str, status_code: int):
        return jsonify({"error": message}), status_code

    def get_game(game_id: str):
        game = app.config["GAMES"].get(game_id)
        if game is None:
            return None, error_response("Game not found.", 404)
        return game, None

    @app.get("/")
    def index():
        return app.send_static_file("index.html")

    @app.post("/api/games")
    def create_game():
        body = request.get_json(silent=True)
        if not isinstance(body, dict) or "difficulty" not in body:
            return error_response("Request JSON must include difficulty.", 400)

        try:
            word = app.config["WORD_MANAGER"].choose_word(body["difficulty"])
        except InvalidDifficultyError as error:
            return error_response(str(error), 400)

        game_id = uuid4().hex
        game = HangmanGame(word)
        app.config["GAMES"][game_id] = game
        return jsonify({"game_id": game_id, **game.client_state()}), 201

    @app.get("/api/games/<game_id>")
    def get_game_state(game_id: str):
        game, error = get_game(game_id)
        if error:
            return error
        return jsonify({"game_id": game_id, **game.client_state()})

    @app.post("/api/games/<game_id>/guess")
    def submit_guess(game_id: str):
        game, error = get_game(game_id)
        if error:
            return error

        body = request.get_json(silent=True)
        if not isinstance(body, dict) or "letter" not in body:
            return error_response("Request JSON must include letter.", 400)

        try:
            result = game.guess(body["letter"])
        except GameFinishedError as error:
            return error_response(str(error), 409)
        except ValueError as error:
            return error_response(str(error), 400)

        if result["duplicate"]:
            return jsonify({"error": "Letter has already been guessed.", **result["state"]}), 400

        return jsonify({"game_id": game_id, "correct": result["correct"], **result["state"]})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
