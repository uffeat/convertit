import json
from pathlib import Path
import sys
import traceback
from anvil import BlobMedia
from anvil.server import call, callable as server_function
from anvil.tables import app_tables
from tools import connect

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
from client_code.tools import Base

TARGET = Path.cwd() / "theme/assets"
UTF_8 = "utf-8"


class Assets(Base):
    def __init__(self):
        super().__init__()

    def __call__(self, path: str, text: str) -> None:
        """Writes file to disc."""
        if path.startswith("/"):
            path = path[1:]
        file: Path = TARGET / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding=UTF_8)
        print(f"Created '{path}'.")


assets = Assets()


class Build(Base):
    def __init__(self):
        super().__init__()

    def __call__(self) -> None:
        """Creates asset files."""
        with connect("Running local server for building."):
            # Create bundle.json and hyper-media files
            table = getattr(app_tables, "use")
            row: dict = table.get(path="bundle.json")
            file: BlobMedia = row.get("file")
            print(f"Retrieved {file.name} from db.")  ##
            text: str = file.get_bytes().decode(UTF_8)
            assets("bundle.json", text)
            bundle: dict = json.loads(text)
            for path, text in bundle.items():
                path: str = path
                if path.endswith(".css") or path.endswith(".svg"):
                    assets(path, text)

            @server_function
            def _save_file(file: BlobMedia, path: str = None) -> dict:
                """Saves file to db and server disc."""
                try:
                    if not path:
                        path = file.name
                    print("path:", path)  ##
                    row = app_tables.use.get(path=path)
                    if not row:
                        row = app_tables.use.add_row(path=path)
                    row.update(file=file)
                    text: str = file.get_bytes().decode(UTF_8)
                    assets(path, text)
                    return dict(ok=True)
                except:
                    return dict(ok=False, error=traceback.format_exc())


build = Build()


if __name__ == "__main__":
    build()
