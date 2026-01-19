# tests/test_todo_app.py

import pytest
from src.todo_app import TodoApp, Task, TaskNotFoundError
from pathlib import Path


# ============================================================================
# 1. BASIC ASSERTIONS TESTS
# ============================================================================

class TestBasicAssertions:
    """Tests demonstrating basic pytest assertions."""
    
    @pytest.mark.critical
    def test_add_task_basic(self, todo_app):
        """Test basic task addition and assertion."""
        task = todo_app.add_task("Learn pytest")
        
        assert task.title == "Learn pytest"
        assert task.done is False
        assert task.priority == 1
        assert len(todo_app.get_all_tasks()) == 1
    
    def test_task_equality(self, todo_app):
        """Test task properties and equality checks."""
        task1 = todo_app.add_task("Task A", priority=2)
        task2 = todo_app.add_task("Task B", priority=2)
        
        assert task1.title != task2.title
        assert task1.priority == task2.priority
        assert task1.created_at is not None
        assert task1.completed_at is None


# ============================================================================
# 2. EXCEPTION TESTING WITH pytest.raises
# ============================================================================

class TestExceptions:
    """Tests for exception handling."""
    
    def test_add_empty_task(self, todo_app):
        """Test that empty task raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            todo_app.add_task("")
    
    def test_add_whitespace_only_task(self, todo_app):
        """Test that whitespace-only task raises ValueError."""
        with pytest.raises(ValueError, match="cannot be only whitespace"):
            todo_app.add_task("   ")
    
    def test_add_task_too_long(self, todo_app):
        """Test that overly long task raises ValueError."""
        long_title = "a" * 201
        with pytest.raises(ValueError, match="cannot exceed 200 characters"):
            todo_app.add_task(long_title)
    
    def test_invalid_priority(self, todo_app):
        """Test that invalid priority raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be 1, 2, or 3"):
            todo_app.add_task("Valid title", priority=5)
    
    def test_complete_nonexistent_task(self, todo_app):
        """Test that completing non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            todo_app.complete_task("Nonexistent task")
    
    def test_complete_already_completed_task(self, todo_app):
        """Test that completing already completed task raises ValueError."""
        todo_app.add_task("Task")
        todo_app.complete_task("Task")
        
        with pytest.raises(ValueError, match="already completed"):
            todo_app.complete_task("Task")
    
    def test_delete_nonexistent_task(self, todo_app):
        """Test that deleting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            todo_app.delete_task("Nonexistent task")
    
    def test_get_nonexistent_task(self, todo_app):
        """Test that getting non-existent task raises TaskNotFoundError."""
        with pytest.raises(TaskNotFoundError):
            todo_app.get_task("Nonexistent task")


# ============================================================================
# 3. FIXTURES AND PARAMETRIZATION
# ============================================================================

class TestWithFixtures:
    """Tests demonstrating fixture usage."""
    
    @pytest.mark.critical
    def test_complete_task(self, app_with_tasks):
        """Test task completion with fixture."""
        task = app_with_tasks.complete_task("Task 1")
        
        assert task.done is True
        assert task.completed_at is not None
        assert app_with_tasks.active_tasks_count() == 2
    
    def test_fixture_isolation(self, todo_app):
        """Test that fixtures are isolated between tests."""
        # Each test gets a fresh instance
        assert todo_app.active_tasks_count() == 0
        
        todo_app.add_task("Test 1")
        assert todo_app.active_tasks_count() == 1
    
    def test_mixed_status_fixture(self, app_with_mixed_status):
        """Test fixture with mixed task statuses."""
        assert app_with_mixed_status.active_tasks_count() == 1
        assert app_with_mixed_status.completed_tasks_count() == 2


# ============================================================================
# 4. PARAMETRIZATION TESTS
# ============================================================================

