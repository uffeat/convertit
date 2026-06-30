from pathlib import Path
from anvil import BlobMedia
from anvil.server import callable as server_function
from tools import connect, minify

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"




def create_sheet():
    css = []
    for file in SOURCE.rglob("**/*.css"):
        if file.parent.name != file.stem:
            continue
        text = file.read_text(encoding=UTF_8).strip()
        text = minify.css(text)
        css.append(text)

    css = "\n".join(css)
    sheet = BlobMedia("text/css", css.encode(UTF_8), name="main.css")
    return sheet


def sheet():
    """."""
    with connect("Running local server for serving uncommitted main stylesheet."):

        @server_function
        def _sheet() -> BlobMedia:
            print("Returning sheet")  ##
            return create_sheet()


if __name__ == "__main__":
    sheet()
