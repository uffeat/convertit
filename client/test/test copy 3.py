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

        def __call__(self, key, value=None):
            """Registers callable."""
            # NOTE Register mutable to allow lazy instantiation
            if value:
                _registry: dict = self._["_registry"]
                _registry[key] = dict(value=value)
            else:

                def register(value: type):
                    # XXX Must get _registry in function scope!
                    _registry: dict = self._["_registry"]
                    _registry[key] = dict(value=value)
                    return value

                return register

        def __getitem__(self, key):
            """Returns registree instance."""
            _registry: dict = self._["_registry"]
            source = _registry.get(key)
            if source:
                value = source["value"]
                if isinstance(value, type):
                    value = value(key=key, owner=self.owner)
                    source["value"] = value
                return value

    class Use(Base):
        def __init__(self):

            Base.__init__(
                self,
                _cache={},
                source=Registry(owner=self)
            )

        def __call__(self, specifier: str, *args, key="value", **kwargs):
            """."""
            _cache: dict = self._["_cache"]
            path = Path(specifier)

            # Get parcel
            if path.full in _cache:
                # Retrieve parcel
                parcel = _cache[path.full]
            else:
                # Build parcel
                parcel = dict(path=path.path)
                source = self.source[path.source]
                if source:
                    source(parcel, path=path)
                    _cache[path.full] = parcel
            # Return parcel value
            return parcel.get(key)

        @property
        def Base(self):
            return Base

        @property
        def Log(self):
            return Log

        @property
        def Path(self):
            return Path

        @property
        def anvil(self):
            return anvil

        @property
        def console(self):
            return console

        @property
        def document(self):
            return document

        @property
        def js(self):
            return js

        @property
        def meta(self):
            return meta

        @property
        def source(self) -> Registry:
            return self._["source"]

        @property
        def window(self):
            return window

        

    use = Use()

    @use.source("tools")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(
                self,
                _members={
                    "/base.py": Base,
                    "/log.py": Log,
                    "/path.py": Path,
                    "/anvil.py": anvil,
                    "/console.py": console,
                    "/document.py": document,
                    "/js.py": js,
                    "/window.py": window,
                },
                **kwargs
            )

        def __call__(self, parcel: dict, path=None):
            """."""
            _members: dict = self._["_members"]
            value = _members.get(path.path)
            if value is not None:
                parcel["value"] = value





    @use.source("use")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, transpiler=Registry(), **kwargs)

        def __call__(self, parcel: dict, path=None):
            """."""
            
            if use.meta.DEV:
                try:
                    text = use.anvil.server.call("_use", path.path)
                except use.anvil.server.UplinkDisconnectedError as error:
                    text = self._get_text(path.path)
            else:
                text = self._get_text(path.path)

            parcel['text'] = text


        @property
        def transpiler(self) -> Registry:
            return self._["transpiler"]



        def _get_text(self, path: str) -> str:
            """Returns uncached text from sheet."""
            node = use.document.createElement("div")
            node.setAttribute("__path__", path)
            use.document.head.append(node)
            value = (
                use.js.getComputedStyle(node)
                .getPropertyValue("--__use__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid {path}.")
            node.remove()
            text = use.js.atob(value[1:-1])
            return text

    print('tools:', use.source['tools'])
    print('Log:', use("tools/log.py"))


    print('text:', use("use/ping.py", key='text'))
