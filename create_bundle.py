import json
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.server import call, connect
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

    def __call__(self) -> BlobMedia:
        """Creates and returns bundle."""

        bundle = {}

        for file in SOURCE.rglob("**/*.*"):
            if " " in file.name:
                continue
            if "history" in file.parts:
                continue
            if "scratch" in file.parts:
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
        # Write bundle to disc
        text = json.dumps(bundle)
        file: Path = Path.cwd() / self.name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding=UTF_8)
        print("Bundle saved to local disc as:", self.name)
        bundle = self.create_blob(text)
        self.upload(bundle)
        return bundle
    
    @property
    def name(self):
        return "bundle.json"
    
    def create_blob(self, text: str) -> BlobMedia:
        return BlobMedia("application/json", text.encode(UTF_8), name=self.name)
    
    
    def upload(self, bundle: BlobMedia=None):
        # NOTE Allows upload without bundle recreation
        if not bundle:
            # Create bundle from disk
            text = (Path.cwd() / self.name).read_text(UTF_8)
            bundle = self.create_blob(text)

        try:
            connect(
                (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                    "development"
                ]["client"]
            )
        except Exception as error:
            print(f"Could not connect. Error: {str(error)}")
        else:
            try:
                response: dict = call("_upload_bundle", bundle)
            except Exception as error:
                # Uncontrolled error related to the server function
                print(f"Bundle not uploaded. Error: {str(error)}")
            else:
                if response.get("ok"):
                    print("Bundle uploaded.")
                else:
                    # Controlled error
                    print(f"Bundle upload failed. Error: {response.get('error')}")


bundle = bundle()


if __name__ == "__main__":
    bundle()
