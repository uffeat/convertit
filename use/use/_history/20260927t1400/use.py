def main(
    use: callable,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> callable:
    """."""
    ##log("Loading...")  ##
    from anvil.js import import_from, new, window
    element = use.package.client.tools.element

    Path = use("use/path/path.py")
    ##typeName = use("use/type/name.js")

    document = window.document

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._(_creators={}, _processors={})

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            path = self.Path(specifier)
            parcel = self._create(path)
            args = self._parse(args, kwargs, **parcel)
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
            """Decorates creator."""

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
            """Decorates processor."""

            def register(cls):
                value = cls(owner=self, __keys=keys)
                container = dict(value=value)
                for k in keys:
                    self._processors[k] = container
                return value

            return register

        def _create(self, path) -> dict:
            """Returns parcel built by creators."""
            if path.path in self._cache:
                parcel = self._cache[path.path]
                if self.meta.DEV:
                    parcel.update(cached=True)
            else:
                parcel = dict(state=dict())

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

                # Run creation pipe
                for key in self._creators.keys():
                    create(key)
                # Cache
                self._cache[path.path] = parcel

            return parcel

        @staticmethod
        def _parse(args: tuple, kwargs: dict, **parcel) -> tuple:
            """Mutates kwargs and returns modified args."""
            # Allow kwargs as positional arg
            _kwargs = dict(
                next(
                    iter([a for a in args[0:1] if hasattr(a, "keys")]),
                    {},
                )
            )
            ##log("_kwargs:", _kwargs)  ##
            if _kwargs:
                args = tuple(args[1:])
                kwargs.update(**_kwargs)
            # Enable boolean key specification
            for key in parcel:
                if kwargs.pop(key, None) is True:
                    kwargs.update(key=key)
                    break
            return args

    # Create new use
    use = Use(Path=Path, **use._)

    

    @use.creator("source", "use")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, **parcel) -> dict:
            """Returns node and text updates."""
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
            value = window.getComputedStyle(node).getPropertyValue("--__path__").strip()
            text = window.atob(value[1:-1])
            return text

    @use.creator("type", "py")
    class cls(Base):

        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                Construct = use.package.tools.Construct
                Log = use.package.client.tools.Log
                result = {}
                value = Construct(text=text, use=use)(
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
            self._(meta=window.Object.freeze(dict(use.meta)))

        def __call__(self, path, text: str = None, **parcel) -> dict:
            """."""
            if isinstance(text, str):
                Construct = use.package.client.tools.Construct
                result = {}
                value = Construct(path=path.path, text=text, use=use)(
                    path=path.path, **parcel
                )
                if value is not None:
                    result.update(default="value", value=value)
                return result

    

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

    ##Path = use("use/path/path.py")
    ##log("Path:", Path)  ##

    return use
