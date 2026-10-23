# Student Task Manager

A small FastAPI service for creating, listing, updating, and deleting student tasks. Tasks are stored in a local SQLite database.

## Create and activate the environment (Windows PowerShell)

From this project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, run the environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run and inspect

```powershell
Get-ChildItem -Recurse
Get-Content .\app\main.py
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API interactively. The database file, `student_tasks.db`, is created in this folder on first startup.

## Run tests

```powershell
python -m pytest
```

## API endpoints

- `GET /tasks` — list tasks
- `POST /tasks` — create a task (`title`, `student_name`, optional `description`)
- `PATCH /tasks/{task_id}` — update supplied task fields
- `DELETE /tasks/{task_id}` — delete a task
