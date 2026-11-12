import os, json
from pathlib import Path

with open("history.json", "r", encoding="utf-8") as file:
    history = json.load(file)

listForFiles = []
for path in reversed(history):
    try:
        if Path(path[1]).exists() and not Path(path[0]).exists():
            os.rename(Path(path[1]), Path(path[0]))
            print("File", Path(path[1]).name, "successfully moved!")

        else:
            print("File", Path(path[1]).name, "not moved!")
            listForFiles.append(path)

    except FileExistsError:
        print("File", Path(path[1]).name, "not moved!")
        listForFiles.append(path)

print("Files moved back!")

if len(listForFiles) > 0:
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(listForFiles, file, indent=4)

else:
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump([], file)