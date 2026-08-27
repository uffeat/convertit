from ..tools import Base, meta
from ..works import works

if meta.DEV:

    PREFIX = f"app/{meta.name}"
    PREFIX_SIZE = len(PREFIX)

    
    
        


    class Log(Base):
        def __init__(self, *args, **kwargs):
            path = next(iter(args), kwargs.get('path'))
            kwargs.update(path=f"client_code{path[PREFIX_SIZE:]}" if path and path.startswith(PREFIX) else path)
            Base.__init__(self, **kwargs)

        def __call__(self, *args, **kwargs):
            """Writes to console."""
            kwargs.update(
                **next(
                    iter(
                        [
                            a
                            for a in args
                            if works.window.Object.prototype.toString.call(a)[8:-1]
                            == "Object"
                        ]
                    ),
                    {},
                )
            )

            

            if self.path:
                args = [*args, f"\n(trace: {self.path})"]

            native = kwargs.get("native")
            if native:
                if isinstance(native, str):
                    works.window.console[native](*args)
                else:
                    works.window.console.log(*args)
            else:
                print(*args)

else:

    class Log:
        def __init__(self, *args, **kwargs):
            """."""

        def __call__(self, *args, **kwargs):
            """."""
