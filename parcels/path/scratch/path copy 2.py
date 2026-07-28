class Path:
    def __init__(self, specifier: str):
        self.__dict__.update(__={})

        self(specifier)

    def __call__(self, specifier: str):
        self._.update(
            detail={},
            specifier=specifier,
        )

        source, sep, _path = specifier.partition("/")
        _parents, sep, name = specifier.rpartition("/")
        parents = _parents.split("/")[1:]
        stem, sep, _types = name.partition(".")
        types = _types.split(".")
        path = f"/{_path}"

        

        
       

        

        self._.update(
            full=source + path,
            parents=tuple(parents),
            parts=tuple([*parents, stem]),
            path=path,
            # Ensure that no source is '/'
            source=source or "/",
            type=types[-1],
            types=tuple(types),
        )

        print("self._:", self._)  ##

        return self

    @property
    def _(self) -> dict:
        return self.__

    def __contains__(self, part: str) -> bool:
        return part in self.parts

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.parts[key]
        else:
            if -len(self) <= key < len(self):
                return self.parts[key]

    def __len__(self) -> int:
        return len(self.parts)

    def __str__(self) -> str:
        return self.path

    @property
    def detail(self) -> dict:
        return self._["detail"]

    @property
    def full(self) -> str:
        """Returns path with source."""
        return self._["full"]

    @property
    def name(self) -> str:
        return self._["name"]

    @property
    def parents(self) -> tuple:
        """Returns path parts without source and name."""
        return self._["parents"]

    @property
    def parts(self) -> tuple:
        """Returns path parts without source."""
        return self._["parts"]

    @property
    def path(self) -> str:
        """Returns path relative to source. Always starts with '/'."""
        return self._["path"]

    @property
    def source(self) -> str:
        return self._["source"]

    @property
    def specifier(self) -> str:
        return self._["specifier"]

    @property
    def stem(self) -> str:
        return self._["stem"]

    @property
    def type(self) -> str:
        return self._["type"]

    @property
    def types(self) -> tuple:
        return self._["types"]


path = Path("@/foo/foo.py.html")
path = Path("/foo.py.html")
