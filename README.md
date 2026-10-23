# Student Marks App

A command-line application that records five subject marks for each student,
calculates their average and grade, and stores records in a local SQLite database.
It uses only the Python standard library.

## Run

From the project root, start the program with:

```powershell
py -3 -m app.main
```

Choose **Add student** to enter a name and five marks (each from 0 to 100), or
**View report** to see all saved student records. The database file
`student_marks.db` is created in the current working directory.

Grade boundaries are based on the average:

| Grade | Average |
| --- | --- |
| A | 90–100 |
| B | 80–under 90 |
| C | 70–under 80 |
| D | 60–under 70 |
| F | under 60 |

## Tests

Run the tests from the project root:

```powershell
py -3 -m unittest discover -s tests -v
```
