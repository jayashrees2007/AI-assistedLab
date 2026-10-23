"""SQLite persistence for student marks."""

import sqlite3
from pathlib import Path
from typing import List, Union

from app.models import Student, StudentRecord


DatabasePath = Union[str, Path]
DEFAULT_DATABASE = Path("student_marks.db")


def _connect(database_path: DatabasePath):
    connection = sqlite3.connect(str(database_path))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: DatabasePath = DEFAULT_DATABASE):
    """Create the student and subject-mark tables if they do not exist."""
    with _connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS marks (
                student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                subject_number INTEGER NOT NULL,
                mark REAL NOT NULL CHECK (mark >= 0 AND mark <= 100),
                PRIMARY KEY (student_id, subject_number)
            )
            """
        )


def add_student(
    student: Student, database_path: DatabasePath = DEFAULT_DATABASE
) -> int:
    """Save a student and their marks, returning the new student ID."""
    with _connect(database_path) as connection:
        cursor = connection.execute(
            "INSERT INTO students (name) VALUES (?)", (student.name.strip(),)
        )
        student_id = cursor.lastrowid
        connection.executemany(
            "INSERT INTO marks (student_id, subject_number, mark) VALUES (?, ?, ?)",
            [
                (student_id, subject_number, mark)
                for subject_number, mark in enumerate(student.marks, start=1)
            ],
        )
    return student_id


def get_students(database_path: DatabasePath = DEFAULT_DATABASE) -> List[StudentRecord]:
    """Return saved students in insertion order with all their subject marks."""
    with _connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT students.id, students.name, marks.subject_number, marks.mark
            FROM students
            JOIN marks ON marks.student_id = students.id
            ORDER BY students.id, marks.subject_number
            """
        ).fetchall()

    records = []
    current_id = None
    current_name = None
    current_marks = []
    for student_id, name, _subject_number, mark in rows:
        if current_id is not None and student_id != current_id:
            records.append(
                StudentRecord(current_id, Student(current_name, tuple(current_marks)))
            )
            current_marks = []
        current_id = student_id
        current_name = name
        current_marks.append(mark)

    if current_id is not None:
        records.append(
            StudentRecord(current_id, Student(current_name, tuple(current_marks)))
        )
    return records
