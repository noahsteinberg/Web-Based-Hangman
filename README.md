# Web-Based Hangman

CSE 4095 individual assignment: build and deploy a Hangman game with a Python/Flask server and a browser client.

## Status

The independent game engine and word lists are complete. The Flask API, browser interface, and deployment will be implemented incrementally according to `TODO.md`.

## Word lists

The project includes original, manually selected English word lists: 35 Easy words, 35 Medium words, and 25 Hard words. The lists are lowercase alphabetic text files in `words/`; the application validates and de-duplicates them at load time.

## Run Phase 2 tests

From the project folder, run:

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

## API (Phase 3)

The Flask server keeps every game in memory and is the only component that decides game results. Run it locally with:

```powershell
.\.venv\Scripts\python server.py
```

Endpoints accept and return JSON:

- `POST /api/games` with `{"difficulty": "easy"}`, `medium`, or `hard`
- `GET /api/games/<game_id>`
- `POST /api/games/<game_id>/guess` with `{"letter": "a"}`

While a game is active, responses contain its masked pattern and state but never the hidden word. The word appears only when the game is won or lost.

## Browser client (Phase 4)

Visit `http://127.0.0.1:5000/` after starting `server.py`. Choose a difficulty, select **New game**, then use the on-screen or physical keyboard. The browser sends every action to the Flask API; it does not contain the active hidden word or independent Hangman rules.

## Reference materials

- `Specification.md` is the original, broader specification.
- `TODO.md` narrows the work to this assignment.
- `cursor_transcript.md` is instructor guidance only; this project will use an independent implementation.
