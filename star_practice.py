"""STAR practice: sample behavioral-interview answers and a small practice CLI.

Python standard library only. Usage:
    python3 star_practice.py list
    python3 star_practice.py quiz <profession>
    python3 star_practice.py show <profession> <n>
    python3 star_practice.py validate
"""
import json
import random
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
FIELDS = ("id", "category", "question", "situation", "task", "action", "result")
STAR_FIELDS = ("situation", "task", "action", "result")


def list_professions(data_dir=DATA_DIR):
    """Return the profession slugs found in data_dir, sorted."""
    return sorted(p.stem for p in Path(data_dir).glob("*.json"))


def load_profession(slug, data_dir=DATA_DIR):
    """Load one profession file: returns {'profession': str, 'answers': list}."""
    path = Path(data_dir) / (slug + ".json")
    if not path.is_file():
        raise FileNotFoundError("unknown profession: " + slug)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_all(data_dir=DATA_DIR):
    """Load every profession: returns {slug: data}."""
    return {slug: load_profession(slug, data_dir) for slug in list_professions(data_dir)}


def validate_answers(data, label="data"):
    """Return a list of problems in one loaded profession file (empty if fine)."""
    problems = []
    if not isinstance(data, dict):
        return [label + ": top level must be an object"]
    answers = data.get("answers")
    if not isinstance(answers, list) or not answers:
        return [label + ": 'answers' must be a non-empty list"]
    for i, answer in enumerate(answers, 1):
        where = "%s answer %d" % (label, i)
        if not isinstance(answer, dict):
            problems.append(where + ": not an object")
            continue
        for field in FIELDS:
            if field not in answer:
                problems.append("%s: missing field '%s'" % (where, field))
            elif field == "id":
                if not isinstance(answer[field], int) or isinstance(answer[field], bool):
                    problems.append(where + ": 'id' must be an integer")
            elif not isinstance(answer[field], str) or not answer[field].strip():
                problems.append("%s: field '%s' must be a non-empty string" % (where, field))
    return problems


def validate_all(data_dir=DATA_DIR):
    """Validate every file in data_dir; return the list of problems."""
    slugs = list_professions(data_dir)
    if not slugs:
        return ["no data files found in " + str(data_dir)]
    problems = []
    for slug in slugs:
        try:
            data = load_profession(slug, data_dir)
        except (OSError, ValueError) as exc:
            problems.append("%s: cannot load (%s)" % (slug, exc))
            continue
        problems.extend(validate_answers(data, slug))
    return problems


def format_answer(answer):
    """Return the S/T/A/R text of one answer."""
    lines = ["[%s] %s" % (answer["category"], answer["question"]), ""]
    for field in STAR_FIELDS:
        lines.append("%s: %s" % (field.capitalize(), answer[field]))
        lines.append("")
    return "\n".join(lines).rstrip()


def get_answer(data, n):
    """Return the n-th answer (1-based) of a loaded profession."""
    answers = data["answers"]
    if not 1 <= n <= len(answers):
        raise IndexError("n must be between 1 and %d" % len(answers))
    return answers[n - 1]


def cmd_list(out=print):
    for slug, data in load_all().items():
        out("%s: %d questions" % (slug, len(data["answers"])))
    return 0


def cmd_show(slug, n, out=print):
    try:
        out(format_answer(get_answer(load_profession(slug), int(n))))
    except (FileNotFoundError, IndexError, ValueError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    return 0


def cmd_quiz(slug, out=print, wait=input, rng=random):
    try:
        data = load_profession(slug)
    except FileNotFoundError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    answer = rng.choice(data["answers"])
    out("[%s] %s" % (answer["category"], answer["question"]))
    wait("\nThink through your STAR answer, then press Enter to see the sample... ")
    out("")
    out(format_answer(answer))
    return 0


def cmd_validate(out=print):
    problems = validate_all()
    if problems:
        for p in problems:
            out("PROBLEM: " + p)
        return 1
    out("OK: all data files are valid")
    return 0


USAGE = "usage: star_practice.py list | quiz <profession> | show <profession> <n> | validate"


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print(USAGE, file=sys.stderr)
        return 2
    cmd = args[0]
    if cmd == "list" and len(args) == 1:
        return cmd_list()
    if cmd == "quiz" and len(args) == 2:
        return cmd_quiz(args[1])
    if cmd == "show" and len(args) == 3:
        return cmd_show(args[1], args[2])
    if cmd == "validate" and len(args) == 1:
        return cmd_validate()
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
