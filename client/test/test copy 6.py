def main(
    Base: type = None,
    Log: type = None,
    Path: callable = None,
    anvil=None,
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

    class Registry(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _registry={}, **kwargs)

        def __call__(self, *keys, **kwargs):
            """Registers callable."""
            if keys:
                if callable(keys[-1]):
                    keys = list(keys)
                    value = keys.pop()
                    keys = tuple(keys)
                else:
                    value = None
            else:
                value = None

            # NOTE Reliable alternative to using 'global'
            context = dict(keys=keys)

            def register(value):
                keys = context["keys"]
                if not keys:
                    keys = tuple([value.__name__])
                # NOTE Create 'stored' once - NOT in keys loop!
                stored = dict(keys=keys, value=value, kwargs=kwargs)
                for key in keys:
                    self._registry[key] = stored
                return value

            if not value:
                return register
            return register(value)

        def __contains__(self, key) -> bool:
            return key in self._registry

        def __getitem__(self, key):
            """Returns instance."""
            if key in self:
                stored: dict = self._registry[key]
                value = stored["value"]
                if isinstance(value, type):
                    ##print("Instatiating for:", key)  ##
                    kwargs = stored.get("kwargs")
                    if "__init__" in value.__dict__:
                        value = value(owner=self, **kwargs)
                    else:
                        value = value()
                    stored.update(value=value)
                return value

    class Parcel(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _creators=Registry(owner=self), _data={}, **kwargs)

        def __call__(self, *args, **kwargs):
            """Registers creator."""
            return self._creators(*args, **kwargs)

        def __getitem__(self, key):
            """Returns item value."""
            if key in self._data:
                return self._data[key]
            creator = self._creators[key]
            if creator:
                value = creator(key)
                self._data[key] = value
                return value

    class Use(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _cache={}, **kwargs)
            # Create top-level container
            node = self.document.createElement("div")
            node.attachShadow(dict(mode="open"))
            slot = self.document.createElement("slot")
            node.shadowRoot.append(slot)
            node.id = "use"
            self.document.body.append(node)
            # Update state
            self._.update(
                node=node,
                transpiler=Registry(owner=self),
                source=Registry(owner=self),
            )

        def __call__(self, specifier: str, *args, **kwargs):
            """Returns result from import engine."""
            # Enable setting options from JS
            kwargs.update(**next(iter([a for a in args if js.type(a, "Object")]), {}))
            path = Path(specifier)
            key = kwargs.get("key", "value")

            result = {}

            handlers = {}
            def value():
                handler = self.transpiler[path.type]
                if handler:
                    result: dict = self._get_text(path=path)
                    result: dict = handler(path=path, **result)
                    return result
                return {}
            handlers['value'] = value
            def text():
                result: dict = self._get_text(path=path)
                return result
            handlers['text'] = text

            



            if key == "value":
                handler = self.transpiler[path.type]
                if handler:
                    result: dict = self._get_text(path=path)
                    result: dict = handler(path=path, **result)

            elif key == "text":
                result: dict = self._get_text(path=path)

            return result.get(key)

        def _get_text(self, path=None) -> dict:
            """."""
            handler = self.source[path.source]
            if handler:
                result: dict = handler(path=path)
                return result
            return {}

    use = Use(
        Base=Base,
        Path=Path,
        Log=Log,
        anvil=anvil,
        document=document,
        js=js,
        meta=meta,
        window=window,
    )

    @use.source("use")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, _cache={}, **kwargs)

        def __call__(self, path=None, **kwargs) -> dict:
            key = path.path
            if key in self._cache:
                result: dict = self._cache[key]
                if use.meta.DEV and 'cached' not in result:
                    log('Using cache')##
                    result.update(cached=True)
            else:
                result = dict()
                node = use.document.createElement("div")
                node.setAttribute("__path__", path.path)
                use.node.append(node)
                message = {}
                if use.meta.DEV:
                    try:
                        text = use.anvil.server.call(f"_use", path.full)
                        message.update(test=True)
                    except use.anvil.server.UplinkDisconnectedError as error:
                        text = self._get_text(node=node, path=path)
                    except Exception as error:
                        raise ValueError(
                            f"Invalid path: {path.full}. Error: {str(error)}"
                        )
                else:
                    text = self._get_text(node=node, path=path)
                result.update(node=node, text=text, **message)
                self._cache[key] = result
            return result

        def _get_text(self, node=None, path=None) -> str:
            """Returns uncached text from sheet."""
            value = (
                use.js.getComputedStyle(node)
                .getPropertyValue(f"--__{self.key}__")
                .strip()
            )
            if not value:
                raise ValueError(f"Invalid path: {path.full}.")
            text = use.js.atob(value[1:-1])
            return text

    @use.transpiler("py")
    class cls(use.Base):
        def __init__(self, **kwargs):
            use.Base.__init__(self, _cache={}, **kwargs)

        def __call__(
            self, node=None, path=None, test=None, text=None, **kwargs
        ) -> dict:
            key = path.full
            if key in self._cache:
                result: dict = self._cache[key]
            else:
                result = dict()
                locals = {}
                exec(text, {}, locals)
                main = locals.pop("main", None)
                if main:
                    value = main(
                        use,
                        log=Log(path=path.full),
                        node=node,
                        path=path,
                        test=test,
                        **locals,
                    )
                    if isinstance(value, dict):
                        value = use.js.freeze(value)
                else:
                    value = use.js.freeze(locals)
                result.update(value=value)
                self._cache[key] = result
            return result

    

    log("use/ping.py:", use("use/ping.py")())

    

    log("use/ping.py:", use("use/ping.py", key="text"))
    log("use/ping.py:", use("use/ping.py", key="text"))

    
