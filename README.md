# STAR interview sample answers

Twenty sample STAR (Situation, Task, Action, Result) answers to common behavioral interview questions, five each for four professions: registered nurse, teacher, CDL driver and retail manager. A small command-line tool lets you list them, quiz yourself and print any answer.

This project is built and maintained by an automated agent system.

## About the content

- The answers were written with AI assistance. They are fictional, educational examples of structure, length and tone. They are not the real experience of any nurse, teacher, driver or manager, and you should rebuild each one from a true story of your own.
- This is interview-preparation material only. It does not promise any hiring outcome.
- It is not affiliated with any employer, licensing body or testing organisation.

## Usage

Python 3.8 or newer, standard library only. From this folder:

```
python3 star_practice.py list
python3 star_practice.py quiz nurse
python3 star_practice.py show teacher 3
python3 star_practice.py validate
```

- `list` prints the professions and how many questions each has.
- `quiz <profession>` prints a random question, waits for Enter, then shows the Situation, Task, Action and Result.
- `show <profession> <n>` prints answer number n (1 to 5).
- `validate` checks every data file for the seven fields (id, category, question, situation, task, action, result) with non-empty text, and exits 1 on failure.

Profession names are the file names in `data/`: `nurse`, `teacher`, `cdl-driver`, `retail-manager`.

Run the tests:

```
python3 -m unittest discover -s tests
```

## Data format

Each `data/<profession>.json` holds `{"profession": "...", "answers": [...]}`. Every answer has `id`, `category`, `question`, `situation`, `task`, `action` and `result`.

## Full sets

Full 30-answer sets per profession are sold on the project site: https://augeo-star-interview-answers-by-profession-eed9.pages.dev/

## License

Code: MIT. Data files: CC BY 4.0. See `LICENSE`.
