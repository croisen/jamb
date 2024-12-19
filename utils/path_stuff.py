from pathlib import Path
import os


def get_script_dir(file: str) -> Path:
    return Path(os.path.dirname(os.path.realpath(file)))
