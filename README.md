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

## Reference materials

- `Specification.md` is the original, broader specification.
- `TODO.md` narrows the work to this assignment.
- `cursor_transcript.md` is instructor guidance only; this project will use an independent implementation.
