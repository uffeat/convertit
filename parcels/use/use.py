def main(
    _use: callable,
    Base: type = None,
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

    class Path:

        DASH = "/"
        DOT = "."

        def __init__(self, specifier: str):
            self.__dict__.update(__={})
            self(specifier)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, a) -> "Path":
            """Parses specifier."""
            if isinstance(a, Path):
                self._.update(a._)
            else:
                specifier: str = a
                self._.update(
                    detail={},
                    specifier=specifier,
                )
                source, _, _path = specifier.partition(Path.DASH)
                path = f"{Path.DASH}{_path}"
                _parents, _, name = specifier.rpartition(Path.DASH)
                parents = _parents.split(Path.DASH)
                parents.pop(0)
                if Path.DOT in name:
                    # Handle file
                    stem, _, types = name.partition(Path.DOT)
                    shapes, _, type_ = types.rpartition(Path.DOT)
                    self._.update(
                        file=True,
                        shapes=shapes,
                        type=type_,
                        types=types,
                    )
                else:
                    stem = name
                self._.update(
                    full=source + path,
                    name=name,
                    parents=tuple(parents),
                    parts=tuple([*parents, stem]),
                    path=path,
                    # Ensure that no source is interpreted as '/'
                    source=source or Path.DASH,
                    stem=stem,
                )

                # NOTE Currently, 'full' is identical to 'specifier'. However, keep explicit
                # construction of 'full', since later versions may introduce special specifier features.

            return self

        def __contains__(self, part: str) -> bool:
            """Tests membership with respect to parts."""
            return part in self.parts

        def __getitem__(self, a):
            """Returns parts part of slice."""
            if isinstance(a, slice):
                start, stop = a.start, a.stop
                if (
                    isinstance(start, int)
                    and not isinstance(start, bool)
                    and isinstance(stop, int)
                    and not isinstance(stop, bool)
                ):
                    # Standard slicing
                    return self.parts[a]

                print(f"Not implemented: {start}:{stop}")  ##
                return

            elif isinstance(a, int) and not isinstance(a, bool):
                # Standard item by index, but without index errors; out-of-index returns None
                if -len(self) <= a < len(self):
                    return self.parts[a]

            print(f"Not implemented: [{a}]")  ##

        def __len__(self) -> int:
            """Returns number of parts."""
            return len(self.parts)

        def __repr__(self) -> str:
            return str(self._)

        def __str__(self) -> str:
            return self.path

        @property
        def detail(self) -> dict:
            return self._["detail"]

        @property
        def file(self) -> bool:
            """Returns is-file flag."""
            return self._.get("file", False)

        @property
        def full(self) -> str:
            """Returns path with source."""
            return self._["full"]

        @property
        def name(self) -> str:
            """Returns name of file of leaf dir."""
            return self._["name"]

        @property
        def parents(self) -> tuple:
            """Returns parents of file or leaf dir. Does not include source."""
            return self._["parents"]

        @property
        def parts(self) -> tuple:
            """Returns path parts without source, but with file or leaf dir stem."""
            return self._["parts"]

        @property
        def path(self) -> str:
            """Returns path relative to source. Always starts with '/'."""
            return self._["path"]

        @property
        def shapes(self) -> str:
            """Returns file suffixes without file type."""
            return self._.get("shapes", "")

        @property
        def source(self) -> str:
            """Returns source ('/' if no explicit source)."""
            return self._["source"]

        @property
        def specifier(self) -> str:
            """Returns specifier."""
            return self._["specifier"]

        @property
        def stem(self) -> str:
            """Returns stem of file or leaf dir."""
            return self._["stem"]

        @property
        def type(self) -> str:
            """Returns file type."""
            return self._.get("type", "")

        @property
        def types(self) -> str:
            """Returns all file suffixes."""
            return self._.get("types", "")

    class Text:
        def __init__(self, owner=None):
            self.__dict__.update(__={})
            self._.update(owner=owner, _registry={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: Path) -> str:
            """Returns text via registered source-dependent handlers."""
            registry: dict = self._["_registry"]
            handler = registry.get(path.source)
            if not handler:
                raise ValueError(f"Invalid source: {path.source}")
            result = handler(path.path)
            if not isinstance(result, str):
                raise TypeError(f"{path.path}: {result} is not text.")
            return result

        @property
        def owner(self) -> "Use":
            return self._["owner"]

        def use(self, *keys):
            def register(handler):
                handler = handler(owner=self.owner)
                for key in keys:
                    self._["_registry"][key] = handler
                return handler

            return register

    class Transpile:
        def __init__(self, owner=None):
            self.__dict__.update(__={})
            self._.update(owner=owner, _registry={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: Path):
            """."""
            registry: dict = self._["_registry"]
            handler = registry.get(path.type)
            if not handler:
                raise ValueError(f"No transpiler for: {path.type}")
            result = handler(path.path)
            return result

        @property
        def owner(self) -> "Use":
            return self._["owner"]

        def use(self, *keys):
            def register(handler):
                handler = handler(owner=self.owner)
                for key in keys:
                    self._["_registry"][key] = handler
                return handler

            return register

    class Use:
        def __init__(self):
            self.__dict__.update(__={})
            owner = self
            self._.update(text=Text(owner=owner), transpile=Transpile(owner=owner))

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, specifier: str, *args, **kwargs):
            """."""
            path = Path(specifier)
            raw = kwargs.pop("raw", False)
            if raw:
                result = self.text(path)
                log(f"Raw {path.path} requested: {result}.", trace="Use")  ##
                return result
            result = self.transpile(path)
            log(f"Non-raw {path.path} requested: {result}.", trace="Use")  ##
            return result

        @property
        def text(self):
            return self._["text"]

        @property
        def transpile(self):
            return self._["transpile"]

    use = Use()

    class Cache:
        def __init__(self, cache: dict = None, create: callable = None, owner=None):
            self.__dict__.update(__={})
            self._.update(_cache=cache or {}, _create=create, owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, key, value=None):
            """."""
            if value is None:
                return self.get(key)
            return self.set(key, value)

        def __contains__(self, key) -> bool:
            """."""
            return key in self._["_cache"]

        def __getitem__(self, key):
            return self.get(key)

        def __len__(self) -> int:
            """."""
            return len(self._["_cache"])

        def __setitem__(self, key, value):
            return self.set(key, value)

        def __str__(self):
            return str(self._["_cache"])

        @property
        def owner(self):
            return self._["owner"]

        def get(self, key):
            """."""
            cache: dict = self._["_cache"]
            if key in cache:
                value = cache[key]
                log(f"Got {key} from cache: {value}", trace="Cache")  ##
                return value
            create: callable = self._.get("_create")
            if create:
                return self.set(key, create)

        def set(self, key, value):
            """."""
            cache: dict = self._["_cache"]
            if callable(value):
                value = value(key)
                log(f"Created {key} from function: {value}", trace="Cache.set")  ##
            if value is None:
                value = cache.pop(key, None)
                log(f"Removed {key} from cache.", trace="Cache.set")  ##
            else:
                log(f"Created {key} to cache: {value}", trace="Cache.set")  ##
                cache[key] = value
            return value

        def create(self, owner=None) -> callable:
            """Decorated create callable"""
            if owner:
                self._.update(owner=owner)

            def register(create: callable) -> callable:
                self._.update(_create=create)
                return create

            return register

    @use.text.use("/")
    class cls:

        name = "use"

        def __init__(self, owner: Use = None):
            self.__dict__.update(__={})

            def get(path: str) -> str:
                """Returns uncached parcel text from sheet."""
                node = document.createElement("div")
                node.setAttribute("__path__", path)
                document.head.append(node)
                value = js.getComputedStyle(node).getPropertyValue("--__use__").strip()
                if not value:
                    raise ValueError(f"Invalid {path}.")
                node.remove()
                result = js.atob(value[1:-1])
                return result

            def create(path: str) -> str:
                """Returns uncached parcel text from local server or sheet."""
                if meta.DEV:
                    try:
                        result = anvil.server.call("_use", path)
                        test = True
                        log(f"Got {path} from local server.", trace="create")  ##
                    except anvil.server.UplinkDisconnectedError as error:
                        result = get(path)
                        test = False
                        log(f"Got {path} from sheet.", trace="create")  ##
                else:
                    result = get(path)
                return result

            self._.update(cache=Cache(create=create, owner=self), owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: str) -> str:
            """Returns parcel text."""
            result = self.cache(path)
            return result

        @property
        def cache(self) -> Cache:
            return self._["cache"]

        @property
        def owner(self) -> Use:
            return self._["owner"]

    @use.transpile.use("py")
    class cls:

        name = "py"

        def __init__(self, owner: Use = None):
            self.__dict__.update(__={})

            def create(path: str):
                raw = owner(path, raw=True)
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
                        log=log,
                        meta=meta,
                        path=path,
                        window=window,
                    )
                    if isinstance(result, (dict, list)):
                        result = js.freeze(result)
                else:
                    result = js.freeze(locals)
                return result

            self._.update(cache=Cache(create=create, owner=self), owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: str):
            """Returns transpiled parcel."""
            result = self.cache(path)
            return result

        @property
        def cache(self) -> Cache:
            return self._["cache"]

        @property
        def owner(self) -> Use:
            return self._["owner"]

    ##ping = use("/ping.py")
    ##print("ping:", ping())

    ##ping = use("/ping.py")
    ##print("ping:", ping())

    raw = use("/ping.py", raw=True)
    ##raw = use.text(Path("/ping.py"))
    log("raw:", raw)

    raw = use("/ping.py", raw=True)
    ##log("raw:", raw)

    ##
    from types import MethodType, FunctionType


    def foo():
        """."""


    print('type_name:', type(foo).__name__)
    print('Is function:', isinstance(foo, FunctionType))


    class Owner:
        """."""
        def create(self):
            """."""

        @staticmethod
        def stat(self):
                """."""


    owner = Owner()

    print('Is method:', isinstance(owner.create, MethodType))

    print('Is static:', isinstance(owner.stat, staticmethod))

    print('type_name:', type(owner.create).__name__)
    print('type_name:', type(owner.stat).__name__)


    


    ##

    return use
