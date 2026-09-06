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


            log("self._hooks:", self._hooks)  ##



            log("path.path:", path.path)  ##
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                parcel = {}
                self._cache[path.path] = parcel

                registry = self._hooks.get('source')
                if registry:

                    hook = registry.get(path.source)
                    if hook:

                        log("hook:", hook)  ##


                        updates = hook(path, **parcel)
                        if updates:
                            parcel.update(**updates)

            return parcel  ##

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
                        parcel.update(**updates)
                        return self(path)

            result = parcel.get(key)
            return result

        def hook(self, cls):
            """."""
            registry = getattr(cls, "registry", None)
            keys = getattr(cls, "keys", None)
            if registry not in self._hooks:
                self._hooks[registry] = {}
            registry = self._hooks[registry]
            hook = cls(owner=self)
            for key in keys:
                registry[key] = hook

    use = Use(**_use._)

    @use.hook
    class cls(Base):

        registry = "source"
        keys = ("use",)

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            result = dict(node=None, text=None)
            return result

    ping = use("use/foo/ping.py")

    foo = use("use/foo/foo.py", ".node")
    log("foo:", foo)

    return use
