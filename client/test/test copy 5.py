def main(
    Base: type = None,
    Log: type = None,
    Path: callable = None,
    anvil=None,
    console=None,
    document=None,
    js=None,
    log: callable = None,
    meta=None,
    path: str = None,
    window=None,
    server=None,
    **kwargs,
):
    """."""

    class Registry(Base):
        def __init__(self, owner=None):
            Base.__init__(
                self,
                owner=owner,
                _registry={},
            )

        def __call__(self, key, *args, **kwargs):
            """Registers callable."""
            # NOTE Register mutable to allow lazy instantiation
            value = args[0] if args else None
            if value:
                if isinstance(value, type):
                    value = value(key=key, owner=self)
                self._registry[key] = dict(value=value)
                return value

            def register(value: type):
                self._registry[key] = dict(value=value)
                return value

            return register

        def __getitem__(self, key):
            """Returns registree instance."""
            _registry: dict = self._["_registry"]
            source = _registry.get(key)
            if source:
                value = source["value"]
                if isinstance(value, type):
                    value = value(key=key, owner=self)
                    source["value"] = value
                return value

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)
            node = self.document.createElement("div")
            node.id = "use"
            self.document.head.append(node)
            self._.update(node=node, source=self.Registry(owner=self))

        def __call__(self, specifier: str, *args, key="value", **kwargs):
            """."""
            path = Path(specifier)
            # Get parcel
            if path.full in self._cache:
                # Retrieve parcel
                parcel = self._cache[path.full]
            else:
                # Build parcel
                source = self.source[path.source]
                if source:
                    parcel = source(path)
                    self._cache[path.full] = parcel
                else:
                    log(f"Invalid source: {path.source}", native="error")
                    parcel = dict()
            # Return parcel value
            return parcel.get(key)

    use = Use(
        Base=Base,
        Path=Path,
        Log=Log,
        Registry=Registry,
        anvil=anvil,
        console=console,
        document=document,
        js=js,
        meta=meta,
        window=window,
    )

    @use.source("use")
    class UseSource(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, transpiler=use.Registry(), **kwargs)
            node = use.document.createElement("div")
            node.setAttribute("source", self.key)
            use.document.head.append(node)
            self._.update(node=node)

        def __call__(self, path) -> dict:
            """."""
            ##log("key:", self.key)##
            parcel = dict()

            if use.meta.DEV:
                try:
                    text = use.anvil.server.call(f"_{self.key}", path.full)
                except use.anvil.server.UplinkDisconnectedError as error:
                    text = self._get_text(path)
            else:
                text = self._get_text(path)

            transpile = self.transpiler[path.type]
            if transpile:
                value = transpile(path=path, text=text)
                if value is not None:
                    parcel.update(value=value)

            parcel.update(text=text)

            return parcel

        def _get_text(self, path) -> str:
            """Returns uncached text from sheet."""
            node = use.document.createElement("div")
            node.setAttribute("__path__", path.path)
            use.document.head.append(node)
            value = (
                use.js.getComputedStyle(node)
                .getPropertyValue(f"--__{self.key}__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid {path.full}.")

            text = use.js.atob(value[1:-1])
            return text

    use_source = use.source["use"]

    ##use_source = use.source("use", UseSource)
    log("use_source:", use_source)

    @use_source.transpiler("py")
    class Transpiler(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, path=None, test=False, text=None):
            """."""
            locals = {}
            exec(text, {}, locals)
            main = locals["main"]
            value = main(use, log=Log(path=path.full), path=path.full, test=test)
            return value

    log("ping:", use("use/ping.py")())
    log("text:", use("use/ping.py", key="text"))

    ##use("bad/ping.py")
