"""Collect marks for five students and print their grades."""


def grade_for(mark):
    """Return the grade for a mark using the program's grade boundaries."""
    if not 0 <= mark <= 100:
        raise ValueError("Mark must be between 0 and 100.")

    # Grade boundaries: A >= 90, B >= 80, C >= 70, D >= 60, otherwise F.
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    return "F"


def read_mark(student_number):
    """Keep asking until a valid mark between 0 and 100 is entered."""
    while True:
        try:
            mark = float(input(f"Enter marks for student {student_number} (0-100): "))
        except ValueError:
            print("Invalid input. Enter a number between 0 and 100.")
            continue

        if 0 <= mark <= 100:
            return mark
        print("Invalid mark. Marks must be between 0 and 100.")


def main():
    students = []
    for student_number in range(1, 6):
        name = input(f"Enter name for student {student_number}: ").strip()
        if not name:
            name = f"Student {student_number}"
        students.append((name, read_mark(student_number)))

    print("\nStudent Marks Report")
    print(f"{'Student':<20}{'Mark':>8}{'Grade':>8}")
    print("-" * 36)
    for name, mark in students:
        print(f"{name:<20}{mark:>8.2f}{grade_for(mark):>8}")


if __name__ == "__main__":
    main()