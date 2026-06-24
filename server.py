import json
from mimetypes import guess_type
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.server import (
    callable as server_function,
    connect,
    disconnect,
    wait_forever,
)
from anvil.tables import app_tables, Row, Table

PARCELS = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class Server:
    def __init__(self):
        """."""
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self):
        """."""
        connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["server"]
        )

        @server_function
        def _access() -> bool:
            return True

        @server_function
        def _get_file(path: str) -> BlobMedia:
            """Returns file from local disc."""
            file = Path.cwd() / path[1:]
            content_type, encoding = guess_type(file.name)
            content = file.read_text(encoding=UTF_8).strip().encode(UTF_8)
            return BlobMedia(content_type, content, name=path)
        
        @server_function
        def _save_file(blob: BlobMedia) -> None:
            """Saves file to local disc."""
            path = blob.name
            text: str = blob.get_bytes().decode(UTF_8)
            file: Path = Path.cwd() / path[1:]
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(text, encoding=UTF_8)

        @server_function
        def _log(*args) -> None:
            print(*args)

        @server_function
        def _use(path: str) -> str:
            """Returns code text from local disc."""
            ##print("path:", path)  ##
            file = PARCELS / path[1:]
            result = file.read_text(encoding=UTF_8).strip()
            ##print("result:", result)  ##
            return result

        @server_function
        def _upload_bundle(bundle: BlobMedia) -> dict:
            """Saves bundle to db."""
            try:
                app_tables.use.get(key="files").update(bundle=bundle)
                return dict(ok=True)
            except:
                return dict(ok=False, error=traceback.format_exc())

        @server_function
        def _upload_sheet(sheet: BlobMedia) -> dict:
            """Saves sheet to db."""
            try:
                app_tables.use.get(key="files").update(use=sheet)
                return dict(ok=True)
            except:
                return dict(ok=False, error=traceback.format_exc())

        print("Running local server.")

        # HACK Sometimes fails at first run
        try:
            wait_forever()
        except:
            wait_forever()


if __name__ == "__main__":
    Server()()
