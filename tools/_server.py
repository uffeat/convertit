import json
from pathlib import Path
from anvil.server import (
    HttpResponse,
    call,
    callable as server_function,
    connect as _connect,
    http_endpoint,
    request,
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


    def api(self, *args) -> callable:
            """Decorates server http endpoint."""
            source = next(iter([a for a in args if callable(a)]), None)
            name: str = next(iter([a for a in args if isinstance(a, str)]), None)
    
            def register(source):
                if isinstance(source, type):
    
                    def wrapper(*args, **kwargs):
                        if "__init__" in source.__dict__:
                            submission = kwargs.pop("submission", None)
                            return source(submission=submission)(*args, **kwargs)
                        return source()(*args, **kwargs)
    
                else:
    
                    def wrapper(*args, **query):

                        result = source(*args, **query)

                        return HttpResponse(
                            body=result,
                            headers={
                                "access-control-allow-origin": "*",
                            },
                        )
    
                
    
                ##self.names.add(name)
                http_endpoint(name)(wrapper)
                return source
    
            if source:
                return register(source)
            return register




    def function(self, *args) -> callable:
        """Decorates server function."""
        source = next(iter([a for a in args if callable(a)]), None)
        name: str = next(iter([a for a in args if isinstance(a, str)]), None)

        def register(source):
            if isinstance(source, type):

                def wrapper(*args, **kwargs):
                    if "__init__" in source.__dict__:
                        submission = kwargs.pop("submission", None)
                        return source(submission=submission)(*args, **kwargs)
                    return source()(*args, **kwargs)

            else:

                def wrapper(*args, **kwargs):
                    return source(*args, **kwargs)

            wrapper.__name__ = name or source.__name__

            self.names.add(name)
            server_function(wrapper)
            return source

        if source:
            return register(source)
        return register

    @staticmethod
    def wait():
        try:
            wait_forever()
        except:
            wait_forever()


server = Server()
