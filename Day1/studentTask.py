from datetime import datetime

class Task:
    def __init__(self, task_id: int, title: str, due_date: str, description: str = "", priority: str = "Medium"):
        self.id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date  # Format: YYYY-MM-DD
        self.priority = priority  # Low, Medium, High
        self.status = "Pending"   # Pending or Completed

    def __str__(self):
        status_icon = "✓" if self.status == "Completed" else " "
        return f"[{status_icon}] ID: {self.id} | {self.title} (Due: {self.due_date}) - Priority: {self.priority}"


class TaskManager:
    def __init__(self):
        self.tasks = []
        self._next_id = 1

    # CREATE
    def create_task(self, title: str, due_date: str, description: str = "", priority: str = "Medium"):
        if not title.strip() or not due_date.strip():
            raise ValueError("Title and Due Date are mandatory.")
        
        task = Task(self._next_id, title.strip(), due_date.strip(), description.strip(), priority.strip())
        self.tasks.append(task)
        print(f"Task created successfully! (ID: {self._next_id})")
        self._next_id += 1

    # READ
    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\n--- Current Tasks ---")
        for task in self.tasks:
            print(task)
        print("-" * 21)

    # UPDATE
    def update_task(self, task_id: int, title: str = None, due_date: str = None, description: str = None, priority: str = None):
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        if title: task.title = title.strip()
        if due_date: task.due_date = due_date.strip()
        if description is not None: task.description = description.strip()
        if priority: task.priority = priority.strip()
        print(f"Task {task_id} updated successfully.")

    # STATUS TOGGLE
    def toggle_status(self, task_id: int):
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return
        
        task.status = "Completed" if task.status == "Pending" else "Pending"
        print(f"Task {task_id} status changed to: {task.status}")

    # DELETE
    def delete_task(self, task_id: int):
        task = self._find_task_by_id(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return
        
        self.tasks.remove(task)
        print(f"Task {task_id} deleted successfully.")

    def _find_task_by_id(self, task_id: int):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None


# --- Demonstration / CLI Test ---
if __name__ == "__main__":
    manager = TaskManager()

    # 1. Create Tasks
    manager.create_task("Finish Math Assignment", "2026-10-25", "Complete exercises 1 to 10", "High")
    manager.create_task("Read Computer Architecture Chapter", "2026-10-28", priority="Medium")

    # 2. Read / List Tasks
    manager.list_tasks()

    # 3. Toggle Status (Complete a task)
    manager.toggle_status(1)
    manager.list_tasks()

    # 4. Update Task
    manager.update_task(2, priority="High", description="Focus on cache optimization slides")
    manager.list_tasks()

    # 5. Delete Task
    manager.delete_task(1)
    manager.list_tasks()