# Web-Based Hangman

CSE 4095 individual assignment: a browser-based Hangman game with a Python/Flask server. The server owns the game rules and hidden word; the browser communicates with it through a JSON REST API.

## Requirements

- Python 3.10 or newer
- A modern web browser such as Chrome

## Local setup

From the project folder, create and activate a virtual environment, then install the dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, run the commands below with `.\.venv\Scripts\python` instead of `python`.

## Run locally

Start the Flask development server:

```powershell
.\.venv\Scripts\python server.py
```

Open http://127.0.0.1:5000/ in a browser. Select a difficulty, choose **New game**, and use the on-screen letter buttons or your physical keyboard. A game ends after the word is guessed or after six incorrect guesses; choose **New game** to restart without reloading the page.

## Run tests

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

The tests cover game rules, word-list loading, API validation, separate games, win/loss paths, hidden-word protection, and serving the browser interface.

## REST API

All endpoints accept and return JSON.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/games` | Create a game for `easy`, `medium`, or `hard` difficulty. |
| `GET` | `/api/games/<game_id>` | Retrieve the current state of one game. |
| `POST` | `/api/games/<game_id>/guess` | Submit one letter guess. |

Create a game:

```json
{"difficulty": "easy"}
```

Submit a guess:

```json
{"letter": "a"}
```

While a game is `playing`, responses include the pattern, guessed letters, incorrect letters, remaining guesses, and status, but never the hidden word. The `word` field appears only after a win or loss.

## Project structure

```text
game.py                 # Framework-independent Hangman rules
word_manager.py         # Validates, loads, and selects words
server.py               # Flask routes and in-memory game storage
static/                 # Browser HTML, CSS, and JavaScript
tests/                  # Unit and API tests
words/                  # Easy, Medium, and Hard word lists
requirements.txt        # Python dependencies
TODO.md                 # Verified, phased assignment plan
```

## Word lists

The project includes AI-generated English word lists: 35 Easy words, 35 Medium words, and 25 Hard words. The lists are lowercase alphabetic text files in `words/`; the application validates and de-duplicates them at load time.

## Known limitations

- Games are stored only in memory, so server restarts clear active games.
- The application has no accounts, authentication, database, leaderboard, terminal client, or automated bots; these are outside this assignment's reduced scope.
- `server.py` runs Flask's development server locally. A production server command will be added for Render deployment.

## Render deployment

The repository includes `render.yaml` for a Python Web Service. Its preliminary service name is `noah-web-based-hangman`; change it before creating the Render service if you prefer a different available `onrender.com` URL.

Render will use:

| Setting | Value |
| --- | --- |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn --bind 0.0.0.0:$PORT --workers 1 server:app` |
| Health-check path | `/` |
| Environment variables | None required |

The single Gunicorn worker is intentional. Active games are stored only in this application's memory; multiple workers would have separate memory and could receive different requests for the same game, causing inconsistent or missing game state. A single worker keeps every request for this small assignment application in one process. Server restarts still clear active games.

To deploy, create a Render **Web Service**, connect the `main` branch of this repository, review the generated settings, choose the final service name/region/plan, and create the service. Do not commit credentials or add secrets for this application.

## Reference materials

- `Specification.md` is the original, broader specification.
- `TODO.md` narrows the work to this assignment.
- `cursor_transcript.md` is instructor guidance only; this project uses an independent implementation.
