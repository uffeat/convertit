import json
from pathlib import Path
from bs4 import BeautifulSoup as bs
import minify_html as minify
from anvil import BlobMedia
from anvil.server import call, connect, disconnect

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
    return minify.minify(html, **config)


def minify_css(css: str) -> str:
    """Returns minified css."""
    html = minify_html(f"<style>\n{css}</style>")
    soup = bs(html, "html.parser")
    style = soup.select_one("style")
    return style.string


class Bundle:
    def __init__(self):
        self.__dict__.update(__={})
        self._.update(bundle={}, name="bundle.json")

    def __call__(self) -> "Bundle":
        """Creates bundle."""
        for file in SOURCE.rglob("**/*.*"):
            if "test" in file.parts:
                continue
            path = f"/{file.relative_to(SOURCE).as_posix()}"
            text = file.read_text(encoding=UTF_8).strip()
            if file.suffix == ".css":
                text = minify_css(text)
            elif file.suffix == ".html":
                text = minify_html(text)

            self._["bundle"][path] = text
        self._.update(text=json.dumps(self._["bundle"]))
        print(f'Bundled {len(self._["bundle"])} files.')
        return self

    @property
    def _(self) -> dict:
        return self.__

    def save(self) -> "Bundle":
        """Writes bundle to local disc."""
        file = Path.cwd() / self._["name"]
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(self._["text"], encoding=UTF_8)
        print(f"Bundle saved to local disc as:", self._["name"])
        return self

    def upload(self) -> "Bundle":
        """Uploadsbundle to db."""
        content = self._["text"].encode(UTF_8)
        bundle = BlobMedia("application/json", content, name=self._["name"])
        connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["client"]
        )
        try:
            call("_upload_bundle", bundle)
            print(f"Bundle uploaded.")
        except:
            print(f"Bundle NOT uploaded.")
        return self


if __name__ == "__main__":
    Bundle()().save().upload()
