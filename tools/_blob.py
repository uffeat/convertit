from mimetypes import guess_type
from anvil import BlobMedia





UTF_8 = "utf-8"

def Blob(name: str, content: str) -> BlobMedia:
    """."""
    content_type, _ = guess_type(name)
    content = content.encode(UTF_8)
    return BlobMedia(content_type, content, name=name)


