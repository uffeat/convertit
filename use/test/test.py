def main(
    use,
    Base: type = None,
    log: callable = None,
    path: str = None,
    state: dict = None,
    **kwargs,
):
    """."""
    from anvil.js import window
    from anvil.server import call

    Log = use("use/log/log.py")
    Py = use("use/use/py.py")

    def main(*args, **kwargs):

        ##log("Loading", path) ##

        if state.get("used"):
            return
        state.update(used=True)
        ##log("Using...")  ##

        def test(specifier: str, **kwargs):
            """."""
            path = use.Path(specifier)
            try:
                text = call("_use", path.path)
            except:
                return window.console.error(f"Invalid path:", path.path)

            if path.type == "py":

                constructed = Py(text=text, use=use)(
                    Base=Base,
                    log=Log(path.path),
                    path=path.path,
                    test=test,
                    text=text,
                )

                if kwargs.get('text'):
                    return text

                return constructed["value"]

            if path.type == "js":
                Construct = use.package.client.tools.Construct
                result = Construct(path=path.path, text=text, use=use)(
                    path=path.path,
                    test=test,
                    text=text,
                )
                return result

            return text

        def keydown(event):

            if event.code == "KeyU" and event.shiftKey:
                stored = window.localStorage.getItem("__test__")
                path = window.prompt("Path:", stored)
                if path:
                    window.localStorage.setItem("__test__", path)
                    test(path)

        window.addEventListener("keydown", keydown)

    return main
