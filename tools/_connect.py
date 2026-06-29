import json
from pathlib import Path
from anvil.server import (
    connect as _connect,
    wait_forever,
)

UTF_8 = "utf-8"


class connect:

    def __call__(self, *args, server: bool = True):
        """."""
        message = next(iter(args), '')

        _connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["server" if server else "client"]
        )

        message and print(message)

        if server:

            class connection:
                def __enter__(self):
                    return self

                def __exit__(self, exc_type, exc_val, exc_tb):
                    self.keep()

                def keep(self):
                    try:
                        wait_forever()
                    except:
                        wait_forever()

            return connection()

        return self


connect = connect()
