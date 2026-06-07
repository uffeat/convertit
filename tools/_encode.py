import base64

UTF_8 = "utf-8"


def encode(text: str) -> str:
    """Returns base64 interpretation of text"""
    return base64.b64encode(text.encode(UTF_8)).decode(UTF_8)
    return base64.b64encode(text.encode("utf-8")).decode("ascii")
    
