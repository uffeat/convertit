def main(
    use: callable,
    Base: type = None,
    Path: callable = None,
    anvil=None,
    console=None,
    document=None,
    js=None,
    log=None,
    meta=None,
    window=None,
    **kwargs,
) -> callable:
    """."""

    class Text:
        def __init__(self, owner=None):
            self.__dict__.update(__={})
            self._.update(_registry={})
            if owner:
                self._.update(owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path):
            """."""
            registry: dict = self._["_registry"]
            handler = registry.get(path.source)
            if not handler:
                raise ValueError(f"Invalid source: {path.source}")
            result = handler(path)
            return result

        @property
        def owner(self) -> 'Use':
            return self._.get("owner")

        def use(self, *keys):
            def register(handler):
                if isinstance(handler, type):
                    expects = getattr(
                        handler.__dict__.get("__init__"), "__annotations__", {}
                    ).keys()
                    if "owner" in expects:
                        handler = handler(owner=self.owner)
                    else:
                        handler = handler()
                for key in keys:
                    self._["_registry"][key] = handler
                return handler

            return register

    class Transpile:
        def __init__(self, owner=None):
            self.__dict__.update(__={})
            self._.update(_registry={})
            if owner:
                self._.update(owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path):
            """."""
            registry: dict = self._["_registry"]
            handler = registry.get(path.type)
            if not handler:
                raise ValueError(f"No transpiler for: {path.type}")
            result = handler(path)
            return result

        @property
        def owner(self) -> 'Use':
            return self._.get("owner")

        def use(self, *keys):
            def register(handler):
                if isinstance(handler, type):
                    expects = getattr(
                        handler.__dict__.get("__init__"), "__annotations__", {}
                    ).keys()
                    if "owner" in expects:
                        handler = handler(owner=self.owner)
                    else:
                        handler = handler()
                for key in keys:
                    self._["_registry"][key] = handler
                return handler

            return register

    class Use:
        def __init__(self):
            self.__dict__.update(__={})
            self._.update(text=Text(owner=self), transpile=Transpile(owner=self))

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, specifier: str, *args, **kwargs):
            """."""
            path = Path(specifier)
            raw = kwargs.pop("raw", False)
            if raw:
                return self.text(path)
            return self.transpile(path)

        @property
        def text(self) -> Text:
            return self._["text"]

        @property
        def transpile(self) -> Transpile:
            return self._["transpile"]

    use = Use()

    @use.text.use("/")
    class cls:
        def __init__(self, owner: type = None):
            self.__dict__.update(__={})
            self._.update(_cache={})
            if owner:
                self._.update(owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path) -> str:
            """Returns parcel text."""
            cache: dict = self._["_cache"]
            if path.path in cache:
                return cache[path.path]
            if meta.DEV:
                try:
                    result = anvil.server.call("_use", path.path)
                except anvil.server.UplinkDisconnectedError as error:
                    log("Local server not running.")
                    result = self.get(path)
            else:
                result = self.get(path)

            cache[path.path] = result
            return result

        @property
        def owner(self) -> Use:
            return self._.get("owner")

        def get(self, path) -> str:
            """Returns uncached parcel text from sheet."""
            node = document.createElement("div")
            node.setAttribute("__path__", path.path)
            document.head.append(node)
            value = js.getComputedStyle(node).getPropertyValue("--__use__").strip()
            if not value:
                raise ValueError(f"Invalid {path}.")
            node.remove()
            result = js.atob(value[1:-1])
            return result

    @use.transpile.use("py")
    class cls:
        def __init__(self, owner: type = None):
            self.__dict__.update(__={})
            self._.update(_cache={})
            if owner:
                self._.update(owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path) -> str:
            """Returns parcel text."""
            cache: dict = self._["_cache"]
            if path.path in cache:
                return cache[path.path]

            raw = self.owner.text(path)

            locals = {}
            exec(raw, {}, locals)
            if "main" in locals:

                main = locals["main"]
                result = main(
                    self.owner,
                    Base=Base,
                    Path=Path,
                    anvil=anvil,
                    console=console,
                    document=document,
                    js=js,
                    meta=meta,
                    log=log,
                    path=path,
                    window=window,
                )
                if isinstance(result, (dict, list)):
                    result = js.freeze(result)
            else:
                result = js.freeze(locals)

            

            cache[path.path] = result
            return result

        @property
        def owner(self) -> Use:
            return self._.get("owner")

    

    ##ping = use("/ping.py")
    ##print("ping:", ping())

    raw = use("/ping.py", raw=True)
    print("raw:", raw)

    raw = use("/ping.py", raw=True)
    print("raw:", raw)

    

    return use
