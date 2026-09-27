def main(use, Base: type = None, log: callable = None, **kwargs) -> callable:
    """Returns function to be called at main client-code entry point."""
    ##Path = use("use/path/path.py")
    Path = use.Path

    def main(*args, error: str = None, path: dict = None, query: dict = None, **kwargs):
        if error:
            raise Exception(error)
        path = Path(**path)
        if path.source == "test":
            if use.meta.DEV:
                use(f"use/test/test.py")()
                ##use(f"use/test/test.py")()  ##

    return main
