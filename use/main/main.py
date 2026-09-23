def main(use, Base: type = None, log: callable = None, **kwargs):
    """."""

    log('Loading...') ##

    

    def main(*args, error: str = None, path: dict = None, query: dict = None, **kwargs):
        if error:
            raise Exception(error)
        Path = use("use/path/path.py")


        path = Path(**path)
        ##log("path:", repr(path))  ##
        ##log("query:", query)  ##
        

        if path.source == "test":
            if use.meta.DEV:
                use(f"use/test/test.py")()
                use(f"use/test/test.py")()

    return main
