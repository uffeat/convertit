import json
from anvil import BlobMedia

UTF_8 = "utf-8"

def Blob(content, content_type='', name='') -> BlobMedia:
    """."""
    content = json.dumps(content)
    content = content.encode(UTF_8)
    return BlobMedia(content_type, content, name=name)

