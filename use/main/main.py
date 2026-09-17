def main(use, log: callable, path: str = None, **kwargs):
    """."""
    Path = use("use/path/path.py")

    def main(*args, error: str = None, path: dict = None, query: dict = None, **kwargs):
        if error:
            raise Exception(error)
        path = Path(**path)
        log("path:", repr(path))  ##
        log("query:", query)  ##
        page = next(iter(path.parts[1:2]), None)
        log("page:", page)  ##

    return main
