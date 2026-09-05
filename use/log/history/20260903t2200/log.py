def main(use, Base=None, anvil=None, **kwargs):
    """."""

    meta = use("use/meta/meta.py")

    
    if meta.DEV:

        console = anvil.window.console

        PREFIX = f"app/{meta.name}"

        class Log(Base):
            def __init__(self, path: str = None):
                if path and path.startswith(PREFIX):
                    path = f"client_code{path[len(PREFIX):]}"
                Base.__init__(self, _path=path)

            def __call__(self, *args, native: str = None):
                """Writes to console."""
                if self._path:
                    args = [*args, f"\n(trace: {self._path})"]

                if native:
                    if isinstance(native, str):
                        console[native](*args)
                    else:
                        console.log(*args)
                else:
                    print(*args)

    else:

        class Log:
            def __init__(self, *args, **kwargs):
                """."""

            def __call__(self, *args, **kwargs):
                """."""


   

    return Log




