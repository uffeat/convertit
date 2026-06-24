import json
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

        ##
        ##
        @server_function
        def _bundle() -> BlobMedia:
            """Returns bundle from local disc."""
            name = "bundle.json"
            file = Path.cwd() / name
            content = file.read_text(encoding=UTF_8).strip()
            content = content.encode(UTF_8)
            return BlobMedia("application/json", content, name=name)

        ##
        ##

        ##
        ##
        @server_function
        def _download_bundle() -> dict:
            """Returns bundle from db."""
            try:
                result: BlobMedia = app_tables.use.get(key="files")["bundle"]
                return dict(ok=True, result=result)
            except:
                return dict(ok=False, error=traceback.format_exc())
        ##
        ##

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
