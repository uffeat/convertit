import json
from pathlib import Path
from anvil.server import (
    call,
    callable as server_function,
    connect as _connect,
    wait_forever,
)
from ._use import use

Base = use("@@/base/base.py")

UTF_8 = "utf-8"


class Server(Base):
    def __init__(self):
        super().__init__()
        keys = (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))["development"]

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, *args) ->  'Server':
        """Spins up uplink server."""
        message = next(iter(args), "")
        _connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["server"]
        )
        message and print(message)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.keep()

    @staticmethod
    def function(*args) -> callable:
        """Decorates server function."""
        first = next(iter(args), None)

        if callable(first):
            server_function(first)
            return first

        def register(target):
            if first:
                target.__name__ = first
            server_function(target)
            return target

        return register
    
    @staticmethod
    def keep():
        try:
            wait_forever()
        except:
            wait_forever()


server = Server()
