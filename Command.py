import sys
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime
import re
import uuid


# Predefined status values
VALID_STATUSES = ["todo", "in progress", "done"]

class ValidationError(Exception):
    """Custom exception for input validation errors."""
    pass

class CommandParser:
    def __init__(self, data) -> None:
        self.commands = {
            "add": self.add,
            "delete": self.delete,
            "list": self.list,
            "help": self.help,
            "update": self.update,
            "mark": self.mark
        }
        self.helps = {
            "add": {
                "name": "Add",
                "description": "Add a task to the todo list",
                "args": [
                    "name: <string> (1-100 characters)"
                ]
            },
            "delete": {
                "name": "Delete",
                "description": "Delete a task from the todo list",
                "args": [
                    "id: <uuid> or 'all'"
                ]
            },
            "list": {
                "name": "List",
                "description": "List all tasks",
                "args": [
                    "status (optional): todo | in progress | done"
                ]
            },
            "update": {
                "name": "Update",
                "description": "Update a task description",
                "args": [
                    "id: <uuid>",
                    "description: <string> (1-250 characters)"
                ]
            },
            "help": {
                "name": "Help",
                "description": "Show help",
                "args": [
                    "command (optional): <string>"
                ]
            }
        }
        self.args = []
        self.data = data if data else []
    
    def _sanitize_input(self, input_str, max_length=250):
        """Sanitize and validate input strings."""
        if not input_str or not isinstance(input_str, str):
            raise ValidationError("Input must be a non-empty string")
        
        # Remove leading/trailing whitespace
        sanitized = input_str.strip()
        
        # Check length
        if len(sanitized) < 1 or len(sanitized) > max_length:
            raise ValidationError(f"Input must be between 1 and {max_length} characters")
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>&\'"()]', '', sanitized)
        
        return sanitized

    def _find_task_by_id(self, task_id):
        """Find a task by its full or short ID."""
        # First try full match
        for task in self.data:
            if task['id'] == task_id:
                return task
        
        # Then try short ID match (first 8 characters)
        for task in self.data:
            if task['id'].startswith(task_id):
                return task
        
        return None

    def execute(self):
        argsLen = len(sys.argv)
        if argsLen < 2:
            print("[bold red]No commands given[/bold red]")
            self.help()
            return self.data
        
        for i in range(2, argsLen):
            self.args.append(sys.argv[i])
        
        try:
            if sys.argv[1] in self.commands:
                self.commands[sys.argv[1]]()
            else:
                print("[bold red]Command not found[/bold red]")
                self.help()
        except ValidationError as ve:
            print(f"[bold red]Validation Error: {ve}[/bold red]")
        except Exception as e:
            print(f"[bold red]An unexpected error occurred: {e}[/bold red]")
            
        return self.data
            
    def help(self):
        if len(self.args) == 0:
            print("[bold green]Commands:[/bold green]")
            for command in self.commands:
                print(f"    [bold red]{command}[/bold red]", end = " - ")
                print(f"[bold]{self.helps[command]['name']}[/bold]")
                print(f"    [dim]{self.helps[command]['description']}[/dim]")
                for commandArg in self.helps[command]["args"]:
                    print(f"        {commandArg}")
        else:
            command = self.args[0]
            if command not in self.helps:
                print("[bold red]Unknown command[/bold red]")
                return
            
            print("[bold green]Command:[/bold green]")
            print(f"    [bold red]{command}[/bold red]", end = " - ")
            print(f"[bold]{self.helps[command]['name']}[/bold]")
            print(f"    [dim]{self.helps[command]['description']}[/dim]")
            for commandArg in self.helps[command]["args"]:
                print(f"        {commandArg}")

    def add(self):
        if not self.args:
            raise ValidationError("Task name is required")
        
        task_name = self._sanitize_input(self.args[0], max_length=100)
        
        new_task = {
            "id": str(uuid.uuid4()),  # Use UUID for unique identification
            "name": task_name,
            "description": "No description",
            "status": "todo",
            "createdAt": str(datetime.now()),
            "updatedAt": str(datetime.now())
        }
        
        self.data.append(new_task)
        print(f"[bold green]Task added: {task_name}[/bold green]")
    
    def update(self):
        if len(self.args) < 2:
            raise ValidationError("Update requires task ID and new description")
        
        task_id = self.args[0]
        new_description = self._sanitize_input(self.args[1], max_length=250)
        
        task = self._find_task_by_id(task_id)
        if not task:
            raise ValidationError(f"Task with ID {task_id} not found")
        
        old_description = task['description']
        task['description'] = new_description
        task['updatedAt'] = str(datetime.now())
        
        print(f"[bold green]Task updated[/bold green] [bold red]{old_description} -> {new_description}[/bold red]")
        print(f"[dim]Task ID: {task['id']}[/dim]")

    def delete(self):
        if not self.args:
            raise ValidationError("Task ID is required for deletion")
        
        if self.args[0] == "all":
            self.data = []
            print("[bold green]All tasks deleted[/bold green]")
            return
        
        task_id = self.args[0]
        task = self._find_task_by_id(task_id)
        
        if not task:
            raise ValidationError(f"Task with ID {task_id} not found")
        
        self.data = [t for t in self.data if t['id'] != task['id']]
        print(f"[bold green]Task deleted[/bold green]")
        print(f"[dim]Deleted Task ID: {task['id']}[/dim]")

    def mark(self):
        if len(self.args) < 2:
            raise ValidationError("Marking a task requires ID and status")
        
        task_id = self.args[0]
        new_status = self._sanitize_input(self.args[1]).lower()
        
        if new_status not in VALID_STATUSES:
            raise ValidationError(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
        
        task = self._find_task_by_id(task_id)
        if not task:
            raise ValidationError(f"Task with ID {task_id} not found")
        
        old_status = task['status']
        task['status'] = new_status
        task['updatedAt'] = str(datetime.now())
        
        print(f"[bold green]Task marked[/bold green] [bold red]{old_status} -> {new_status}[/bold red]")
        print(f"[dim]Task ID: {task['id']}[/dim]")

    def list(self):
        filtered_tasks = self.data
        
        if self.args:
            status = self._sanitize_input(self.args[0]).lower()
            if status not in VALID_STATUSES:
                raise ValidationError(f"Invalid status. Must be one of: {', '.join(VALID_STATUSES)}")
            
            filtered_tasks = [task for task in self.data if task['status'] == status]
        
        if not filtered_tasks:
            print("[bold yellow]No tasks found[/bold yellow]")
            return
        
        table = Table(title="Tasks")
        table.add_column("Short ID", style="cyan", justify="center")
        table.add_column("Full ID", style="dim", justify="left")
        table.add_column("Name", style="magenta", justify="center")
        table.add_column("Description", style="yellow", justify="center")
        table.add_column("Status", style="green", justify="center")
        table.add_column("Created At", style="blue", justify="center")
        table.add_column("Updated At", style="blue", justify="center")
        
        for task in filtered_tasks:
            # Create a short, readable ID (first 8 characters)
            short_id = task["id"][:8]
            table.add_row(
                short_id, 
                task["id"],  # Full ID for reference
                task["name"], 
                task["description"], 
                task["status"], 
                task["createdAt"], 
                task["updatedAt"]
            )
        
        console = Console()
        console.print(table)
        
        # Optional: Print instructions for copying ID
        print("\n[bold green]💡 Tip:[/bold green] [dim]Use the full ID for commands like update or delete[/dim]")