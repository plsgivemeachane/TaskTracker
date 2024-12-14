import sys
from json import loads, dumps
from Command import CommandParser

if __name__ == "__main__":
    data = None
    try:
        with open("db.json", "r") as f:
            data = loads(f.read())
    except FileNotFoundError:
        pass        
    commandParser = CommandParser(data=data)
    output = commandParser.execute()
    
    # Save data
    with open("db.json", "w") as f:
        f.write(dumps(output, indent=4))