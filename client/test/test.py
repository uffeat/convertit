def main(
    Base: type = None,
    Log: type = None,
    anvil=None,
    log: callable = None,
    path: str = None,
    **kwargs,
):
    """."""
    ##from types import MappingProxyType

    class Use(Base):
        def __init__(self, **kwargs):

            DEV = anvil.app.environment.name == "development"

            class Meta:
                @property
                def DEV(self):
                    return DEV

            Base.__init__(
                self,
                _cache={},
                meta=Meta(),
                **kwargs,
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            # Parse specifier
            source, *path = specifier.partition("/")
            path = "".join(path)
            *_, suffix = path.rpartition(".")

            if specifier in self._cache:
                result = self._cache[specifier]
            else:
                node = anvil.window.document.createElement("div")
                node.setAttribute("__path__", path)

                message = dict(node=node, path=specifier)

                if self.meta.DEV:
                    try:
                        text = anvil.server.call(f"_{source}", specifier)
                        message.update(test=True)
                    except:
                        text = self._get_text(node)
                else:
                    text = self._get_text(node)
                message.update(text=text)

                if suffix == "js":
                    text = f"{text}\n//# sourceURL={path}"
                    blob = anvil.js.new(
                        anvil.window.Blob, [text], dict(type="text/javascript")
                    )
                    url = anvil.window.URL.createObjectURL(blob)
                    module = anvil.js.import_from(url)
                    anvil.window.URL.revokeObjectURL(url)
                    result = module.default(self, dict(**message))
                elif suffix == "py":
                    locals = {}
                    exec(text, {}, locals)
                    result = locals["main"](
                        self,
                        Base=Base,
                        Log=Log,
                        anvil=anvil,
                        log=Log(path=specifier),
                        **message,
                    )
                else:
                    result = text
                self._cache[specifier] = result

            return result

        def _get_text(self, node) -> str:
            """Returns uncached text from sheet."""
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

    ##
    log("ping:", use("use/foo/ping.py")())  ##
    ##log("ping:", use("use/ping.js")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##log("ping:", use("use/ping.py")())  ##
    ##

    Path = use("use/path/path.py")
    js = use("use/js/js.py")
    meta = use("use/meta/meta.py")
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