class TestParametrization:
    """Tests demonstrating parametrized testing."""
    
    @pytest.mark.parametrize("title,priority,expected_priority", [
        ("Low priority task", 1, 1),
        ("Medium priority task", 2, 2),
        ("High priority task", 3, 3),
    ])
    def test_add_task_with_different_priorities(
        self, todo_app, title, priority, expected_priority
    ):
        """Parametrized test for task addition with different priorities."""
        task = todo_app.add_task(title, priority=priority)
        
        assert task.priority == expected_priority
        assert task.title == title
    
    @pytest.mark.parametrize("invalid_title", [
        "",
        "   ",
        "\t\n",
    ])
    def test_invalid_task_titles(self, todo_app, invalid_title):
        """Parametrized test for invalid task titles."""
        with pytest.raises(ValueError):
            todo_app.add_task(invalid_title)
    
    @pytest.mark.parametrize("priority", [0, 4, 5, -1])
    def test_invalid_priorities(self, todo_app, priority):
        """Parametrized test for invalid priorities."""
        with pytest.raises(ValueError):
            todo_app.add_task("Task", priority=priority)


# ============================================================================
# 5. FILTERING TESTS WITH MARKERS
# ============================================================================

class TestMarkers:
    """Tests demonstrating pytest markers."""
    
    @pytest.mark.critical
    def test_persistence_across_instances(self, todo_app):
        """Critical test: verify data persists across instances."""
        todo_app.add_task("Persistent task")
        
        # Create new app instance with same storage
        new_app = TodoApp(todo_app.storage)
        
        assert new_app.active_tasks_count() == 1
        assert new_app.get_task("Persistent task").title == "Persistent task"
    
    @pytest.mark.slow
    def test_many_tasks(self, todo_app):
        """Slow test: add many tasks."""
        for i in range(100):
            todo_app.add_task(f"Task {i}")
        
        assert todo_app.active_tasks_count() == 100
    
    @pytest.mark.integration
    def test_complete_workflow(self, todo_app):
        """Integration test: full user workflow."""
        # Add tasks
        todo_app.add_task("Task A", priority=3)
        todo_app.add_task("Task B", priority=1)
        todo_app.add_task("Task C", priority=2)
        
        assert todo_app.active_tasks_count() == 3
        
        # Complete some tasks
        todo_app.complete_task("Task A")
        todo_app.complete_task("Task B")
        
        assert todo_app.active_tasks_count() == 1
        assert todo_app.completed_tasks_count() == 2
        
        # Delete a task
        todo_app.delete_task("Task C")
        
        assert len(todo_app.get_all_tasks()) == 2


# ============================================================================
# 6. COMPLEX ASSERTIONS AND COMPARISONS
# ============================================================================

class TestComplexAssertions:
    """Tests demonstrating complex assertions."""
    
    def test_task_in_list(self, app_with_tasks):
        """Test checking if task exists in list."""
        tasks = app_with_tasks.get_all_tasks()
        titles = [t.title for t in tasks]
        
        assert "Task 1" in titles
        assert "Task 2" in titles
        assert "Nonexistent" not in titles
    
    def test_list_length_and_content(self, app_with_tasks):
        """Test list length and content assertions."""
        tasks = app_with_tasks.get_all_tasks()
        
        assert len(tasks) == 3
        assert len(tasks) >= 2
        assert len(tasks) <= 5
    
    def test_task_attributes_multiple_assertions(self, todo_app):
        """Test multiple task attributes."""
        task = todo_app.add_task("Complex task", priority=3)
        
        # Multiple related assertions
        assert task.title == "Complex task"
        assert task.priority == 3
        assert task.done is False
        assert task.created_at is not None
        assert task.completed_at is None
    
    def test_task_string_representation(self, todo_app):
        """Test task can be properly converted to dict."""
        task = todo_app.add_task("Test task", priority=2)
        
        # Verify task has necessary attributes
        assert hasattr(task, 'title')
        assert hasattr(task, 'done')
        assert hasattr(task, 'priority')
        assert hasattr(task, 'created_at')
        assert hasattr(task, 'completed_at')


# ============================================================================
# 7. TESTING WITH CUSTOM ASSERTIONS
# ============================================================================

class TestCustomAssertions:
    """Tests demonstrating custom assertion patterns."""
    
    def test_high_priority_filtering(self, app_with_tasks):
        """Test filtering high-priority tasks."""
        high_priority = app_with_tasks.get_high_priority_tasks()
        
        # Custom assertion: verify all returned tasks are high-priority
        assert all(task.priority == 3 for task in high_priority), \
            "All tasks should be priority 3"
        assert len(high_priority) == 1
    
    def test_priority_filtering(self, app_with_tasks):
        """Test filtering tasks by specific priority."""
        for priority in [1, 2, 3]:
            tasks = app_with_tasks.get_tasks_by_priority(priority)
            assert all(t.priority == priority for t in tasks), \
                f"All tasks should have priority {priority}"
    
    def test_all_tasks_have_creation_date(self, app_with_tasks):
        """Custom assertion: all tasks should have creation date."""
        tasks = app_with_tasks.get_all_tasks()
        
        assert all(task.created_at for task in tasks), \
            "All tasks must have creation timestamp"


