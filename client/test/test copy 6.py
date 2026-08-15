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
            # Create top-level container
            node = self.document.createElement("div")
            node.attachShadow(dict(mode="open"))
            slot = self.document.createElement("slot")
            node.shadowRoot.append(slot)
            node.id = "use"
            self.document.body.append(node)
            # Update state
            self._.update(node=node, source=self.Registry(owner=self))

        def __call__(self, specifier: str, *args, key="value", **kwargs):
            """Returns parcel member."""
            path = Path(specifier)
            # Get parcel
            if path.full in self._cache:
                # Retrieve parcel
                parcel: dict = self._cache[path.full]
            else:
                # Build parcel
                source = self.source[path.source]
                if not source:
                    raise ValueError(f"Invalid source: {path.source}.")
                parcel: dict = source(path)
                self._cache[path.full] = parcel
            
            member = parcel.get(key)
            return member

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
            use.node.append(node)
            self._.update(node=node)

        def __call__(self, path) -> dict:
            """Returns parcel."""
            ##log("key:", self.key)##
            parcel = dict()
            node = use.document.createElement("div")
            node.setAttribute("__path__", path.path)
            self.node.append(node)
            message = {}
            if use.meta.DEV:
                try:
                    text = use.anvil.server.call(f"_{self.key}", path.full)
                    message.update(test=True)
                except use.anvil.server.UplinkDisconnectedError as error:
                    text = self._get_text(node=node, path=path)
            else:
                text = self._get_text(node=node, path=path)
            transpile = self.transpiler[path.type]
            if transpile:
                value = transpile(path=path, text=text, **message)
                if value is None:
                    parcel.update(value=text)
                else:
                    parcel.update(value=value, text=text)
            else:
                parcel.update(value=text)
            parcel.update(node=node)
            return parcel

        def _get_text(self, node=None, path=None) -> str:
            """Returns uncached text from sheet."""
            value = (
                use.js.getComputedStyle(node)
                .getPropertyValue(f"--__{self.key}__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid path: {path.full}.")
            text = use.js.atob(value[1:-1])
            return text

    use_source = use.source["use"]

    ##use_source = use.source("use", UseSource)
    ##log("use_source:", use_source)  ##

    @use_source.transpiler("py")
    class Transpiler(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, path=None, test=False, text=None):
            """Returns transpiled value."""
            locals = {}
            exec(text, {}, locals)
            main = locals.pop("main", None)
            if main:
                value = main(
                    use, log=Log(path=path.full), path=path.full, test=test, **locals
                )
                if isinstance(value, dict):
                    value = use.js.freeze(value)
            else:
                value = use.js.freeze(locals)
            return value

    log("ping:", use("use/ping.py")())
    log("text:", use("use/ping.py", key="text"))

    log("foo.html:", use("use/foo/foo.html"))

    Foo, foo = use("use/foo/foo.py")
    log("Foo.foo:", Foo().foo)

    use("use/foo/bar/bar.py").bar()

    ##use("bad/ping.py")
