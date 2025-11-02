#!/usr/bin/env python3
"""
A simple command-line todo list application that stores tasks in JSON format.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, TypedDict

class Task(TypedDict):
    """Type definition for a task."""
    id: int
    title: str
    description: str
    created_at: str
    completed: bool

# Constants
TASKS_FILE = "tasks.json"

def load_tasks() -> List[Task]:
    """Load tasks from JSON file. Create empty file if it doesn't exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks: List[Task]) -> None:
    """Save tasks to JSON file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(title: str, description: str = "") -> None:
    """Add a new task to the list."""
    tasks = load_tasks()
    new_task = {
        "id": len(tasks) + 1,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task: {title}")

def list_tasks() -> None:
    """Display all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    print("\nTODO LIST:")
    print("-" * 50)
    for task in tasks:
        status = "✓" if task["completed"] else " "
        print(f"[{status}] {task['id']}. {task['title']}")
        if task["description"]:
            print(f"   {task['description']}")
    print("-" * 50)

def find_task_by_id(tasks: List[Task], task_id: int) -> Optional[Task]:
    """Find a task by its ID."""
    return next((task for task in tasks if task["id"] == task_id), None)

def mark_complete(task_id: int) -> bool:
    """Mark a task as complete.
    
    Args:
        task_id: The ID of the task to mark as complete.
        
    Returns:
        bool: True if the task was marked complete, False if the task was not found.
        
    Raises:
        ValueError: If task_id is negative.
    """
    if task_id < 1:
        raise ValueError("Task ID must be a positive integer")
        
    tasks = load_tasks()
    task = find_task_by_id(tasks, task_id)
    
    if task is None:
        print(f"Error: Task with ID {task_id} not found")
        return False
        
    if task["completed"]:
        print(f"Task {task_id} is already marked as complete")
        return True
        
    task["completed"] = True
    save_tasks(tasks)
    print(f"Marked task {task_id} as complete")
    return True

def main():
    """Main function to handle CLI commands."""
    parser = argparse.ArgumentParser(description="Simple TODO list application")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Add task command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument("-d", "--description", help="Task description", default="")
    
    # List tasks command
    subparsers.add_parser("list", help="List all tasks")
    
    # Complete task command
    complete_parser = subparsers.add_parser("complete", help="Mark a task as complete")
    complete_parser.add_argument("task_id", type=int, help="ID of the task to mark as complete")
    
    args = parser.parse_args()
    
    if args.command == "add":
        add_task(args.title, args.description)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        mark_complete(args.task_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()