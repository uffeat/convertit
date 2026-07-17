from ._base import Base


class File(Base):
    def __init__(self, name: str):
        Base.__init__(self)
        if name and "." in name:
            types = name.split(".")
            stem = types.pop(0)
            t = types[-1]
            self._.update(stem=stem, type=t, types=tuple(types))
        self._.update(name=name)

    def __contains__(self, t: str) -> bool:
        return t in self.types

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._["name"] or ""

    @property
    def stem(self) -> str:
        return self._.get("stem", self.name)

    @property
    def type(self) -> str:
        return self._.get("type", self.types[-1] if self.types else "")

    @property
    def types(self) -> tuple:
        return self._.get("types", tuple([""]))

    @types.setter
    def types(self, types: tuple):
        if isinstance(types, str):
            types = types.split(".")
        if isinstance(types, list):
            types = tuple(types)
        return self._.update(types=types)


class Path(Base):
    def __init__(self, specifier: str):

        Base.__init__(self)

        self._.update(
            detail={},
            specifier=specifier,
        )

        parts: list = specifier.split("/")
        source = parts.pop(0)
        name = parts[-1]
        file = File(name)
        size = len(parts)

        # Enable '//' syntax for injection of next part
        constructed = []
        for index, part in enumerate(parts):
            if part:
                constructed.append(part)
            else:
                next_index = index + 1
                if next_index < size:
                    constructed.append(
                        file.stem if next_index + 1 == size else parts[next_index]
                    )

        path = "/" + "/".join(constructed)

        self._.update(
            file=file,
            full=source + path,
            parts=tuple(constructed),
            path=path,
            source=source or "/",
        )

        if constructed:
            constructed.pop()

        self._.update(
            parents=tuple(constructed),
        )

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
    def file(self) -> File:
        return self._["file"]

    @property
    def full(self) -> str:
        """Returns path with source."""
        return self._["full"]

    @property
    def parents(self) -> tuple:
        """Returns path parts without source and file."""
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
