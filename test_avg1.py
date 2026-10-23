import unittest

from avg1 import calculate_average


class CalculateAverageTests(unittest.TestCase):
    def test_normal_marks(self):
        self.assertEqual(calculate_average([70, 80, 90]), 80)

    def test_boundary_marks(self):
        self.assertEqual(calculate_average([0, 100]), 50)
        self.assertEqual(calculate_average([0]), 0)
        self.assertEqual(calculate_average([100]), 100)

    def test_does_not_change_original_list(self):
        marks = [100, 0, 50]
        original = marks.copy()

        calculate_average(marks)

        self.assertEqual(marks, original)

    def test_rejects_empty_list(self):
        with self.assertRaises(ValueError):
            calculate_average([])

    def test_rejects_marks_below_zero_or_above_100(self):
        for marks in ([-0.01], [100.01], [float("nan")], [float("inf")]):
            with self.subTest(marks=marks):
                with self.assertRaises(ValueError):
                    calculate_average(marks)

    def test_rejects_non_numeric_marks(self):
        for marks in (["75"], [None], [True]):
            with self.subTest(marks=marks):
                with self.assertRaises(TypeError):
                    calculate_average(marks)


if __name__ == "__main__":
    unittest.main()
