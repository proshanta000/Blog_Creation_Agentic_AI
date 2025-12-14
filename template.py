import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')



project_name = "Blog_Post_AI_Agent"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/llm/__init__.py",
    f"src/{project_name}/graphs/__init__.py",
    f"src/{project_name}/nodes/__init__.py",
    f"src/{project_name}/states/configuration.py",
    "main.py",
    "setup.py",
    "templates/index.html",
    ".env"
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filename)) or (os.path.getsize(filepath) ==0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"creating empty file: {filepath}")
    else:
        logging.info(f"(filename) is already exist")