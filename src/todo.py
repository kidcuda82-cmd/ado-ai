#!/usr/bin/env python3
"""
A simple command-line todo list application that stores tasks in JSON format.
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, List

# Constants
TASKS_FILE = "tasks.json"

def load_tasks() -> List[Dict]:
    """Load tasks from JSON file. Create empty file if it doesn't exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks: List[Dict]) -> None:
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

def mark_complete(task_id: int) -> None:
    """Mark a task as complete."""
    tasks = load_tasks()
    # Bug: No validation for task_id existence
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Marked task {task_id} as complete")
            return
    # Silent failure - no error message if task not found

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