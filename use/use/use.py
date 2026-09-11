def main(
    _use: callable,
    log: callable = None,
    path: str = None,
    tools=None,
    **kwargs,
) -> callable:
    """."""
    from types import ModuleType

    from anvil.server import call
    from anvil.js import import_from, new, window

    Base = tools.base.Base
    Log = tools.log.Log

    window.Object.defineProperty(
        _use,
        "foo",
        dict(
            configurable=False,
            enumerable=True,
            writable=False,
            value=42,
        ),
    )

    log("ping():", _use("use/foo/ping.js")())
    ping = _use("use/foo/ping.py")
    log("ping():", ping())
    log("ping():", ping())

    document = window.document

    log("tools.__dict__:", tools.__dict__)

    Path = _use("use/path/path.py")

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._.update(_registry={})

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            caller = kwargs.get("caller")  ##
            path = Path(specifier)
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                # Create parcel
                parcel = {}
                log("self._registry:", self._registry)  ##
                def update(key):
                    registry: dict = self._registry.get(key)
                    if registry:
                        container = registry.get(path[key])
                        if container:
                            hook = container["value"]
                            updates: dict = hook(path, **parcel)
                            if updates:
                                parcel.update(**updates)
                    return update
                update("source")("type")

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

        def hook(self, key: str, *keys):
            def register(cls):
                registry = self._registry.get(key)
                if registry is None:
                    registry = {}
                    self._registry[key] = registry
                value = cls(owner=self, _key=key, _keys=keys)
                container = dict(value=value)
                for k in keys:
                    registry[k] = container
                return value

            return register

    use = Use(**_use)

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

    @use.hook("value", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            value = parcel.get('value')
            if isinstance(value, dict):
                return window.Object.freeze(value)


    @use.hook("text", "json")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            import json
            text = parcel.get('text')
            return json.loads(text)
            

    ##ping = use("use/foo/ping.py")

    ##foo = use("use/foo/foo.py", "?text")
    Foo, foo = use("use/foo/foo.py")

    log("foo:", foo)

    return use
