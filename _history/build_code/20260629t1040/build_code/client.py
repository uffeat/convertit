import json
from pathlib import Path
from anvil import BlobMedia
from anvil.tables import app_tables
from anvil.server import (
    callable as server_function,
    connect,
    disconnect,
    wait_forever,
)

UTF_8 = "utf-8"

class build:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self) -> None:
        """."""
        connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["client"]
        )
        blob: BlobMedia = app_tables.use.get(key="files")["use"]
        text: str = blob.get_bytes().decode(UTF_8)
        file = Path.cwd() / f"theme/assets/{blob.name}"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding=UTF_8)


build = build()


if __name__ == "__main__":
    build()
