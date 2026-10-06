def main(
    _use: callable,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> callable:
    """."""
    ##log("Loading...")  ##
    from anvil.js import import_from, new, window

    element = _use.package.client.tools.element

    ##typeName = use("use/type/name.js")

    document = window.document

    Log = _use("use/log/log.py")
    Py = _use("use/use/py.py")

    ##log("Py:", Py)  ##

    class use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)
            self._(_creators={}, _processors={}, session=window.crypto.randomUUID())

        def __call__(self, specifier, *args, **kwargs):
            """Returns result from import engine."""
            path = self.Path(specifier)
            parcel = self._create(path)
            args = self._parse(args, kwargs, **parcel)
            result = parcel.get(kwargs.get("key", parcel.get("default", "text")))
            result = self._process(
                args=args, kwargs=kwargs, path=path, parcel=parcel, result=result
            )
            return result

        def creator(self, key: str, *keys):
            """Decorates creator."""

            def register(cls):
                registry = self._creators.get(key)
                if registry is None:
                    registry = {}
                    self._creators[key] = registry
                value = cls(owner=self, _key=key, _keys=keys)  ##
                container = dict(value=value)
                for k in keys:
                    registry[k] = container
                return value

            return register

        def get(self, key) -> dict:
            """Returns copy of parcel."""
            if key not in self._cache:
                self(key)

            return dict(**self._cache.get(key, {}))

        def processor(self, *keys):
            """Decorates processor."""

            def register(cls):
                value = cls(owner=self, __keys=keys)  ##
                container = dict(value=value)
                for k in keys:
                    self._processors[k] = container
                return value

            return register

        def update(self, key, **updates) -> dict:
            """Creates or updates and returns parcel."""
            parcel: dict = self._cache.get(key, {})
            if parcel:
                for k, v in updates.items():
                    if v is None:
                        parcel.pop(k, None)
                    else:
                        parcel[k] = v
            else:
                self._cache[key] = parcel
                parcel.update(**updates)
            return parcel

        def _create(self, path) -> dict:
            """Returns parcel built by creators."""
            if path.path in self._cache:
                parcel = self._cache[path.path]
                if not self.meta.PROD:
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
                if parcel.pop("cache", True):
                    self._cache[path.path] = parcel

            return parcel

        @staticmethod
        def _parse(args: tuple, kwargs: dict, **parcel) -> tuple:
            """Mutates kwargs and returns modified args."""
            # Allow kwargs as positional arg
            _kwargs = dict(
                next(
                    (a for a in args[0:1] if hasattr(a, "keys")),
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

        def _process(
            self,
            args: tuple = None,
            kwargs: dict = None,
            path=None,
            parcel: dict = None,
            result=None,
        ):
            """."""
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

    # Create new use
    """
    HACK Something fishy is going on with the path parcel (client-side); 
    it reverts to the use class itself in subsequent use calls. 
    Therefore, make it a use prop.
    """
    use = use(Path=_use("use/path/path.py"), **_use)

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
            if not use.meta.PROD:
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
                result = {}
                constructed: dict = Py(use=use, text=text)(
                    Base=Base,
                    log=Log(path.path),
                    path=path.path,
                    **parcel,
                )
                if constructed:
                    if "value" in constructed:
                        result.update(default="value", value=constructed["value"])
                    if "meta" in constructed:
                        result.update(meta=constructed["meta"])
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

        def __call__(self, args=None, kwargs=None, path=None, result=None, **_):
            """."""
            if not kwargs.get("key") == "text" and isinstance(result, str):
                import json

                return json.loads(result)

    return use
