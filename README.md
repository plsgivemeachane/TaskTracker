# TaskTracker CLI

## Overview

__This is a project of https://roadmap.sh/projects/task-tracker__

TaskTracker is a simple, command-line task management tool that helps you organize and track your tasks efficiently.

## Prerequisites
- Python 3.7+
- Rich library (`pip install rich`)

## Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install rich
```

## Usage

### Available Commands

#### Add a Task
```bash
python task-cli.py add "Task name"
```
Adds a new task to your todo list.

#### List Tasks
```bash
python task-cli.py list
# Optional: Filter by status
python task-cli.py list todo
python task-cli.py list "in progress"
python task-cli.py list done
```
Lists all tasks or tasks with a specific status.

#### Update a Task
```bash
python task-cli.py update <task_id> "New task description"
```
Updates the description of an existing task.

#### Delete a Task
```bash
python task-cli.py delete <task_id>
```
Removes a task from the list.

#### Mark Task Status
```bash
python task-cli.py mark <task_id> <status>
```
Change the status of a task (todo/in progress/done).

#### Help
```bash
python task-cli.py help
# Get help for a specific command
python task-cli.py help add
```
Display available commands or detailed help for a specific command.