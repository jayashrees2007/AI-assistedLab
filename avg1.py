"""Calculate the arithmetic mean of a list of marks."""

from typing import List, Union


def calculate_average(marks: List[Union[int, float]]) -> float:
    """Return the mean of marks, rejecting empty lists and invalid marks.

    Raises:
        ValueError: If the list is empty or a mark is outside 0–100.
        TypeError: If a mark is not an integer or float (booleans excluded).
    """
    if not marks:
        raise ValueError("marks must not be empty")

    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise TypeError("each mark must be a number")
        if not 0 <= mark <= 100:
            raise ValueError("each mark must be between 0 and 100")

    # Iterate over the input without sorting, removing, or otherwise changing it.
    return sum(marks) / len(marks)