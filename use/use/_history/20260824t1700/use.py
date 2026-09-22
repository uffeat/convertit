def main(
    use: callable,
    Base=None,
    Log=None,
    Path=None,
    anvil=None,
    console=None,
    document=None,
    js=None,
    log=None,
    meta=None,
    path: str = None,
    window=None,
    **kwargs,
) -> callable:
    """."""
   


    log = Log(path=path)
    

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
                    anvil=anvil,
                    console=console,
                    document=document,
                    js=js,
                    meta=meta,
                    sources=Registry(owner=self),
                    transpilers=Registry(owner=self),
                    window=window,
                ),
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """."""
            _cache: dict = self._["_cache"]

            path = Path(specifier)
            key = str(path)  # Full path

            # Get parcel
            if key in _cache:
                parcel = _cache[key]
            else:
                # Build parcel
                source = self.sources[path.source]
                if source:
                    parcel: dict = source(path=key)
                    transpile = self.transpilers[path.type]
                    if transpile:
                        value = transpile(path=key, **parcel)
                        parcel.update(value=value)
                    else:
                        value = parcel.pop("text")
                        parcel.update(value=value)
                    _cache[key] = parcel

            # Deliver from parcel
            key = next(iter([k for k, v in kwargs.items() if v is True]), "value")
            log("key:", key)  ##
            return parcel.get(key)

        def __getattr__(self, key):
            """."""
            _public: dict = self._["_public"]
            return _public[key]

    use = Use()

    @use.sources("/")
    class cls(Base):

        def __init__(self, owner=None):
            Base.__init__(self, owner=owner)

        def __call__(self, path: str=None) -> dict:
            """."""
            if self.owner.meta.DEV:
                try:
                    text = self.owner.anvil.server.call("_use", path)
                    parcel = dict(test=True, text=text)
                    log(f"Got {path} from local server.")  ##
                except self.owner.anvil.server.UplinkDisconnectedError as error:
                    parcel = self._get(path)
                    log(f"Got {path} from sheet.")  ##
            else:
                parcel = self._get(path)
            return parcel

        def _get(self, path: str) -> dict:
            """Returns uncached parcel from sheet."""
            node = self.owner.document.createElement("div")
            node.setAttribute("__path__", path)
            self.owner.document.head.append(node)
            value = (
                self.owner.js.getComputedStyle(node)
                .getPropertyValue("--__use__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid {path}.")
            node.remove()
            text = self.owner.js.atob(value[1:-1])
            parcel = dict(node=node, text=text)
            return parcel

    @use.transpilers("py")
    class cls(Base):

        def __init__(self, owner=None):
            Base.__init__(self, owner=owner)

        def __call__(
            self, node=None, path: str = None, text: str = None, test: bool = None
        ):
            """Returns transpiled parcel."""
            locals = {}
            exec(text, {}, locals)
            main = locals.get("main")
            if main:

                log = Log(path=path)

                result = main(
                    self.owner,
                    anvil=self.owner.anvil,
                    console=self.owner.console,
                    document=self.owner.document,
                    js=self.owner.js,
                    log=log,
                    meta=self.owner.meta,
                    node=node,
                    path=path,
                    test=test,
                    window=self.owner.window,
                )

                if isinstance(result, tuple):
                    result = {a.__name__: a for a in result}

                if isinstance(result, (dict, list)):
                    result = self.owner.js.freeze(result)

                return result

            else:
                result = self.owner.js.freeze(locals)

            return result

    ping = use("/ping.py")
    print("ping:", ping())

    ping = use("/ping.py")
    print("ping:", ping())

    raw = use("/ping.py", text=True)
    log("raw:", raw)

    raw = use("/ping.py", text=True)
    ##log("raw:", raw)

    ##use("/foo/foo.py").foo()
    ##print("foo:", use("/foo/foo.py").Foo().foo)

    return use
