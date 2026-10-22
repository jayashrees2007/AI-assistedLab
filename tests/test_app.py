import tempfile
import unittest
from pathlib import Path

from app.database import add_student, get_students, initialize_database
from app.models import Student


class StudentModelTests(unittest.TestCase):
    def test_calculates_average_and_grade(self):
        student = Student("Avery", (90, 90, 90, 90, 90))
        self.assertEqual(student.average, 90)
        self.assertEqual(student.grade, "A")

    def test_rejects_invalid_mark(self):
        with self.assertRaises(ValueError):
            Student("Avery", (90, 90, 90, 90, 101))

    def test_rejects_wrong_number_of_marks(self):
        with self.assertRaises(ValueError):
            Student("Avery", (90, 90))


class StudentDatabaseTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "test.db"
        initialize_database(self.database_path)

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_saves_and_loads_student_marks(self):
        student = Student("Jordan", (100, 80, 70, 60, 50))

        student_id = add_student(student, self.database_path)
        records = get_students(self.database_path)

        self.assertEqual(student_id, 1)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].student, student)
        self.assertEqual(records[0].student.average, 72)
        self.assertEqual(records[0].student.grade, "C")

    def test_empty_database_has_no_students(self):
        self.assertEqual(get_students(self.database_path), [])


if __name__ == "__main__":
    unittest.main()
