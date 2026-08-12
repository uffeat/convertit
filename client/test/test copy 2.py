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

    class Use(Base):
        def __init__(self):

            Base.__init__(
                self,
                _cache={},
                _sources={},
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
                _sources: dict = self._["_sources"]
                parcel = dict(path=path.path)
                source = _sources.get(path.source)
                if source:
                    value = source["value"]
                    if isinstance(value, type):
                        value = value(key=path.source, owner=self)
                        source["value"] = value
                    value(parcel)
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
        def window(self):
            return window

        def source(self, key, value=None):
            """."""
            # NOTE Register mutable to allow lazy instantiation
            if value:
                _sources: dict = self._["_sources"]
                _sources[key] = dict(value=value)
            else:

                def register(value: type):
                    # XXX Get _sources in function scope!
                    _sources: dict = self._["_sources"]
                    _sources[key] = dict(key=key, value=value)
                    return value

                return register

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

        def __call__(self, parcel: dict):
            """."""
            _members: dict = self._["_members"]
            value = _members.get(parcel["path"])
            if value is not None:
                parcel["value"] = value


    class UseSource(Base):
        def __init__(self):
        
            Base.__init__(
                self,
                _cache={},
                _sources={},
            )




    @use.source("use")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, parcel: dict):
            """."""

   

    print('Log:', use("tools/log.py"))
