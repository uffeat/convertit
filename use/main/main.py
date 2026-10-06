def main(use, Base: type = None, log: callable = None, **kwargs) -> callable:
    """Returns function to be called at main client-code entry point."""

    ##
    ##
    from anvil.js import window
    from anvil.server import call

    log("session:", use.session)

    result = call("main", 'foo', )
    log("result:", result)  ##

    result = call("main")
    log("result:", result)  ##
    ##
    ##

    ##Path = use("use/path/path.py")
    Path = use.Path

    def main(*args, error: str = None, path: dict = None, query: dict = None, **kwargs):
        ##log("kwargs:", kwargs)  ##
        if error:
            raise Exception(error)
        path = Path(**path)
        if path.source == "test":
            if not use.meta.PROD:
                use(f"use/test/test.py")()
                ##use(f"use/test/test.py")()  ##

    return main
