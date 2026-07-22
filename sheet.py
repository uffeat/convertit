from pathlib import Path
from anvil import BlobMedia
from tools import minify, server

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"




def Sheet(name: str, text: str) -> BlobMedia:
    text = minify.css(text)
    return BlobMedia("text/css", text.encode(UTF_8), name=name)


def sheet(path: str) -> BlobMedia:
    print("path:", path)  ##
    if path == "/main.css":
        text = "\n".join(
            [
                f.read_text(encoding=UTF_8)
                for f in SOURCE.rglob("**/*.css")
                if f.parent.name == f.stem
            ]
        )
        return Sheet(path[1:], text)

    file = SOURCE / path[1:]
    text = file.read_text(encoding=UTF_8).strip()
    return Sheet(file.name, text)


if __name__ == "__main__":
    with server("Running local server for serving uncommitted stylesheets."):
        server.function("_sheet")(sheet)
