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

        def __call__(self, key, *args):
            """Registers callable."""
            # NOTE Register mutable to allow lazy instantiation
            value = args[0] if args else None
            if value:
                # Not used as decorator
                if isinstance(value, type):
                    value = value(key=key, owner=self)
                self._registry[key] = dict(value=value)
                return value
            # Used as decorator
            def register(value: type):
                self._registry[key] = dict(value=value)
                return value

            return register

        def __getitem__(self, key):
            """Returns registree instance."""
            source = self._registry.get(key)
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

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            path = Path(specifier)
            # Get result
            if path.full in self._cache:
                # Retrieve result
                result: dict = self._cache[path.full]
            else:
                # Build result
                source = self.source[path.source]
                if not source:
                    raise ValueError(f"Invalid source: {path.source}.")
                result: dict = source(path)
                nocache = result.get("nocache", False)
                if nocache is False:
                    self._cache[path.full] = result

            # Process

            member = result.get(kwargs.get("key", "value"))
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
                nocache = getattr(transpile.__class__, "nocache", False)
                if nocache:
                    parcel.update(nocache=nocache)
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

    @use_source.transpiler("json")
    class Transpiler(use.Base):

        nocache = True

        def __init__(self, **kwargs):
            use.Base.__init__(self, **kwargs)

        def __call__(self, path=None, test=False, text=None):
            """Returns transpiled value."""
            import json

            value = json.loads(text)
            return value

    log("ping:", use("use/ping.py")())
    log("ping:", use("use/ping.py")())
    log("text:", use("use/ping.py", key="text"))

    log("foo.html:", use("use/foo/foo.html"))

    Foo, foo = use("use/foo/foo.py")
    log("Foo.foo:", Foo().foo)

    use("use/foo/bar/bar.py").bar()

    foo_json = use("use/foo/foo.json")
    log("foo_json:", foo_json)
    foo_json["foo"] = 44

    foo_json = use("use/foo/foo.json")
    log("foo_json:", foo_json)

    ##use("bad/ping.py")
