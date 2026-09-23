def main(use, Base: type = None, log: callable = None, path: str = None, **kwargs):
    """."""

    Path = use("use/path/path.py")

    def main(*args, error: str = None, path: dict = None, query: dict = None, **kwargs):
        if error:
            raise Exception(error)
        path = Path(**path)
        ##log("path:", repr(path))  ##
        ##log("query:", query)  ##
        

        if path.source == "test":
            if use.meta.DEV:
                from anvil.js import window
                from anvil.server import call

                ##Log = use("app/tools/log.py").Log
                Log = use.package.tools.log.Log

                def keydown(event):
                    if event.code == "KeyU" and event.shiftKey:
                        stored = window.localStorage.getItem("__test__")
                        path = window.prompt("Path:", stored)
                        if path:
                            window.localStorage.setItem("__test__", path)
                            path = Path(path)
                            try:
                                text = call("_use", path.path)
                                if path.type == 'py':
                                    locals = {}
                                    exec(text, {}, locals)
                                    locals["main"](
                                        use,
                                        Base=Base,
                                        log=Log(path.path),
                                        path=path.path,
                                        text=text,
                                    )
                            except:
                                window.console.error(f"Invalid path:", path.path)

                window.addEventListener("keydown", keydown)

    return main
