from base64 import b64decode, b64encode

UTF_8 = "utf-8"


class b64:
    def decode(encoded: str) -> str:
        """Returns text interpretation of base64 string."""
        return b64decode(encoded).decode(UTF_8)

    def encode(text: str) -> str:
        """Returns base64 interpretation of text"""
        return b64encode(text.encode(UTF_8)).decode(UTF_8)

    

