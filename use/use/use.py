def main(
    _use: callable,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> callable:
    """."""

    ##ping = _use('use/foo/ping.py')
    ##log('ping():', ping())
    ##log('ping():', ping())

    from anvil.server import call
    from anvil.js import import_from, new, window

    document = window.document

    Path = _use("use/path/path.py")

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._.update(_hooks={})

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            caller = kwargs.get("caller")

            path = specifier if isinstance(specifier, Path) else Path(specifier)
            
            log("path.path:", path.path)  ##
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                parcel = {}
                self._cache[path.path] = parcel

            ##log("path.source:", path.source)  ##
            ##log("path.type:", path.type)  ##

            key = next(
                iter(
                    [
                        a[1:]
                        for a in args
                        if isinstance(a, str) and a.startswith(".") and len(a) > 1
                    ]
                ),
                "value",
            )
            log("key:", key)  ##

            if key not in parcel:
                hook = self._hooks.get(key)
                if hook:
                    updates = hook(path, **parcel)
                    if updates:
                        parcel.update(updates)
                        return self(path)

            result = parcel.get(key)
            return result

        def hook(self, cls):
            """."""
            hook = cls(owner=self)
            self._hooks[cls.key] = hook
            return hook

    use = Use(**_use._)

    @use.hook
    class cls(Base):

        key = "value"

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel):
            """."""
            
   

    ping = use("use/foo/ping.py")

    foo = use("use/foo/foo.py", ".node")
    log("foo:", foo)

    return use
