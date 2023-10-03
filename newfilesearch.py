import os
import datetime
from pathlib import Path

root_folder = Path("/home/chin/Music")

exclude_folders = []

current_date = datetime.datetime.now().date()

for file_path in root_folder.glob("**/*"):
    if file_path.is_dir() and file_path.name in exclude_folders:
        continue

    if file_path.is_file():
        modification_date = datetime.datetime.fromtimestamp(file_path.stat().st_mtime).date()
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).strftime("%Y-%m-%d %H:%M:%S")

        if modification_date == current_date:
            print(f"New file: {file_path} (Created at: {creation_time})")