# ============================================================================
# 8. TESTING EDGE CASES
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_add_task_with_special_characters(self, todo_app):
        """Test task with special characters."""
        special_titles = [
            "Task with émojis 🎉",
            "Task with \"quotes\"",
            "Task with 'apostrophes'",
            "Task with\nnewline",
            "Task with\ttab",
        ]
        
        for title in special_titles:
            task = todo_app.add_task(title)
            assert task.title == title
    
    def test_task_with_max_length_title(self, todo_app):
        """Test task with maximum allowed title length."""
        max_length_title = "a" * 200
        task = todo_app.add_task(max_length_title)
        
        assert len(task.title) == 200
        assert task.title == max_length_title
    
    def test_complete_and_delete_same_task(self, todo_app):
        """Test edge case: delete a task and verify it's gone."""
        todo_app.add_task("Test task")
        todo_app.delete_task("Test task")
        
        with pytest.raises(TaskNotFoundError):
            todo_app.get_task("Test task")
    
    def test_storage_directory_creation(self, tmp_path):
        """Test that storage directory is created if it doesn't exist."""
        nested_path = tmp_path / "deep" / "nested" / "path" / "tasks.json"
        app = TodoApp(nested_path)
        
        # Should not raise exception and file should exist
        app.add_task("Test")
        assert nested_path.exists()


# ============================================================================
# 9. TESTING STATE AND MUTATIONS
# ============================================================================

class TestStateMutations:
    """Tests for state changes and mutations."""
    
    def test_task_count_progression(self, todo_app):
        """Test task count changes with each operation."""
        assert todo_app.active_tasks_count() == 0
        
        todo_app.add_task("Task 1")
        assert todo_app.active_tasks_count() == 1
        
        todo_app.add_task("Task 2")
        assert todo_app.active_tasks_count() == 2
        
        todo_app.complete_task("Task 1")
        assert todo_app.active_tasks_count() == 1
        assert todo_app.completed_tasks_count() == 1
    
    def test_completion_timestamp(self, todo_app):
        """Test that completion timestamp is set correctly."""
        todo_app.add_task("Task")
        task = todo_app.get_task("Task")
        
        assert task.completed_at is None
        
        todo_app.complete_task("Task")
        task = todo_app.get_task("Task")
        
        assert task.completed_at is not None


# ============================================================================
# 10. TESTING WITH SESSION FIXTURES
# ============================================================================

class TestSessionFixtures:
    """Tests using session-level fixtures."""
    
    def test_session_info_available(self, session_info):
        """Test that session info is available."""
        assert session_info["test_suite"] == "TODO App Test Suite"
        assert "version" in session_info
        assert "author" in session_info


# ============================================================================
# 11. COMBINED OPERATIONS
# ============================================================================

class TestCombinedOperations:
    """Tests combining multiple operations."""
    
    def test_multiple_operations_sequence(self, todo_app):
        """Test a sequence of different operations."""
        # Add multiple tasks
        titles = ["Buy groceries", "Write report", "Exercise", "Read book"]
        for title in titles:
            todo_app.add_task(title, priority=2)
        
        # Verify all added
        assert len(todo_app.get_all_tasks()) == 4
        
        # Complete some
        todo_app.complete_task("Buy groceries")
        todo_app.complete_task("Exercise")
        
        # Verify state
        assert todo_app.completed_tasks_count() == 2
        assert todo_app.active_tasks_count() == 2
        
        # Delete one
        todo_app.delete_task("Read book")
        
        # Final verification
        assert len(todo_app.get_all_tasks()) == 3
        
        tasks = todo_app.get_all_tasks()
        titles_remaining = [t.title for t in tasks]
        assert "Buy groceries" in titles_remaining  # completed but still exists
        assert "Read book" not in titles_remaining  # deleted
