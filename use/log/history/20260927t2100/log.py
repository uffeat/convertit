def main(use, Base=None, **kwargs):
    """."""

    if use.meta.DEV:

        class Log(Base):
            def __init__(self, *args, **kwargs):
                path = next(iter(args), None)
                Base.__init__(self, path=path)

            def __call__(self, *args, **kwargs):
                """Writes to console."""
                if self.path:
                    args = [*args, f"\n(trace: {self.path})"]
                print(*args)

    else:

        class Log:
            def __init__(self, *args, **kwargs):
                """."""

            def __call__(self, *args, **kwargs):
                """."""

    return Log
