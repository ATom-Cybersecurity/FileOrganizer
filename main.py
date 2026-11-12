from pathlib import Path
import hashlib, os, argparse, logging, json, pyinputplus as pyip

with open("organizer.log", "w") as file:
    pass

listOfFilesToMove = []
while True:
    folderPath = pyip.inputFilepath(prompt="Please, enter the path to the folder: ")
    folderPath = Path(folderPath)
    if folderPath.is_dir():
        break

logPath = Path("organizer.log")
logging.basicConfig(
    filename=logPath,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dry-run",
    action="store_true"
)
args = parser.parse_args()

countForFiles = 1
filesDict = {}
categoriesFoldersDict = {
    "Images": [], "Documents": [], 
    "Audio": [], "Video": [], 
    "Archives": [], "Programs": [], 
    "Code": [], "Fonts": [],
    "DataBases": [], "Torrents": [],
    "Other": []
               }

for filename in os.listdir(folderPath):
    filePath = folderPath / filename
    fileSuffix = filePath.suffix

    if filePath.is_dir():
        continue
    with open(filePath, "rb") as f:
        fileHash = hashlib.sha256()
        while True:
            file = f.read(4096)
            fileHash.update(file)
            if file == b"":
                break

        filesDict.setdefault(fileHash.hexdigest(), [])
        filesDict[fileHash.hexdigest()].append(filePath.name)
        logging.debug(f"File name: {filePath.name} File hash: {fileHash.hexdigest()}")

    if fileSuffix.lower() in (
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp",
        ".tiff", ".tif", ".svg", ".ico", ".heic", ".heif",
        ".raw", ".cr2", ".nef"
                      ):
        categoriesFoldersDict["Images"].append(filePath.name)

    elif fileSuffix.lower() in (
        ".pdf", ".doc", ".docx", ".odt", ".rtf",
        ".txt", ".md", ".tex", ".pages", ".xls",
        ".xlsx", ".xlsm", ".xlsb"
                        ):
        categoriesFoldersDict["Documents"].append(filePath.name)

    elif fileSuffix.lower() in (".mp3", ".wav", ".ogg", ".flac", ".aac", ".wma", ".mid", ".midi"):
        categoriesFoldersDict["Audio"].append(filePath.name)

    elif fileSuffix.lower() in (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg"):
        categoriesFoldersDict["Video"].append(filePath.name)

    elif fileSuffix.lower() in (".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".cab"):
        categoriesFoldersDict["Archives"].append(filePath.name)

    elif fileSuffix.lower() in (".exe", ".msi", ".app", ".bat", ".sh", ".bin", ".deb", ".rpm"):
        categoriesFoldersDict["Programs"].append(filePath.name)

    elif fileSuffix.lower() in (".py", ".js", ".java", ".cpp", ".c", ".cs", ".go", ".rs", ".rb", ".php", ".swift", ".kt"):
        categoriesFoldersDict["Code"].append(filePath.name)

    elif fileSuffix.lower() in (".ttf", ".otf", ".woff", ".woff2", ".eot"):
        categoriesFoldersDict["Fonts"].append(filePath.name)

    elif fileSuffix.lower() in (".db", ".sqlite", ".mdb", ".accdb", ".sql", ".dump", ".bak"):
        categoriesFoldersDict["DataBases"].append(filePath.name)

    elif fileSuffix.lower() in (".torrent",):
        categoriesFoldersDict["Torrents"].append(filePath.name)

    else:
        categoriesFoldersDict["Other"].append(filePath.name)

        
for key, value in filesDict.items():
    if len(value) > 1:
        logging.warning("Files with identical hashes: %s", value)

for key in categoriesFoldersDict.keys():
    if args.dry_run:
        logging.info(f"The folder {key} will be created!")

    else:
        (folderPath / key).mkdir(exist_ok=True)

logging.info(f"Folders successfully created!")

if not args.dry_run:
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump([], file)
for keys, values in categoriesFoldersDict.items():
    if len(values) == 0:
        continue

    else:
        for value in values:
            if args.dry_run:
                print(f"The file {value} will be moved!")
    
            else:
                originalName = Path(value).stem
                extension = Path(value).suffix

                def function():
                    global countForFiles

                    if Path(folderPath / keys / value).exists():
                        while True:
                            newValue = originalName + str(countForFiles) + extension
                            if (folderPath / keys / newValue).exists():
                                countForFiles += 1

                            else:
                                break

                        os.rename(folderPath / value, folderPath / keys / newValue)
                        print(f"File {value} successfully moved!")

                        listOfFilesToMove.append([])
                        listOfFilesToMove[-1].append(folderPath / value)
                        listOfFilesToMove[-1].append(Path(folderPath / keys / newValue))

                    else:
                        os.rename(folderPath / value, folderPath / keys / value)
                        print(f"File {value} successfully moved!")

                        listOfFilesToMove.append([])
                        listOfFilesToMove[-1].append(Path(folderPath / value))
                        listOfFilesToMove[-1].append(Path(folderPath / keys / value))

                function()
                with open("history.json", "w", encoding="utf-8") as file:
                    json.dump(listOfFilesToMove, file, indent=4, default=str)

if args.dry_run:
    pass

else:
    with open("history.json", "w", encoding="utf-8") as file:
        json.dump(listOfFilesToMove, file, indent=4, default=str)

print("Ready!")