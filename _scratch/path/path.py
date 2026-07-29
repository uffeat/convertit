DASH = "/"
DOT = "."


class Path:
    def __init__(self, specifier: str):
        self.__dict__.update(__={})
        self(specifier)

    def __call__(self, specifier: str = None) -> "Path":
        """Parses specifier."""
        if isinstance(specifier, Path):
            self._.update(specifier._)
        else:
            self._.update(
                detail={},
                specifier=specifier,
            )
            source, _, _path = specifier.partition(DASH)
            path = f"{DASH}{_path}"
            _parents, _, name = specifier.rpartition(DASH)
            parents = _parents.split(DASH)
            parents.pop(0)
            if DOT in name:
                # Handle file
                stem, _, types = name.partition(DOT)
                shapes, _, type_ = types.rpartition(DOT)
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
                source=source or DASH,
                stem=stem,
            )

            # NOTE Currently, 'full' is identical to 'specifier'. However, keep explicit
            # construction of 'full', since later versions may introduce special specifier features.

        return self

    @property
    def _(self) -> dict:
        return self.__

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
