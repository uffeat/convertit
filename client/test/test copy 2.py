def main(
    Base: type = None,
    anvil=None,
    log: callable = None,
    **kwargs,
):
    """."""

    class Use(Base):
        def __init__(self, **kwargs):
            DEV = (anvil.app.environment.name == "development")
            Base.__init__(self, _cache={},  DEV=DEV,**kwargs)
           

        def __call__(self, path: str, *args, **kwargs):
            """Returns result from import engine."""
            if path in self._cache:
                parcel = self._cache[path]
                
            else:
                parcel = {}

                if self.DEV:
                    try:
                        text = anvil.server.call(f"_use", path)
                    except:
                        text = self._get_text(path)
                else:
                    text = self._get_text(path)

                parcel.update(text=text)
                if path.endswith(".py"):
                    locals = {}
                    exec(text, {}, locals)
                    value =  locals["main"](self, Base=Base, anvil=anvil)
                    parcel.update(value=value) 
                elif path.endswith(".js"):
                    ...
                self._cache[path] = parcel

            result = parcel.get(kwargs.get('key', 'value'))
            return result

        def _get_text(self, path) -> str:
            """Returns uncached text from sheet."""
            node = anvil.window.document.createElement("div")
            node.setAttribute("__path__", path)
            anvil.window.document.head.append(node)
            value = (
                anvil.window.getComputedStyle(node)
                .getPropertyValue(f"--__use__")
                .strip()
            )
            node.remove()
            text = anvil.window.atob(value[1:-1])
            return text

    use = Use()

    use = use("use/use/use.py")
    

    # Set up test harness
    if meta.DEV:

        def test(path: str) -> None:
            """Runs test script."""
            text = anvil.server.call(f"_test", path)
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            main(
                use,
                log=Log(path=path),
                path=path,
                test=True,
            )

        @window.on()
        def keydown(event):
            if event.code == "KeyU" and event.shiftKey:
                stored = js.localStorage.getItem("__test__")
                path = window.prompt("Path:", stored)
                if path:
                    js.localStorage.setItem("__test__", path)
                    test(path)

    def _():

        Foo, foo = use("use/foo/foo.py")
        log("foo:", foo())
        ##log("text:", use("use/foo/foo.py", key="text"))
        log("html:", use("use/foo/foo.html"))

        foo = use("use/foo/foo.json")
        foo["foo"] = 43
        log("json:", foo)
        log("json:", use("use/foo/foo.json"))
        log("json:", use("use/foo/foo.json", key="text"))

        ##use("use/foo/bar/bar.py").bar()
        ##log("node:", use("use/foo/bar/bar.py").node)

    _()

    log("ping:", use("use/ping.py")())  ##
    log("ping:", use("use/ping.py")())  ##

    log("pong:", use("use/pong.py").pong())  ##
