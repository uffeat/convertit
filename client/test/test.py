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
                _tools=dict(
                    Base=Base,
                    Log=Log,
                    Path=Path,
                    anvil=anvil,
                    console=console,
                    document=document,
                    js=js,
                    meta=meta,
                    window=window,
                ),
            )

        def __call__(self, specifier: str, *args, key="value", **kwargs):
            """."""
            _cache: dict = self._["_cache"]

            path = Path(specifier)

            # Get parcel
            if path.full in _cache:
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

        def source(self, key, value=None):
            """."""
            _sources: dict = self._["_sources"]
            if value:
                _sources[key] = dict(key=key, value=value)
            else:

                def register(value: type):
                    _sources[key] = dict(key=key, value=value)
                    return value

                return register

    use = Use()


    @use.source('use')
    class cls(Base):
        def __init__(self):
            Base.__init__(self)

