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
            caller = kwargs.get("caller")  ##
            path = specifier if isinstance(specifier, Path) else Path(specifier)
            ##log("self._hooks:", self._hooks)  ##
            ##log("path.path:", path.path)  ##
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                parcel = {}
                for hook, detail in self._hooks.items():
                    updates: dict = hook(path, **parcel)
                    if updates:
                        stop = updates.pop("stop", False)
                        parcel.update(**updates)
                        if stop:
                            break
                        ##log("parcel:", parcel)  ##

            ##log("parcel:", parcel)  ##

            ##log("path.source:", path.source)  ##
            ##log("path.type:", path.type)  ##

            key = next(
                iter(
                    [
                        a[1:]
                        for a in args
                        if isinstance(a, str) and a.startswith("?") and len(a) > 1
                    ]
                ),
                "value",
            )
            ##log("key:", key)  ##

            result = parcel.get(key)
            return result

        def hook(
            self,
        ):
            def register(cls):
                instance = cls(owner=self)
                self._hooks[instance] = {}
                return instance

            return register

    use = Use(**_use._)

    @use.hook()
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            if path.source == "use":
                result = {}
                node = document.createElement("div")
                node.setAttribute("__path__", path.relative)
                use.node.append(node)
                if use.meta.DEV:
                    try:
                        text = call("_use", path.path)
                        result.update(test=True)
                    except:
                        text = use._get_text(node)
                else:
                    text = use._get_text(node)
                result.update(node=node, text=text)
            return result

    @use.hook()
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if path.source == "use" and path.type == "py":

                result = dict(stop=True)
                locals = {}
                exec(text, {}, locals)

                def log(*args, **kwargs):
                    if use.meta.DEV:
                        args = [*args, f"\n(trace: {path.path})"]
                        print(*args)

                value = locals["main"](
                    self,
                    Base=Base,
                    log=log,
                    path=path.path,
                    **parcel,
                )

                if value is not None:

                    result.update(default="value", value=value)

                return result

    ##ping = use("use/foo/ping.py")

    ##foo = use("use/foo/foo.py", "?text")
    Foo, foo = use("use/foo/foo.py")

    log("foo:", foo)

    return use
