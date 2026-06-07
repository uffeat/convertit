import json
from pathlib import Path
from anvil.server import (
    callable as server_function,
    connect as _connect,
    disconnect,
    wait_forever,
)

UTF_8 = "utf-8"


def connect(message: str = "", server: bool = True) -> callable:

    _connect(
        (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
            "development"
        ]["server" if server else "client"]
    )

    message and print(message)

    def keep(message: str = ""):
        message and print(message)
        if server:
            # HACK Sometimes fails at first run
            try:
                wait_forever()
            except:
                wait_forever()

    return keep


class Connection:
    def __init__(self, message: str = "", server: bool = True):
        """."""
        self._ = dict(message=message, server=server)

    def __enter__(self):
        """."""
        self._.update(keep=connect())

        # Return 'as' variable
        return server_function

    def __exit__(self, exc_type, exc_val, exc_tb):
        """."""
        keep = self._["keep"]
        keep(self._["message"])
        # Return True to suppress exceptions, False to let them propagate
        return False
