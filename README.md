# Python Quiz Master

A local desktop multiple-choice quiz application built with Python's standard library. It uses Tkinter/ttk for the interface and SQLite for attempt history and settings.

## Features

- Five categories and three difficulty levels, with 51 built-in questions.
- Name, category, and difficulty selection; randomized question and answer order.
- Configurable quiz length and per-question countdown timer, including a timer-off setting.
- Correct, incorrect, and unanswered scoring with percentage and performance feedback.
- Answer review with the selected answer, correct answer, and explanation.
- SQLite results history and persistent local settings.
- Light and dark themes, with confirmation before clearing history.

## Requirements and run

Requires Python 3.10 or later with Tkinter available. There are no third-party packages and no `requirements.txt` is needed.

From this project folder:

```sh
python main.py
```

The database is created automatically at `~/.python_quiz_master.sqlite3` on first launch. It contains quiz results and settings; the application does not collect network data.

## Tests

Run the standard-library unit tests without opening a GUI:

```sh
python -m unittest discover -s tests
```

## Project structure

```text
main.py                       Application launcher
python_quiz_master/
  main.py                     Tkinter screens and application flow
  database.py                 SQLite result and settings persistence
  question_bank.py            Built-in questions and categories
  quiz_engine.py              Session flow and scoring logic
tests/
  test_database.py
  test_quiz_engine.py
README.md
```

## Add questions

Edit `_RAW` in `python_quiz_master/question_bank.py`. Each entry contains a category, one of `Easy`, `Medium`, or `Hard`, a prompt, exactly four answer options, the correct option text, and an explanation. Category choices are derived from the bank automatically.

## Troubleshooting

- **Tkinter is missing:** install the operating system's Python Tk package or use a Python distribution that includes Tkinter. On some Linux distributions this is provided separately (for example, `python3-tk`).
- **The window does not open:** run `python -m tkinter` to check Tk support and use a desktop session with a display server.
- **History is unavailable:** confirm the application can write to your home directory; the SQLite file is stored there.
- **A category and difficulty has fewer questions than the configured quiz length:** the quiz uses all available questions for that selection.
