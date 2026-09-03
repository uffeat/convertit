import anvil.js
from .base import Base
from .meta import meta



console = anvil.js.window.console


if meta.DEV:

    OUT = (print, console)
    PREFIX = f"app/{meta.name}"
    PREFIX_SIZE = len(PREFIX)

    class Log(Base):
        def __init__(self, *args, **kwargs):
            path = next(iter(args), None)
            path = (
                f"client_code{path[PREFIX_SIZE:]}"
                if path and path.startswith(PREFIX)
                else path
            )

            Base.__init__(
                self, path=path, **{k: v for k, v in kwargs.items() if k != "path"}
            )

        def __call__(self, *args, **kwargs):
            """Writes to console."""
            show = [a for a in args if a not in OUT]
            if self.path:
                show.append(f"\n(trace: {self.path})")
            out = next(iter([a for a in args if a in OUT]), print)
            out(*show)

else:

    class Log:
        def __init__(self, *args, **kwargs):
            """."""

        def __call__(self, *args, **kwargs):
            """."""


export = Log


