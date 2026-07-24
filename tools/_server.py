import json
from pathlib import Path
from anvil.server import (
    call,
    callable as server_function,
    connect as _connect,
    wait_forever,
)
from ._base import Base
from ._file import file

UTF_8 = "utf-8"


class Server(Base):
    def __init__(self):
        super().__init__()
        self._.update(names=set())

    def __call__(self, *args) -> "Server":
        """Creates uplink connection."""
        message = next(iter(args), "")

        

        _connect(file("secrets.json", shape=dict)["development"]["server"])
        message and print(message)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait()

    def expose(self, *args) -> callable:
        """."""

        source = [a for a in args if callable(a)][0]

        names = [a for a in args if isinstance(a, str)]
        name: str = names[0] if names else getattr(source, "name", source.__name__)

        if isinstance(source, type):

            def wrapper(*args, **kwargs):
                if "__init__" in source.__dict__:
                    submission = kwargs.pop("submission", None)
                    return source(submission=submission)(*args, **kwargs)

                return source()(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                return source(*args, **kwargs)

        wrapper.__name__ = name

        names: set = self._["names"]
        names.add(name)

        server_function(wrapper)
        return source

    def function(self, *args) -> callable:
        """Decorates server function."""

        first = next(iter(args), None)

        if callable(first):
            # Decorator without params
            source = first
            return self.expose(source)

        # Decorator with params
        def register(source):
            name = first
            return self.expose(name, source)

        return register

    @staticmethod
    def wait():
        try:
            wait_forever()
        except:
            wait_forever()


server = Server()
