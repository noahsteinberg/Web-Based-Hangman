# Web-Based Hangman — Assignment Plan

This plan covers only the reduced assignment: a Python game engine, Flask REST API, and browser client. `terminal_client.py`, bots, evaluation, scoring, leaderboard, logging/replay, and multiplayer from `Specification.md` are out of scope. Work one phase at a time; check an item only after its stated verification succeeds.

## Phase 1 — Setup, scope, and Git

- [x] Review `Specification.md`, this plan, and `cursor_transcript.md` for guidance only; do not copy the instructor implementation.
- [x] Create the application structure and a Python virtual environment; add `.gitignore` before installing packages or adding local artifacts.
- [x] Initialize a Git repository, create a GitHub repository, and make an initial commit containing the provided `Specification.md` and revised `TODO.md`.
- [x] Verify the project can be cloned cleanly and that no secrets, virtual-environment files, or generated files are staged; commit after verification.

## Phase 2 — Game engine and word lists

- [x] Add `words/easy.txt`, `words/medium.txt`, and `words/hard.txt` with alphabetic words appropriate to Easy, Medium, and Hard; record their source/counts in `README.md`.
- [x] Implement an interface-independent engine in `game.py` and word loading/selection in `word_manager.py`.
- [x] Support random selection by difficulty; single-letter validation; duplicate handling; correct/incorrect guesses; pattern, remaining incorrect guesses, and `playing`/`won`/`lost` status.
- [x] Prevent guesses after a completed game and expose the answer only after completion. Keep the hidden word out of active client-safe state.
- [x] Add and run engine/word tests in `tests/test_game.py` and `tests/test_word_manager.py`: all difficulties, valid/correct/incorrect/repeated/invalid guesses, win, loss, and word-list validation.
- [x] Review the test results and engine behavior; commit only after they pass.

## Phase 3 — Flask API

- [x] Implement `server.py` using Flask with in-memory, separate game states and unique IDs.
- [x] Implement JSON endpoints: `POST /api/games`, `GET /api/games/<game_id>`, and `POST /api/games/<game_id>/guess`.
- [x] Validate JSON bodies, difficulty, guesses, and unknown IDs; return appropriate status codes and consistent JSON errors/state.
- [x] Ensure active responses never disclose the word and the API, not the browser, decides game outcomes.
- [x] Add and run `tests/test_api.py` for the three difficulty levels, multiple games, correct/incorrect/repeated/invalid guesses, win/loss, malformed requests, missing IDs, and hidden-word protection.
- [x] Manually exercise the API locally and inspect representative JSON; commit only after tests and manual checks pass.

## Phase 4 — Browser interface

- [x] Add `static/index.html`, `static/style.css`, and `static/app.js`, served by `server.py`.
- [x] Build a simple interface with a difficulty selector, New Game/restart flow, word pattern, guessed letters, remaining guesses, end message, and a hangman drawing that changes after wrong guesses.
- [x] Support on-screen letter buttons and keyboard input; disable already guessed letters and prevent input once a game ends.
- [x] Use `fetch()` exclusively for game actions; do not store or derive the hidden word in browser JavaScript.
- [x] Check locally in Chrome: start each difficulty, make correct/incorrect/repeated guesses, complete a win and a loss, and start another game without reloading.
- [x] In Chrome DevTools Network, inspect a guess request and its JSON response, then confirm the page updates from that response; commit only after these checks pass.

## Phase 5 — Complete testing and documentation

- [ ] Run the full automated test suite and fix failures; repeat the local browser checks after fixes.
- [ ] Update `README.md` with setup, local run/test commands, browser use, API examples, project structure, and known limitations.
- [ ] Verify a fresh local setup from the README and confirm that the UI/API behavior meets every reduced assignment requirement; commit the verified result.

## Phase 6 — GitHub, Render, and public verification

- [ ] Push all verified commits to GitHub; confirm the repository includes code, `words/`, tests, `requirements.txt`, deployment configuration, `README.md`, `Specification.md`, and this `TODO.md`—but no credentials.
- [ ] Add deployment configuration after `server.py` is implemented and the Render start command is verified.
- [ ] Deploy the Flask application to Render with a production start command matching `server.py` (for example, Gunicorn); configure Render only through its dashboard/repository integration and do not commit secrets.
- [ ] Verify the public HTTPS URL serves the browser UI and the required API endpoints.
- [ ] Play a complete win or loss on the public site, start another game, and confirm the deployed app works independently of the local server; commit deployment-config/documentation changes after verification.

## Phase 7 — Submission package

- [ ] Record the GitHub repository URL and deployed application URL for HuskyCT.
- [ ] Create a 1–2 page PDF report: AI-assisted development process, engine/API/UI, testing, deployment, one challenge and resolution, reflection, and 2–3 real prompts used during this project.
- [ ] Record a 2–3 minute demo of the deployed site: start a game, make guesses, complete a game, start another game, and show one Chrome DevTools HTTP request plus JSON response.
- [ ] Recheck that the public URL is accessible and submit the repository URL, deployed URL, PDF report, and demo recording.

## Current blockers / decisions before implementation

- [x] Supply or choose original word-list content for `words/easy.txt`, `words/medium.txt`, and `words/hard.txt`; none is currently present in this project.
- [ ] Choose the GitHub repository name/visibility and create/sign in to the GitHub account if needed.
- [ ] Choose a Render account/service name and retain the public URL once created.
