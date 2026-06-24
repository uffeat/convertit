import json
from mimetypes import guess_type
from pathlib import Path
import traceback
from anvil import BlobMedia

UTF_8 = "utf-8"


def get_file(path: str) -> BlobMedia:
    """Returns text-based file from local disc."""
    file = Path.cwd() / path[1:]
    content_type, encoding = guess_type(file.name)
    content = file.read_text(encoding=UTF_8).strip().encode(UTF_8)
    return BlobMedia(content_type, content, name=path)


file = get_file("/parcels/foo/foo.json")
print("file:", file)
