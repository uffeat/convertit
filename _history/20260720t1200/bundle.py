import json
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.tables import app_tables
from tools import minify, server, use

Base = use("@@/base/base.py")


SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class Bundle(Base):
    def __init__(self):
        super().__init__()

    def __call__(self) -> 'Bundle':
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

        print(f"Bundled {len(bundle)} files.")
        # Write bundle to disc
        text = json.dumps(bundle)
        file: Path = Path.cwd() / self.name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding=UTF_8)
        print("Bundle saved to local disc as:", self.name)
        blob = BlobMedia("application/json", text.encode(UTF_8), name=self.name)
        self._.update(blob=blob)
        return self

    @property
    def blob(self):
        return self._.get('blob')
    
    @property
    def name(self):
        return "bundle.json"
    
    def save(self):
        """."""
        
        with server("Running local server for building."):
            if self.blob:
                table = getattr(app_tables, "use")
                row: dict = table.get(path=bundle.name)
                if not row:
                    row: dict = table.add_row(path=self.name)
                row.update(file=self.blob)
                print(f"{self.name} saved to db.")

            

            @server.function
            def _build(path: str) -> str:
                """Returns code text from local disc."""
                print("path:", path)  ##
                file = Path.cwd() / "build" / path[1:]
                result = file.read_text(encoding=UTF_8).strip()
                return result


            


bundle = Bundle()


if __name__ == "__main__":
    bundle().save()

    