import json
from pathlib import Path
from bs4 import BeautifulSoup as bs
import minify_html as _minify

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


class bundle:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self) -> dict:
        """Creates bundle."""

        bundle = {}

        for file in SOURCE.rglob("**/*.*"):
            if " " in file.name:
                continue
            if "history" in file.parts:
                continue
            if "test" in file.parts:
                continue
            path = f"/{file.relative_to(SOURCE).as_posix()}"
            text = file.read_text(encoding=UTF_8).strip()
            if not text:
                continue
            if file.suffix == ".css":
                text = minify_css(text)
            elif file.suffix == ".html":
                text = minify_html(text)
            bundle[path] = text
        print(f"Bundled {len(bundle)} files.")
        self._.update(bundle=bundle)
        return bundle

    def save(self) -> "bundle":
        """Writes bundle to local disc."""
        name = f"{self.__class__.__name__}.json"
        file: Path = Path.cwd() / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(self._["bundle"]), encoding=UTF_8)
        print("Bundle saved to local disc as:", name)
        return self


bundle = bundle()


if __name__ == "__main__":
    bundle()
    bundle.save()
