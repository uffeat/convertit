def main(use, Base: type = None, log: callable = None, state: dict = None, **kwargs):
    """."""

    log("Loading...")  ##

   

    def main(*args, **kwargs):
        if state.get("used"):
            return
        state.update(used=True)

        log("Using...")  ##

        from anvil.js import window
        from anvil.server import call

        Path = use("use/path/path.py")
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
                        if path.type == "py":
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
