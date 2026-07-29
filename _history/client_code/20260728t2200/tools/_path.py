from ._base import Base


class Path(Base):
    def __init__(self, specifier: str):
        Base.__init__(self)
        self(specifier)

    def __call__(self, specifier: str = None):
        if isinstance(specifier, Path):
            self._.update(specifier._)
        else:
            self._.update(
                detail={},
                specifier=specifier,
            )

            source, dash, _path = specifier.partition("/")
            path = f"{dash}{_path}"
            _parents, _, name = specifier.rpartition(dash)
            parents = _parents.split(dash)[1:]
            stem, dot, types = name.partition(".")
            shapes, _, type = types.rpartition(dot)

            self._.update(
                full=source + path,
                parents=tuple(parents),
                parts=tuple([*parents, stem]),
                path=path,
                shapes=shapes,
                # Ensure that no source is '/'
                source=source or dash,
                type=type,
                types=types,
            )

        return self

    def __contains__(self, part: str) -> bool:
        return part in self.parts

    def __getitem__(self, a):
        """."""
        if isinstance(a, slice):

            start, stop = a.start, a.stop
            if (
                isinstance(start, int)
                and not isinstance(start, bool)
                and isinstance(stop, int)
                and not isinstance(stop, bool)
            ):
                return self.parts[a]

        elif isinstance(a, int) and not isinstance(a, bool):
            if -len(self) <= a < len(self):
                return self.parts[a]

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
    def shapes(self) -> str:
        return self._["shapes"]

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
