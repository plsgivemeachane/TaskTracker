import sys
import os
from json import loads, dumps, JSONDecodeError
from Command import CommandParser

def safe_load_data(filename="db.json"):
    """Safely load data from JSON file."""
    if not os.path.exists(filename):
        return None
    
    try:
        with open(filename, "r") as f:
            content = f.read()
            return loads(content) if content else None
    except (FileNotFoundError, JSONDecodeError, PermissionError) as e:
        return None

def safe_save_data(data, filename="db.json"):
    """Safely save data to JSON file with backup."""
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        # Write new data
        with open(filename, "w") as f:
            f.write(dumps(data, indent=4))
        
    except Exception as e:
        pass

if __name__ == "__main__":
    data = safe_load_data()
    
    commandParser = CommandParser(data=data)
    
    try:
        output = commandParser.execute()
        safe_save_data(output)
    except Exception as e:
        sys.exit(1)