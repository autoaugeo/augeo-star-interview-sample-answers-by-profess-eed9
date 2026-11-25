import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import star_practice as sp  # noqa: E402


def good_answer(i=1):
    return {"id": i, "category": "c", "question": "q", "situation": "s",
            "task": "t", "action": "a", "result": "r"}


class LoadTests(unittest.TestCase):
    def test_professions_listed(self):
        self.assertEqual(sp.list_professions(),
                         ["cdl-driver", "nurse", "retail-manager", "teacher"])

    def test_load_each_has_five_answers(self):
        for slug, data in sp.load_all().items():
            self.assertEqual(len(data["answers"]), 5, slug)

    def test_unknown_profession(self):
        with self.assertRaises(FileNotFoundError):
            sp.load_profession("astronaut")

    def test_get_answer_bounds(self):
        data = sp.load_profession("nurse")
        self.assertEqual(sp.get_answer(data, 1)["id"], data["answers"][0]["id"])
        with self.assertRaises(IndexError):
            sp.get_answer(data, 0)
        with self.assertRaises(IndexError):
            sp.get_answer(data, 6)

    def test_format_answer_has_star_parts(self):
        text = sp.format_answer(good_answer())
        for label in ("Situation:", "Task:", "Action:", "Result:"):
            self.assertIn(label, text)


class ValidateTests(unittest.TestCase):
    def test_shipped_data_is_valid(self):
        self.assertEqual(sp.validate_all(), [])

    def test_good_answer_passes(self):
        self.assertEqual(sp.validate_answers({"answers": [good_answer()]}), [])

    def test_missing_field_reported(self):
        bad = good_answer()
        del bad["result"]
        problems = sp.validate_answers({"answers": [bad]})
        self.assertEqual(len(problems), 1)
        self.assertIn("result", problems[0])

    def test_empty_string_reported(self):
        bad = good_answer()
        bad["action"] = "   "
        self.assertEqual(len(sp.validate_answers({"answers": [bad]})), 1)

    def test_empty_list_reported(self):
        self.assertTrue(sp.validate_answers({"answers": []}))

    def test_validate_all_on_temp_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(sp.validate_all(tmp))
            bad = good_answer()
            bad["task"] = ""
            Path(tmp, "x.json").write_text(json.dumps({"answers": [bad]}), encoding="utf-8")
            self.assertEqual(len(sp.validate_all(tmp)), 1)

    def test_validate_command_exit_code(self):
        self.assertEqual(sp.cmd_validate(out=lambda s: None), 0)


if __name__ == "__main__":
    unittest.main()
