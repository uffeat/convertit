import json
from pathlib import Path
from anvil.server import connect as _connect

UTF_8 = "utf-8"


class Connect:

    def __call__(self, message=None):
        """Creates uplink client connection."""

        _connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["client"]
        )

        message and print(message)


connect = Connect()
