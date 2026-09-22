def main(
    _use: callable,
    Base: type = None,
    Log: callable = None,
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
            self._.update(_effect={}, _processor={}, _source={}, _type={})

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            caller = kwargs.get("caller")  ##
            path = specifier if isinstance(specifier, Path) else Path(specifier)
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                parcel = {}

                def update():
                    """."""


                item = self._source.get(path.source)
                if item:
                    hook = item["value"]
                    updates: dict = hook(path, **parcel)
                    if updates:
                        parcel.update(**updates)

                item = self._type.get(path.type)
                if item:
                    hook = item["value"]
                    updates: dict = hook(path, **parcel)
                    if updates:
                        parcel.update(**updates)

            

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

        def hook(self, name: str, *keys):
            def register(cls):
                registry = self[f"_{name}"]
                value = cls(owner=self, keys=keys)
                item = dict(value=value)
                for key in keys:
                    registry[key] = item
                return value

            return register

    use = Use(**_use._)

    @use.hook("source", "use")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            result = {}
            node = document.createElement("div")
            node.setAttribute("__path__", path.relative)
            use.node.append(node)
            if use.meta.DEV:
                try:
                    text = call("_use", path.path)
                    result.update(test=True)
                except:
                    text = self._get_text(node)
            else:
                text = self._get_text(node)
            result.update(node=node, text=text)
            return result

        @staticmethod
        def _get_text(node) -> str:
            """Returns uncached text from sheet."""
            value = window.getComputedStyle(node).getPropertyValue("--__use__").strip()
            text = window.atob(value[1:-1])
            return text

    @use.hook("type", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                result = {}
                locals = {}
                exec(text, {}, locals)
                value = locals["main"](
                    self,
                    Base=Base,
                    Log=Log,
                    log=Log(path.path),
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
