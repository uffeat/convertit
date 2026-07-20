import json
from mimetypes import guess_type
from pathlib import Path
import traceback


UTF_8 = "utf-8"


class File:
    
    def __init__(self):
        self.__dict__.update(__={})
        

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, path: str) -> str:
        """."""
        if path.startswith('/'):
            path = path[1:]
        file = Path.cwd() / path[1:]
        result = file.read_text(encoding=UTF_8).strip()
        return result
        


file = File()
