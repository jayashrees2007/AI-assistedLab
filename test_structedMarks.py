import unittest
from unittest.mock import patch

from structedMarks import grade_for, read_mark


class GradeBoundaryTests(unittest.TestCase):
    def test_grade_boundaries(self):
        cases = [
            (0, "F"),
            (59.99, "F"),
            (60, "D"),
            (69.99, "D"),
            (70, "C"),
            (79.99, "C"),
            (80, "B"),
            (89.99, "B"),
            (90, "A"),
            (100, "A"),
        ]
        for mark, expected_grade in cases:
            with self.subTest(mark=mark):
                self.assertEqual(grade_for(mark), expected_grade)

    def test_grade_rejects_marks_outside_range(self):
        for mark in (-1, 100.01):
            with self.subTest(mark=mark):
                with self.assertRaises(ValueError):
                    grade_for(mark)


class MarkInputTests(unittest.TestCase):
    @patch("builtins.input", side_effect=["not a mark", "-3", "101", "75"])
    @patch("builtins.print")
    def test_retries_invalid_input_until_mark_is_valid(self, _print, _input):
        self.assertEqual(read_mark(1), 75)


if __name__ == "__main__":
    unittest.main()
