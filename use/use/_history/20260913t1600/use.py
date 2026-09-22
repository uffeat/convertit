def main(
    _use: callable,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> callable:
    """."""

    from anvil.js import import_from, new, window

    document = window.document

    Path = _use("use/path/path.py")
    scope = _use("use/tools/scope.py")
    dev = _use("use/tools/dev.py")

    @dev()
    def _():
        """."""
        return  ##
        log("ping():", _use("use/foo/ping.js").ping())
        log("ping():", _use("use/foo/ping.py")())
        log("ping():", _use("use/foo/ping.py")())

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._.update(_creators={}, _processors={})

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            caller = kwargs.get("caller")  ##

            specifier, *search = specifier.partition("?")

            path = Path(specifier)

            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                # Create parcel
                parcel = {}

                @scope()
                def _():
                    ##log("self._creators:", self._creators)  ##
                    def create(key):
                        registry: dict = self._creators.get(key)
                        if registry:
                            container = registry.get(path[key])
                            if container:
                                hook = container["value"]
                                updates: dict = hook(path, **parcel)
                                if updates:
                                    parcel.update(**updates)
                        return create

                    for key in self._creators.keys():
                        create(key)

            log("parcel:", parcel)  ##

                    

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

            log("self._processors:", self._processors)  ##

            result = parcel.get(key)

            return result

        def creator(self, key: str, *keys):
            def register(cls):
                registry = self._creators.get(key)
                if registry is None:
                    registry = {}
                    self._creators[key] = registry
                value = cls(owner=self, _key=key, _keys=keys)
                container = dict(value=value)
                for k in keys:
                    registry[k] = container
                return value

            return register

        def processor(self, key: str, *keys):
            def register(cls):
                registry = self._processors.get(key)
                if registry is None:
                    registry = {}
                    self._processors[key] = registry
                value = cls(owner=self, _key=key, _keys=keys)
                container = dict(value=value)
                for k in keys:
                    registry[k] = container
                return value

            return register

    use = Use(**_use)

    @use.creator("source", "app")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            from types import ModuleType

            result = {}
            parent = use.package
            for key in path.parents:
                _parent = getattr(parent, key, None)
                if isinstance(_parent, ModuleType):
                    parent = _parent
            value = getattr(parent, path.stem, None)
            if value is not None:
                result.update(default="value", value=value)
            return result

    @use.creator("source", "use")
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
                from anvil.server import call

                try:
                    text = call("_use", path.path)
                    result.update(test=True)
                except:
                    text = self._get_text(node)
            else:
                text = self._get_text(node)
            result.update(node=node, text=text)
            return result

        def _get_text(self, node) -> str:
            """Returns uncached text from sheet."""
            value = window.getComputedStyle(node).getPropertyValue("--__use__").strip()
            text = window.atob(value[1:-1])
            return text

    @use.creator("type", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                Log = use("app/tools/log.py").Log
                result = {}
                locals = {}
                exec(text, {}, locals)
                value = locals["main"](
                    self,
                    Base=Base,
                    log=Log(path.path),
                    path=path.path,
                    **parcel,
                )
                if value is not None:
                    result.update(default="value", value=value)
                return result

    @use.processor("value", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            value = parcel.get("value")
            if isinstance(value, dict):
                return window.Object.freeze(value)

    @use.processor("text", "json")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """."""
            import json

            text = parcel.get("text")
            return json.loads(text)

    @dev()
    def _():
        """."""
        return  ##
        log("ping():", use("use/foo/ping.py")())
        log("ping():", use("use/foo/ping.py")())

        ##foo = use("use/foo/foo.py", "?text")

    @dev()
    def _():
        """."""
        return  ##
        Foo, foo = use("use/foo/foo.py")
        log("foo:", foo)

    @dev()
    def _():
        """."""
        foo = use("use/foo/foo.json")
        log("foo:", foo)

    return use
