def main(
    use: callable,
    anvil=None,
    console=None,
    document=None,
    js=None,
    log=None,
    meta=None,
    window=None,
    **kwargs,
) -> callable:
    """."""
    Base = use("/tools/base.py")
    instantiate = use("/tools/instantiate.py")
    Path = use("/path/path.py")

    class Registry(Base):
        def __init__(self, owner=None):
            Base.__init__(self, owner=owner, _registry={})

        def __call__(self, key):
            """."""

            def register(handler):

                return self.add(key, handler)

            return register

        def __getitem__(self, key):
            """."""
            registry: dict = self._["_registry"]
            container = registry.get(key)

            if container:
                handler = container[0]
                if isinstance(handler, type):
                    handler = handler(owner=self.owner)
                    container[0] = handler
                return handler

        def add(self, key, handler):
            registry: dict = self._["_registry"]
            container = [handler]
            registry[key] = container
            return handler

    class Use(Base):
        def __init__(self):
            Base.__init__(
                self,
                _cache={},
                _public=dict(
                    sources=Registry(owner=self),
                    transpilers=Registry(owner=self),
                ),
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """."""
            _cache: dict = self._["_cache"]

            path = Path(specifier)
            key = str(path)  # Full path

            if key in _cache:
                parcel = _cache[key]
            else:

                source = self.sources[path.source]
                if not source:
                    raise ValueError(f"No {path.source} source registered.")
                result: dict = source(key)

                transpile = self.transpilers[path.type]
                if not transpile:
                    raise TypeError(f"No transpiler for {path.type}.")

                value = transpile(self, path=key, **result)
                parcel = dict(value=value, **result)
                _cache[key] = parcel

            if kwargs.pop("raw", False):
                return parcel["text"]
            return parcel["value"]

        def __getattr__(self, key):
            """."""
            _public: dict = self._["_public"]
            return _public[key]

    use = Use()

    @use.sources("/")
    class cls(Base):

        def __init__(self, owner=None):
            Base.__init__(self, owner=owner)

        def __call__(self, path: str) -> tuple:
            """."""
            result = dict()
            if meta.DEV:
                try:
                    text = anvil.server.call("_use", path)
                    result.update(test=True, text=text)
                    log(f"Got {path} from local server.", trace="create")  ##
                except anvil.server.UplinkDisconnectedError as error:
                    result.update(self._get(path))
                    log(f"Got {path} from sheet.", trace="create")  ##
            else:
                result.update(self._get(path))
            return result

        @staticmethod
        def _get(path: str) -> str:
            """Returns uncached parcel text from sheet."""
            node = document.createElement("div")
            node.setAttribute("__path__", path)
            document.head.append(node)
            value = js.getComputedStyle(node).getPropertyValue("--__use__").strip()
            if not value:
                raise ValueError(f"Invalid {path}.")
            node.remove()
            text = js.atob(value[1:-1])
            return dict(node=node, text=text)

    @use.transpilers("py")
    class cls(Base):

        def __init__(self, owner=None):
            Base.__init__(self, owner=owner)

        def __call__(
            self, use, node=None, path: str = None, text: str = None, test: bool = None
        ):
            """Returns transpiled parcel."""
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            if main:

                def log(*args):
                    """."""
                    if meta.DEV:
                        args = [*args, f"({path})"]
                        print(*args)
                    

                result = main(
                    use,
                    anvil=anvil,
                    console=console,
                    document=document,
                    js=js,
                    log=log,
                    meta=meta,
                    node=node,
                    path=path,
                    test=test,
                    window=window,
                )

                if isinstance(result, tuple):
                    result = {a.__name__: a for a in result}

                if isinstance(result, (dict, list)):
                    result = js.freeze(result)
                

                return result

            else:
                result = js.freeze(locals)

            return result

    ping = use("/ping.py")
    print("ping:", ping())

    ping = use("/ping.py")
    print("ping:", ping())

    raw = use("/ping.py", raw=True)
    log("raw:", raw)

    raw = use("/ping.py", raw=True)
    ##log("raw:", raw)

    use("/foo/foo.py").foo()
    print("foo:", use("/foo/foo.py").Foo().foo)

    return use
