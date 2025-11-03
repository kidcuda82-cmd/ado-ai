import pytest
import os
import json
from src.todo import add_task, list_tasks, mark_complete, load_tasks, TASKS_FILE

@pytest.fixture
def clean_tasks_file():
    """Fixture to ensure a clean tasks file for each test."""
    # Remove the tasks file if it exists
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)
    yield
    # Cleanup after test
    if os.path.exists(TASKS_FILE):
        os.remove(TASKS_FILE)

def test_add_task(clean_tasks_file, capsys):
    """Test adding a task."""
    # Test adding a task with title only
    add_task("Test task")
    tasks = load_tasks()
    
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test task"
    assert tasks[0]["description"] == ""
    assert not tasks[0]["completed"]
    assert tasks[0]["id"] == 1
    
    captured = capsys.readouterr()
    assert "Added task: Test task" in captured.out
    
    # Test adding a task with description
    add_task("Test task 2", "Test description")
    tasks = load_tasks()
    
    assert len(tasks) == 2
    assert tasks[1]["title"] == "Test task 2"
    assert tasks[1]["description"] == "Test description"
    assert tasks[1]["id"] == 2

def test_list_tasks(clean_tasks_file, capsys):
    """Test listing tasks."""
    # Test empty list
    list_tasks()
    captured = capsys.readouterr()
    assert "No tasks found." in captured.out
    
    # Test with tasks
    add_task("Task 1", "Description 1")
    add_task("Task 2")
    
    list_tasks()
    captured = capsys.readouterr()
    assert "Task 1" in captured.out
    assert "Description 1" in captured.out
    assert "Task 2" in captured.out
    assert "TODO LIST:" in captured.out

def test_mark_complete(clean_tasks_file, capsys):
    """Test marking tasks as complete."""
    # Add a test task
    add_task("Test task")
    
    # Test marking task as complete
    result = mark_complete(1)
    assert result is True
    tasks = load_tasks()
    assert tasks[0]["completed"] is True
    captured = capsys.readouterr()
    assert "Marked task 1 as complete" in captured.out
    
    # Test marking already completed task
    result = mark_complete(1)
    assert result is True
    captured = capsys.readouterr()
    assert "Task 1 is already marked as complete" in captured.out
    
    # Test marking non-existent task
    result = mark_complete(99)
    assert result is False
    captured = capsys.readouterr()
    assert "Error: Task with ID 99 not found" in captured.out
    
    # Test invalid task ID
    with pytest.raises(ValueError):
        mark_complete(-1)