import base64

UTF_8 = "utf-8"


class Base64:

    def encode(text: str) -> str:
        """Returns base64 interpretation of text"""
        return base64.b64encode(text.encode(UTF_8)).decode(UTF_8)

    def decode(encoded: str) -> str:
        """Returns text interpretation of base64 string."""
        return base64.b64decode(encoded).decode(UTF_8)


text = "stuff"
encoded = Base64.encode(text)

print("encoded:", encoded)

decoded = Base64.decode(encoded)

print("decoded:", decoded)
