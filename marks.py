def read_mark(subject_number):
    while True:
        try:
            mark = float(input(f"Enter marks for subject {subject_number} (0-100): "))
        except ValueError:
            print("Please enter a number.")
            continue

        if 0 <= mark <= 100:
            return mark
        print("Marks must be between 0 and 100.")


def main():
    student_name = input("Enter student name: ").strip()
    if not student_name:
        student_name = "Student"

    marks = [read_mark(subject_number) for subject_number in range(1, 6)]
    total = sum(marks)
    average = total / len(marks)

    if average >= 90:
        grade = "A"
    elif average >= 80:
        grade = "B"
    elif average >= 70:
        grade = "C"
    elif average >= 60:
        grade = "D"
    else:
        grade = "F"

    result = "Pass" if all(mark >= 40 for mark in marks) else "Fail"

    print(f"\nResults for {student_name}")
    print(f"Total marks: {total:g} / 500")
    print(f"Average: {average:.2f}%")
    print(f"Grade: {grade}")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()