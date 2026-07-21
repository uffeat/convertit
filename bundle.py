import json
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.tables import app_tables
from tools import Base, file, minify, server

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class Bundle(Base):
    def __init__(self):
        super().__init__()

    def __call__(self) -> "Bundle":
        """."""

        bundle = self.create()
        print(f"Bundled {len(bundle)} files.")

        text = json.dumps(bundle)

        # Write bundle to disc
        file(self.name, text)
        print(f"{self.name} saved to local disc")

        self._.update(
            blob=BlobMedia("application/json", text.encode(UTF_8), name=self.name)
        )
        return self

    @property
    def blob(self):
        return self._.get("blob")

    @property
    def name(self):
        return "bundle.json"

    def create(self) -> dict:
        """Creates bundle."""

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
                text = minify.css(text)
            elif file.suffix == ".html":
                text = minify.html(text)
            bundle[path] = text

        return bundle

    def connect(self):
        """."""

        with server("Running local server for building."):
            table = getattr(app_tables, "use")

            if self.blob:
                row: dict = table.get(path=bundle.name)
                if not row:
                    row: dict = table.add_row(path=self.name)
                row.update(file=self.blob)
                print(f"{self.name} saved to db.")

            @server.function
            def _build(path: str) -> str:
                """Returns code text from local disc."""
                ##print("path:", path)  ##
                return file(f"build{path}")

            @server.function
            def _save_file(file: BlobMedia, path: str = None) -> dict:
                """Saves file to db."""
                try:
                    if not path:
                        path = file.name
                    ##print("path:", path)  ##
                    row = table.get(path=path)
                    if not row:
                        row = table.add_row(path=path)
                    row.update(file=file)
                    print(f"{path} saved to db.")
                    return dict(ok=True)
                except:
                    return dict(ok=False, error=traceback.format_exc())


bundle = Bundle()


if __name__ == "__main__":
    bundle().connect()
