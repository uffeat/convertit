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
            _processors = {}
            _transpilers = {}

            Base.__init__(
                self,
                _cache={},
                DEV=anvil.app.environment.name == "development",
                processor=lambda key: lambda process: _processors.update(
                    **{key: process}
                ),
                _processors=_processors,
                transpiler=lambda key: lambda transpile: _transpilers.update(
                    **{key: transpile}
                ),
                _transpilers=_transpilers,
                **kwargs,
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            session = dict(caller=kwargs.get("caller", self.path))
            
            session = anvil.window.Object.freeze(session)
            self._["_session"] = session
            # Parse specifier
            source, *path = specifier.partition("/")
            path = "".join(path)
            *_, suffix = path.rpartition(".")

            if specifier in self._cache:
                parcel = self._cache[specifier]
            else:
                # Create parcel
                node = anvil.window.document.createElement("div")
                node.setAttribute("__path__", path)
                parcel = dict(node=node)
                if self.DEV:
                    try:
                        text = anvil.server.call(f"_use", specifier)
                    except:
                        text = self._get_text(node)
                else:
                    text = self._get_text(node)
                parcel.update(text=text)
                transpile = self._transpilers.get(suffix)
                if transpile:
                    parcel.update(default="load", load=transpile(text, specifier))
                self._cache[specifier] = parcel
            # Extract result from parcel
            key = kwargs.get("key", parcel.get("default", "text"))
            result = parcel.get(kwargs.get("key", parcel.get("default", "text")))
            if key == "load":
                result = result(session)

            process = self._processors.get(suffix)
            if process:
                processed = process(result, *args, **kwargs)
                if processed is not None:
                    result = processed

            return result

        def session(self):
            """."""
            return self._.get("_session")

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

    use = Use(path=path)

    @use.transpiler("js")
    def transpile(text, path):
        text = f"{text}\n//# sourceURL={path}"
        blob = anvil.js.new(anvil.window.Blob, [text], dict(type="text/javascript"))
        url = anvil.window.URL.createObjectURL(blob)
        module = anvil.js.import_from(url)
        anvil.window.URL.revokeObjectURL(url)

        def _use(specifier, *args):
            kwargs = next(iter([a for a in args if hasattr(a, "keys")]), {})
            if kwargs:
                args = list(args)
                args.remove(kwargs)
            return use(specifier, *args, caller=path, **kwargs)

        return module.default(
            _use, dict(log=Log(path=path), owner=use, path=path, session=use.session)
        )

    @use.transpiler("py")
    def transpile(text, path):
        locals = {}
        exec(text, {}, locals)

        def _use(*args, **kwargs):
            return use(*args, caller=path, **kwargs)

        return locals["main"](
            _use,
            Base=Base,
            Log=Log,
            anvil=anvil,
            log=Log(path=path),
            owner=use,
            path=path,
            session=use.session,
        )


    def scope(target):
        return target()

    @scope
    def _():



    

        js = use("use/js/js.py")

        @use.processor("py")
        def process(result, *args, **kwargs):
            """."""
            if 'text' not in kwargs:
                if isinstance(result, dict):
                    return js.freeze(result)

    ##use.processor("py")(process)
    ##use.processor("js")(process)

    ##
    log("ping:", use("use/ping.js")())  ##
    log("ping:", use("use/ping.py")())  ##
    log("ping:", use("use/ping.py")())  ##
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
