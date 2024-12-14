import sys
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime


# Data structure
# {
#     "id": int    
#     "name": string
#     "status": "todo" | "in progress" | "done",
#     "createdAt": date
#     "updatedAt": date,
#     "description": string
# }

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
                    "name: <string>"
                ]
            },
            "delete": {
                "name": "Delete",
                "description": "Delete a task from the todo list",
                "args": [
                    "id: <int>"
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
                    "id: <int>",
                    "name: <string>",  
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
    
    def execute(self):
        argsLen = len(sys.argv)
        if argsLen < 2:
            print("[bold red]No commands given[/bold red]")
            return
        
        for i in range(2, argsLen):
            self.args.append(sys.argv[i])
        
        if sys.argv[1] in self.commands:
            self.commands[sys.argv[1]]()
        else:
            print("[bold red]Command not found[/bold red]")
            self.help()
            
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
            print("[bold green]Command:[/bold green]")
            print(f"    [bold red]{command}[/bold red]", end = " - ")
            print(f"[bold]{self.helps[command]['name']}[/bold]")
            print(f"    [dim]{self.helps[command]['description']}[/dim]")
            for commandArg in self.helps[command]["args"]:
                print(f"        {commandArg}")

    
    def add(self):
        self.data.append({
            "id": len(self.data) + 1,
            "name": self.args[0],
            "description": "None",
            "status": "todo",
            "createdAt": str(datetime.now()),
            "updatedAt": str(datetime.now())
        })
    
    def update(self):
        if not self.args[0].isnumeric():
            print("[bold red]ID must be a number[/bold red]")
            return
        if int(self.args[0]) > len(self.data):
            print("[bold red]Task not found[/bold red]")
            return

        for i in range(len(self.data)):
            if self.data[i]["id"] == int(self.args[0]):
                preDes = self.data[i]["description"]
                self.data[i]["description"] = self.args[1]
                self.data[i]["updatedAt"] = str(datetime.now())
                print("[bold green]Task updated[/bold green] [bold red] " + preDes + " -> " + self.data[i]["description"] + "[/bold red]")
                return
        print("[bold red]Task not found[/bold red]")
    
    def delete(self):
        if not self.args[0].isnumeric():
            print("[bold red]ID must be a number[/bold red]")
            return
        if int(self.args[0]) > len(self.data):
            print("[bold red]Task not found[/bold red]")
            return
        if self.args[0] == "all":
            self.data = []
            print("[bold green]All tasks deleted[/bold green]")
            return
        self.data = [task for task in self.data if task["id"] != int(self.args[0])]
        print("[bold green]Task deleted[/bold green]")
    
    def mark(self):
        if not self.args[0].isnumeric():
            print("[bold red]ID must be a number[/bold red]")
            return
        if int(self.args[0]) > len(self.data):
            print("[bold red]Task not found[/bold red]")
            return
        for i in range(len(self.data)):
            if self.data[i]["id"] == int(self.args[0]):
                self.data[i]["status"] = self.args[1]
                self.data[i]["updatedAt"] = str(datetime.now())
                print("[bold green]Task marked as " + self.args[1] + "[/bold green]")
                return
        print("[bold red]Task not found[/bold red]")
    
    def list(self):
        if len(self.args) == 0:
            table = Table(title="Tasks")
            table.add_column("ID", style="cyan", justify="center")
            table.add_column("Name", style="magenta", justify="center")
            table.add_column("Description", style="yellow", justify="center")
            table.add_column("Status", style="green", justify="center")
            table.add_column("Created At", style="blue", justify="center")
            table.add_column("Updated At", style="blue", justify="center")
            for task in self.data:
                table.add_row(str(task["id"]), task["name"], task["description"], task["status"], task["createdAt"], task["updatedAt"])
            console = Console()
            console.print(table)
        else:
            table = Table(title="Tasks (" + self.args[0] + ")")
            table.add_column("ID", style="cyan", justify="center")
            table.add_column("Name", style="magenta", justify="center")
            table.add_column("Description", style="yellow", justify="center")
            table.add_column("Status", style="green", justify="center")
            table.add_column("Created At", style="blue", justify="center")
            table.add_column("Updated At", style="blue", justify="center")
            for task in self.data:
                if task["status"] == self.args[0]:
                    table.add_row(str(task["id"]), task["name"], task["description"], task["status"], task["createdAt"], task["updatedAt"])
            console = Console()
            console.print(table)

    