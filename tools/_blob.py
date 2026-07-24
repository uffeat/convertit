from mimetypes import guess_type
from anvil import BlobMedia



if __name__ == "__main__":
    ...
    ##from _base import Base
else:
    ...


    ##from ._base import Base

UTF_8 = "utf-8"

def Blob(name: str, content: str) -> BlobMedia:
    """."""
    content_type, _ = guess_type(name)
    content = content.encode(UTF_8)
    return BlobMedia(content_type, content, name=name)


if __name__ == "__main__":
    ...