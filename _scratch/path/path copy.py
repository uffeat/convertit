class Base:

    def __init__(self, *args, **kwargs):
        # Enable use of __setattr__
        self.__dict__.update(__={k: v for k, v in kwargs.items() if v is not None})

    @property
    def _(self) -> dict:
        return self.__

    def __contains__(self, key) -> bool:
        return key in self._

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        # Provide JS-like attr lookup
        if not isinstance(key, slice):
            return self._.get(key)

    def __iter__(self) -> iter:
        # Facilitate **-unpacking
        return iter(self._)

    def __len__(self) -> int:
        return len(self._)

    def get(self, key, default=None):
        return self._.get(key, default)

    def items(self):
        return self._.items()

    def keys(self):
        # Facilitate **-unpacking
        return self._.keys()

    def values(self):
        return self._.values()


class Path(Base):
    def __init__(self, *args, **kwargs):
        Base.__init__(self)

        path = next(iter(args), "")

        if "/" in path:
            # Avoid leading '' in parts when path starts with /
            parts = [p if i or p else "/" for i, p in enumerate(path.split("/"))]
            *_, name = parts
            source = _[0] if _ else ""
        else:
            parts = [path]
            name = path
            source = ""

      

        if "." in name:
            stem, _, types = name.partition(".")
            self._.update(
                file=True,
                stem=stem,
                type=types.split(".")[-1],
                types=types,
            )
        else:
            self._.update(
                file=False,
                stem=name,
                type="",
                types="",
            )

        self._.update(
            name=name,
            parts=tuple(parts),
            path=path,
            relative=f"/{'/'.join(parts[1:])}" if source else f"/{path}",
            source=source,
        )

    def __call__(self):
        """."""

    def __contains__(self, part: str) -> bool:
        """Tests membership with respect to parts."""
        return part in self._.get("parts", [])

    def __repr__(self) -> str:
        return str(self._)

    def __str__(self) -> str:
        return self._.get("path", "")


specifier = "use/bar/foo.py"
path = Path(specifier)
print(f"{specifier} -> ", repr(path))
