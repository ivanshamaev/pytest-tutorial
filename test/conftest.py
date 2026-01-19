# tests/conftest.py

import pytest
from pathlib import Path
from src.todo_app import TodoApp


@pytest.fixture
def storage_file(tmp_path: Path) -> Path:
    """Fixture providing a temporary storage file."""
    return tmp_path / "tasks.json"


@pytest.fixture
def todo_app(storage_file: Path) -> TodoApp:
    """Fixture providing a fresh TodoApp instance with temporary storage."""
    return TodoApp(storage_file)


@pytest.fixture
def app_with_tasks(todo_app: TodoApp) -> TodoApp:
    """Fixture providing TodoApp with pre-populated tasks."""
    todo_app.add_task("Task 1", priority=1)
    todo_app.add_task("Task 2", priority=2)
    todo_app.add_task("Task 3", priority=3)
    return todo_app


@pytest.fixture
def app_with_mixed_status(app_with_tasks: TodoApp) -> TodoApp:
    """Fixture providing TodoApp with completed and active tasks."""
    app_with_tasks.complete_task("Task 1")
    app_with_tasks.complete_task("Task 2")
    return app_with_tasks


# Hooks for test collection and execution

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "critical: marks tests as critical functionality"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


@pytest.fixture(scope="session")
def session_info():
    """Session-level fixture with test session information."""
    return {
        "test_suite": "TODO App Test Suite",
        "version": "1.0",
        "author": "Test Engineer"
    }
