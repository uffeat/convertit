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

        def __call__(self, path: Path):
            """."""
            registry: dict = self._["_registry"]
            handler = registry.get(path.source)
            if not handler:
                raise ValueError(f"Invalid source: {path.source}")
            result = handler(path)
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
            result = handler(path)
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
                return self.text(path)
            return self.transpile(path)

        @property
        def text(self):
            return self._["text"]

        @property
        def transpile(self):
            return self._["transpile"]

    use = Use()

    class Cache:
        def __init__(self, create: callable=None):
            self.__dict__.update(__={})
            self._.update(_cache={}, _create=create)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, key, value=None):
            """."""
            cache: dict = self._['_cache']
            if value is None:
                if key in cache:
                    return cache[key]
               
                create: callable = self._.get('_create')
                if create:
                    value = create(key)
                    cache[key] = value
                    return value
                
                    
            else:
                cache[key] = value
                return value

            

       
        

    @use.text.use("/")
    class cls:
        def __init__(self, owner: Use=None):
            self.__dict__.update(__={})
            self._.update(_cache={}, owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path: Path) -> str:
            """Returns parcel text."""
            cache: dict = self._["_cache"]
            if path.path in cache:
                result = cache[path.path]
                log(f"Getting {path.path} from cache:", result)##
                return result
            if meta.DEV:
                try:
                    result = anvil.server.call("_use", path.path)
                    test = True
                    log(f"Got {path.path} from local server:", result)##
                except anvil.server.UplinkDisconnectedError as error:
                    result = self.get(path)
                    test = False
                    log(f"Got {path.path} from sheet:", result)##
                result = result, test
            else:
                result = self.get(path)
            cache[path.path] = result
            return result

        @property
        def owner(self) -> Use:
            return self._["owner"]

        def get(self, path: Path) -> str:
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
        def __init__(self, owner: Use=None):
            self.__dict__.update(__={})
            self._.update(_cache={}, owner=owner)

        @property
        def _(self) -> dict:
            return self.__

        def __call__(self, path) -> str:
            """Returns parcel text."""
            cache: dict = self._["_cache"]
            if path.path in cache:
                return cache[path.path]

            messages = {}
            raw = self.owner.text(path)
            if isinstance(raw, tuple):
                raw, test = raw
                messages.update(test=test)

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
                    **messages,
                )
                if isinstance(result, (dict, list)):
                    result = js.freeze(result)
            else:
                result = js.freeze(locals)

            cache[path.path] = result
            return result

        @property
        def owner(self) -> Use:
            return self._["owner"]

    ping = use("/ping.py")
    print("ping:", ping())

    ##ping = use("/ping.py")
    ##print("ping:", ping())

    raw = use("/ping.py", raw=True)
    ##raw = use.text(Path("/ping.py"))
    print("raw:", raw)

    raw = use("/ping.py", raw=True)
    print("raw:", raw)

    return use
