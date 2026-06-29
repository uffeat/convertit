import json
from mimetypes import guess_type
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.server import (
    callable as server_function,
    connect,
    wait_forever,
)
from anvil.tables import app_tables

ASSETS = Path.cwd() / "theme/assets"
UTF_8 = "utf-8"


class server:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self):
        connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["server"]
        )

        @server_function
        def _upload_sheet(sheet: BlobMedia) -> dict:
            """Saves sheet to disc and to db."""
            try:
                text: str = sheet.get_bytes().decode(UTF_8)
                file: Path = ASSETS / sheet.name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(text, encoding=UTF_8)
                column, *_ = sheet.name.partition('.')
                app_tables.use.get(key="files").update(**{column: sheet})
                return dict(ok=True)
            except:
                return dict(ok=False, error=traceback.format_exc())

        print("Running local server.")

        # HACK Sometimes fails at first run
        try:
            wait_forever()
        except:
            wait_forever()


server = server()


if __name__ == "__main__":
    server()
