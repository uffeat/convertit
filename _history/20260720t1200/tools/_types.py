from pathlib import Path

def get_types(file: Path) -> tuple:
    stem, *types = file.name.split(".")
    return tuple(types)
