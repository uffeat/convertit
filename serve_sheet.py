from pathlib import Path
from anvil import BlobMedia
from anvil.server import callable as server_function
from bs4 import BeautifulSoup as bs
import minify_html as _minify
from tools import connect

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


def minify_html(html: str) -> str:
    """Returns minified html."""
    config = dict(
        minify_css=True,
        minify_js=False,
        remove_processing_instructions=True,
        keep_closing_tags=True,
        keep_html_and_head_opening_tags=True,
        keep_comments=False,
    )
    return _minify.minify(html, **config)


def minify_css(css: str) -> str:
    """Returns minified css."""
    html = minify_html(f"<style>\n{css}</style>")
    soup = bs(html, "html.parser")
    style = soup.select_one("style")
    return style.string


def create_sheet():
    css = []
    for file in SOURCE.rglob("**/*.css"):
        if file.parent.name != file.stem:
            continue
        text = file.read_text(encoding=UTF_8).strip()
        text = minify_css(text)
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
