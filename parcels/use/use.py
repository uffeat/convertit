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

        def __init__(self):
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
                text = js.atob(value[1:-1])
                return text, node

            self._.update(_get=get)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: str) -> tuple:
            """."""
            get: callable = self._["_get"]

            if meta.DEV:
                try:
                    text = anvil.server.call("_use", path)
                    test = True
                    node = None
                    log(f"Got {path} from local server.", trace="create")  ##
                except anvil.server.UplinkDisconnectedError as error:
                    text, node = get(path)
                    test = False
                    log(f"Got {path} from sheet.", trace="create")  ##
            else:
                text, node = get(path)
                test = False
            return text, node, test

    Text = Text()

    class Transpilers:
        def __init__(self, owner=None):
            self.__dict__.update(__={})
            self._.update(_registry={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, key):
            """."""
            registry: dict = self._["_registry"]
            return registry.get(key)

        def add(self, key, handler):
            registry: dict = self._["_registry"]
            registry[key] = handler
            return handler

    class Use:
        def __init__(self):
            self.__dict__.update(__={})
            self._.update(_cache={}, _transpilers=Transpilers())

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, specifier: str, *args, **kwargs):
            """."""
            cache: dict = self._["_cache"]
            transpilers: dict = self._["_transpilers"]

            path = Path(specifier)

            key = str(path)

            if key in cache:
                cached = cache[key]
            else:
                transpilers: Transpilers = self._["_transpilers"]
                transpile = transpilers(path.type)
                if not transpile:
                    raise TypeError(f"No transpiler for {path.type}")
                text, node, test = Text(key)
                transpiled = transpile(
                    self, node=node, path=key, text=text, test=test
                )
                cached = dict(node=node, test=test, raw=text, value=transpiled)
                cache[key] = cached

            raw = kwargs.pop("raw", False)
            if raw:
                return cached["raw"]
            return cached["value"]

        def transpiler(self, *keys):
            def register(target):
                handler = target()
                transpilers: Transpilers = self._["_transpilers"]

                for key in keys:
                    transpilers.add(key, handler)
                return target

            return register

    use = Use()

    @use.transpiler("py")
    class cls:

        def __init__(self):
            self.__dict__.update(__={})

        @property
        def _(self) -> dict:
            return self.__

        def __call__(
            self, use, node=None, path: str = None, text: str = None, test: bool = None
        ):
            """Returns transpiled parcel."""
            locals = {}
            exec(text, {}, locals)
            if "main" in locals:
                main = locals["main"]
                result = main(
                    use,
                    Base=Base,
                    Path=Path,
                    anvil=anvil,
                    console=console,
                    document=document,
                    js=js,
                    log=log,
                    meta=meta,
                    node=node,
                    path=path,
                    test=test,
                    window=window,
                )
                if isinstance(result, (dict, list)):
                    result = js.freeze(result)
            else:
                result = js.freeze(locals)
            return result

    ping = use("/ping.py")
    print("ping:", ping())

    ##ping = use("/ping.py")
    ##print("ping:", ping())

    raw = use("/ping.py", raw=True)
    log("raw:", raw)

    raw = use("/ping.py", raw=True)
    ##log("raw:", raw)

    return use
