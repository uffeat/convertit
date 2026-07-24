import json
from pathlib import Path
from anvil import BlobMedia
from ._base import Base

UTF_8 = "utf-8"


class File(Base):

    def __init__(self):
        super().__init__()

    def __call__(self, path: str, shape: str=None, text: str = None) -> str:
        """Reads from or writes to local disc."""
        if path.startswith("/"):
            path = path[1:]
        f = Path.cwd() / path
        if text is None:
            text = f.read_text(encoding=UTF_8).strip()
            if shape is dict or shape is list:
                return json.loads(text)
            return text
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding=UTF_8)


file = File()
