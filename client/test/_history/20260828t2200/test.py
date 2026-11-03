def main(
    use,
    Base: type = None,
    Log: type = None,
    Path: type = None,
    anvil=None,
    log: callable = None,
    meta=None,
    path: str = None,
    tools=None,
    **kwargs,
):
    """."""

    ##log("dir(meta):", dir(meta))  ##
    ##log("meta.__module__:", meta.__module__)  ##
    ##log("dir(tools):", dir(tools))  ##
    ##log("tools.__dict__:", tools.__dict__)  ##
    ##log("tools:", tools)  ##

    js = use("use/js/js.py")
    document = use("use/document/document.py")
    window = use("use/window/window.py")

    class Use(Base):
        def __init__(self, **kwargs):

            Base.__init__(
                self,
                _cache={},
                **kwargs,
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            # Parse specifier
            path = Path(specifier)

            if path.full in self._cache:
                result = self._cache[path.full]
            else:
                node = document.createElement("div")
                node.setAttribute("__path__", path)
                message = dict(node=node)

                if meta.DEV:
                    try:
                        text = anvil.server.call(f"_{path.source}", path.full)
                        message.update(test=True)
                    except:
                        text = self._get_text(node)
                else:
                    text = self._get_text(node)
                message.update(text=text)

                if path.type == "js":
                    module = js.module(text, path=path)
                    result = module.default(
                        self,
                        dict(log=Log(path.full), meta=meta._, path=path.full, **message),
                    )

                elif path.type == "py":
                    locals = {}
                    exec(text, {}, locals)
                    result = locals["main"](
                        self,
                        Base=Base,
                        Log=Log,
                        anvil=anvil,
                        log=Log(path.full),
                        meta=meta,
                        path=path,
                        **message,
                    )
                else:
                    result = text
                self._cache[path.full] = result

            return result

        def _get_text(self, node) -> str:
            """Returns uncached text from sheet."""
            document.head.append(node)
            value = js.getComputedStyle(node).getPropertyValue(f"--__use__").strip()
            node.remove()
            text = js.atob(value[1:-1])
            return text

    use = Use()

    ##
    log("ping:", use("use/foo/ping.py")())  ##
    log("ping:", use("use/foo/ping.js")())  ##
    ##log("ping:", use("use/ping.js")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##

    window = use("use/window/window.py")

    ##use = use("use/use/use.py")

    # Set up test harness
    if meta.DEV:

        def test(path: str) -> None:
            """Runs test script."""

            # XXX TODO Use Path and add js tests

            text = anvil.server.call(f"_use", path)
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            main(
                use,
                log=Log(path),
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

    # XXX TODO Move to tests

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

    ##_()

    ##log("ping:", use("use/ping.py")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##log("pong:", use("use/pong.py").pong())  ##
