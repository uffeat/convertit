def main(
    use: callable,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> callable:
    """."""

    from anvil.js import import_from, new, window

    document = window.document

    Path = use("use/path/path.py")
    typeName = use("use/type/name.js")
    scope = use("use/tools/scope.py")

    log("use.meta.DEV:", use.meta.DEV)  ##

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._.update(_creators={}, _processors={})

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            args = self._parse(args, kwargs)
            path = Path(specifier)
            parcel = self._create(path)
            ##log("parcel:", parcel)  ##

            @scope()
            def _():
                for key in parcel:
                    if kwargs.pop(key, None) is True:
                        kwargs.update(key=key)
                        break

            result = parcel.get(kwargs.get("key", parcel.get("default", "text")))
            processor = self._processors.get(path.types, {}).get("value")
            if processor:
                processed = processor(
                    args=args,
                    kwargs=kwargs,
                    path=path,
                    result=result,
                )
                if processed is not None:
                    result = processed
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

        def processor(self, *keys):
            def register(cls):
                value = cls(owner=self, __keys=keys)
                container = dict(value=value)
                for k in keys:
                    self._processors[k] = container
                return value

            return register

        def _create(self, path):
            """."""
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                parcel = {}

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

            return parcel

    dev = use("use/tools/dev.py")

    @dev()
    def _():
        """."""
        return  ##

        log("ping():", use("use/foo/ping.py")())
        log("ping():", use("use/foo/ping.py")())

    @dev()
    def _():
        """."""
        return  ##
        log("ping():", use("use/foo/ping.js").ping())

    # Create new use
    use = Use(_parse=use("use/use/parse.py"), **use._)
    log("use.meta.DEV:", use.meta.DEV)  ##
    ##use = Use(_parse=use("use/use/parse.py"), _cache=use._cache, package=use.package, meta=use.meta)

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
                    use,
                    Base=Base,
                    log=Log(path.path),
                    path=path.path,
                    **parcel,
                )
                if value is not None:
                    result.update(default="value", value=value)
                return result

    @use.creator("type", "js")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._.update(meta=window.Object.freeze(dict(use.meta)))

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                result = {}
                text = f"{text}\n//# sourceURL={path.path}"
                blob = new(window.Blob, [text], dict(type="text/javascript"))
                url = window.URL.createObjectURL(blob)
                module = import_from(url)
                window.URL.revokeObjectURL(url)
                value = module.default(
                    use,
                    dict(
                        meta=self.meta,
                        path=path.path,
                        **parcel,
                    ),
                )
                if value is not None:
                    result.update(default="value", value=value)
                return result

    @use.processor("js", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(
            self,
            args=None,
            kwargs=None,
            path=None,
            result=None,
        ):
            """."""

            if isinstance(result, dict) or typeName(result) == "Object":
                return window.Object.freeze(result)

    @use.processor("json")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(
            self,
            args=None,
            kwargs=None,
            path=None,
            result=None,
        ):
            """."""
            if not kwargs.get("key") == "text" and isinstance(result, str):
                import json

                return json.loads(result)

    log("use.meta.DEV:", use.meta.DEV)  ##

    @dev()
    def _():
        """."""
        return  ##
        log("ping():", use("use/foo/ping.py")())
        log("ping():", use("use/foo/ping.py")())

    @dev()
    def _():
        """."""
        return  ##
        log("ping():", use("use/foo/ping.js").ping())

    @dev()
    def _():
        """."""
        ##return  ##
        log("foo():", use("use/foo/foo.py").foo())

    @dev()
    def _():
        """."""
        return  ##
        foo = use("use/foo/foo.json")
        foo.update(foo=43)
        log("foo:", foo)

        foo = use("use/foo/foo.json")
        log("foo:", foo)

        log(
            "foo:",
            use(
                "use/foo/foo.json",
                dict(key="node"),
                1,
                2,
                3,
            ),
        )
        log("foo:", use("use/foo/foo.json", key="text"))
        log("foo:", use("use/foo/foo.json", text=True))

    return use
