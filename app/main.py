"""Command-line interface for recording and reporting student marks."""

from app.database import add_student, get_students, initialize_database
from app.models import SUBJECT_COUNT, Student


def _read_mark(subject_number):
    while True:
        raw_mark = input(f"Mark for subject {subject_number} (0-100): ")
        try:
            mark = float(raw_mark)
        except ValueError:
            print("Enter a numeric mark between 0 and 100.")
            continue
        if 0 <= mark <= 100:
            return mark
        print("Mark must be between 0 and 100.")


def _add_student():
    name = input("Student name: ").strip()
    while not name:
        print("Student name must not be empty.")
        name = input("Student name: ").strip()

    marks = tuple(_read_mark(number) for number in range(1, SUBJECT_COUNT + 1))
    student = Student(name, marks)
    student_id = add_student(student)
    print(f"Saved {student.name} (ID {student_id}), average {student.average:.2f}, "
          f"grade {student.grade}.")


def _print_report():
    students = get_students()
    if not students:
        print("No student records yet.")
        return

    print("\nStudent Marks Report")
    print(f"{'ID':>4}  {'Name':<24} {'Marks':<29} {'Average':>8} {'Grade':>5}")
    print("-" * 77)
    for record in students:
        student = record.student
        marks = ", ".join(f"{mark:g}" for mark in student.marks)
        print(
            f"{record.id:>4}  {student.name:<24} {marks:<29} "
            f"{student.average:>8.2f} {student.grade:>5}"
        )


def main():
    initialize_database()
    while True:
        print("\nStudent Marks")
        print("1. Add student")
        print("2. View report")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            _add_student()
        elif choice == "2":
            _print_report()
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
