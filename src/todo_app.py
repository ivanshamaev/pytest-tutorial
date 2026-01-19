# todo_app.py

import json
from pathlib import Path
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """Represents a task with title, completion status, and metadata."""
    title: str
    done: bool = False
    priority: int = 1  # 1 (low), 2 (medium), 3 (high)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    
    def __post_init__(self):
        if not isinstance(self.priority, int) or self.priority not in (1, 2, 3):
            raise ValueError("Priority must be 1, 2, or 3")


class TaskNotFoundError(Exception):
    """Raised when a task is not found."""
    pass


class TodoApp:
    """Simple TODO application with file-based storage."""
    
    def __init__(self, storage: Path):
        self.storage = storage
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        """Ensure storage file exists and contains valid JSON."""
        if not self.storage.exists():
            self.storage.parent.mkdir(parents=True, exist_ok=True)
            self.storage.write_text("[]")

    def _load(self) -> list[Task]:
        """Load tasks from storage file."""
        try:
            data = json.loads(self.storage.read_text())
            return [Task(**item) for item in data]
        except json.JSONDecodeError:
            return []

    def _save(self, tasks: list[Task]) -> None:
        """Save tasks to storage file."""
        self.storage.write_text(
            json.dumps([asdict(t) for t in tasks], indent=2)
        )

    def add_task(self, title: str, priority: int = 1) -> Task:
        """Add a new task to the TODO list."""
        if not title:
            raise ValueError("Task title cannot be empty")
        if not title.strip():
            raise ValueError("Task title cannot be only whitespace")
        if len(title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        tasks = self._load()
        task = Task(title=title, priority=priority)
        tasks.append(task)
        self._save(tasks)
        return task

    def complete_task(self, title: str) -> Task:
        """Mark a task as completed."""
        tasks = self._load()

        for task in tasks:
            if task.title == title:
                if task.done:
                    raise ValueError("Task is already completed")
                task.done = True
                task.completed_at = datetime.now().isoformat()
                self._save(tasks)
                return task

        raise TaskNotFoundError(f"Task '{title}' not found")
    
    def delete_task(self, title: str) -> Task:
        """Delete a task from the TODO list."""
        tasks = self._load()
        
        for i, task in enumerate(tasks):
            if task.title == title:
                deleted_task = tasks.pop(i)
                self._save(tasks)
                return deleted_task
        
        raise TaskNotFoundError(f"Task '{title}' not found")

    def get_task(self, title: str) -> Task:
        """Get a specific task by title."""
        tasks = self._load()
        
        for task in tasks:
            if task.title == title:
                return task
        
        raise TaskNotFoundError(f"Task '{title}' not found")

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks."""
        return self._load()

    def active_tasks_count(self) -> int:
        """Count active (incomplete) tasks."""
        return sum(not t.done for t in self._load())
    
    def completed_tasks_count(self) -> int:
        """Count completed tasks."""
        return sum(t.done for t in self._load())

    def get_tasks_by_priority(self, priority: int) -> list[Task]:
        """Get tasks filtered by priority level."""
        if priority not in (1, 2, 3):
            raise ValueError("Priority must be 1, 2, or 3")
        return [t for t in self._load() if t.priority == priority]

    def get_high_priority_tasks(self) -> list[Task]:
        """Get all high-priority tasks."""
        return self.get_tasks_by_priority(3)


def main():
    """Main function demonstrating the TODO app usage."""
    storage = Path("tasks.json")
    app = TodoApp(storage)

    print("=" * 50)
    print("📋 TODO Application Demo")
    print("=" * 50)
    
    # Clear previous tasks for demo
    for task in app.get_all_tasks():
        app.delete_task(task.title)

    print("\n1️⃣  Adding tasks with different priorities...")
    task1 = app.add_task("Prepare presentation for meeting", priority=3)
    print(f"   ✅ Added: {task1.title} (Priority: {task1.priority})")
    
    task2 = app.add_task("Review code changes", priority=2)
    print(f"   ✅ Added: {task2.title} (Priority: {task2.priority})")
    
    task3 = app.add_task("Write unit tests for new module", priority=3)
    print(f"   ✅ Added: {task3.title} (Priority: {task3.priority})")
    
    task4 = app.add_task("Update documentation", priority=1)
    print(f"   ✅ Added: {task4.title} (Priority: {task4.priority})")

    print(f"\n2️⃣  Current status:")
    print(f"   📊 Total tasks: {len(app.get_all_tasks())}")
    print(f"   ⏳ Active tasks: {app.active_tasks_count()}")
    print(f"   ✔️  Completed tasks: {app.completed_tasks_count()}")

    print(f"\n3️⃣  High-priority tasks:")
    for task in app.get_high_priority_tasks():
        print(f"   🔴 {task.title}")

    print(f"\n4️⃣  Completing some tasks...")
    completed = app.complete_task("Prepare presentation for meeting")
    print(f"   ✅ Completed: {completed.title}")
    
    completed = app.complete_task("Review code changes")
    print(f"   ✅ Completed: {completed.title}")

    print(f"\n5️⃣  Updated status:")
    print(f"   ⏳ Active tasks: {app.active_tasks_count()}")
    print(f"   ✔️  Completed tasks: {app.completed_tasks_count()}")

    print(f"\n6️⃣  Remaining tasks:")
    for task in app.get_all_tasks():
        status = "✔️ " if task.done else "⏳"
        print(f"   {status} {task.title}")

    print("\n" + "=" * 50)
    print("✨ Demo completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
