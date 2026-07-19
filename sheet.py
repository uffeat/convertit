from pathlib import Path
from anvil import BlobMedia
from anvil.server import callable as server_function
from tools import connect, minify

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


def compile() -> str:
    """Returns aggregate css from same-name parcel sheets."""
    css = [
        f.read_text(encoding=UTF_8)
        for f in SOURCE.rglob("**/*.css")
        if f.parent.name == f.stem
    ]

    css = "\n".join(css)
    return css


def Sheet(text: str, name: str = "") -> BlobMedia:
    text = minify.css(text)
    sheet = BlobMedia("text/css", text.encode(UTF_8), name=name)
    return sheet


def sheet():
    """."""
    with connect("Running local server for serving uncommitted stylesheets."):

        @server_function
        def _sheet(path: str) -> BlobMedia:
            print("path:", path)  ##
            if path == "/main.css":
                text = compile()
                return Sheet(text, name=path[1:])
            file = SOURCE / path[1:]
            text = file.read_text(encoding=UTF_8).strip()
            return Sheet(text, name=file.name)


if __name__ == "__main__":
    sheet()
