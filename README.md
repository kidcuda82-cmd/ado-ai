# Todo CLI Application

A simple command-line todo list application built with Python. This application allows users to manage their tasks through a CLI interface, with data persistence using JSON storage.

## Features

- Add new tasks with titles and optional descriptions
- List all tasks with their completion status
- Mark tasks as complete
- Data persistence using JSON storage
- Simple and intuitive command-line interface
- Type-safe implementation with proper error handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kidcuda82-cmd/ado-ai.git
cd ado-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The application supports the following commands:

### Add a new task
```bash
python src/todo.py add "Task title" -d "Optional task description"
```

### List all tasks
```bash
python src/todo.py list
```

### Mark a task as complete
```bash
python src/todo.py complete <task_id>
```

### Show help
```bash
python src/todo.py --help
```

## Project Structure

```
ado-ai/
├── src/
│   └── todo.py      # Main application file
├── tasks.json       # JSON storage for tasks
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## Requirements

- Python 3.7+
- Dependencies listed in requirements.txt