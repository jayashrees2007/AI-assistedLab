"""Student data and grade calculations."""

from dataclasses import dataclass
from typing import Tuple


SUBJECT_COUNT = 5


@dataclass(frozen=True)
class Student:
    name: str
    marks: Tuple[float, ...]

    def __post_init__(self):
        if not self.name.strip():
            raise ValueError("Student name must not be empty.")
        if len(self.marks) != SUBJECT_COUNT:
            raise ValueError(f"A student must have exactly {SUBJECT_COUNT} marks.")
        for mark in self.marks:
            if isinstance(mark, bool) or not isinstance(mark, (int, float)):
                raise TypeError("Each mark must be a number.")
            if not 0 <= mark <= 100:
                raise ValueError("Each mark must be between 0 and 100.")

    @property
    def average(self):
        return sum(self.marks) / SUBJECT_COUNT

    @property
    def grade(self):
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"


@dataclass(frozen=True)
class StudentRecord:
    id: int
    student: Student
