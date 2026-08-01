"""Regression tests for the phonetic tools.

SKILL.md instructs the agent to trust these tools' output over its own ear —
so their output is a contract. These tests lock the values the skill relies on.
Stdlib only (unittest + subprocess); run with:

    python3 -m unittest discover -s tests -v
"""

import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BIN = REPO / "bin"


def run(tool, *args):
    result = subprocess.run(
        ["python3", str(BIN / tool), *args],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


class TestScan(unittest.TestCase):
    def test_syllable_count(self):
        out = run("scan", "hello world")
        self.assertIn("3σ", out)
        self.assertIn("u s s", out)


class TestRhyme(unittest.TestCase):
    def test_perfect_pair_against_line(self):
        # curiosity-vs-approval axis: the payoff must ring perfect.
        out = run("rhyme", "grade", "--against", "You let the room decide what you made")
        self.assertIn("perfect", out)
        self.assertIn("1.0", out)

    def test_thesis_pair_is_perfect(self):
        out = run("rhyme", "stayed", "--against", "in the glass, looking up, afraid")
        self.assertIn("perfect", out)
        self.assertIn("1.0", out)

    def test_courage_does_not_rhyme_with_safe_pattern(self):
        # "dared" deliberately refuses the grade/made pattern — a distant match.
        out = run("rhyme", "dared", "--against", "You trade the map for a grade")
        self.assertIn("distant", out)


if __name__ == "__main__":
    unittest.main()
