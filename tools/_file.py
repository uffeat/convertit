import json
from mimetypes import guess_type
from pathlib import Path
import traceback
from ._base import Base

UTF_8 = "utf-8"


class File(Base):

    def __init__(self):
        super().__init__()

    def __call__(self, path: str, text: str = None) -> str:
        """."""
        if path.startswith("/"):
            path = path[1:]
        file = Path.cwd() / path
        if text is None:
            return file.read_text(encoding=UTF_8).strip()
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding=UTF_8)


file = File()
