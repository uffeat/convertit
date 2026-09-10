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
            path = specifier if isinstance(specifier, Path) else Path(specifier)
            if path.path in self._cache:
                parcel = self._cache[path.path]
            else:
                parcel = {}

                def update(key):
                    """."""
                    registry: dict = self._registry.get(key)
                    if registry:
                        item = registry.get(path[key])
                        if item:
                            hook = item["value"]
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
                item = dict(value=value)
                for k in keys:
                    registry[k] = item
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

    class Stuff:

        def __init__(self, **kwargs):

            self.__dict__.update(__={k: v for k, v in kwargs.items() if v is not None})

        @property
        def _(self) -> dict:
            return self.__

        @property
        def _public(self) -> dict:
            return {k: v for k, v in self._.items() if not k.startswith("_")}

        def __getattr__(self, key: str):
            return self._.get(key)

        def __getitem__(self, key):
            return self._.get(key)

        def __iter__(self):
            return iter(self._public)

        def keys(self):
            return self._public.keys()

    stuff = Stuff(foo="FOO", bar="BAR")

    def test_stuff(**kwargs):
        for key, value in kwargs.items():
            print(key, value)

    test_stuff(**stuff)

    return use
