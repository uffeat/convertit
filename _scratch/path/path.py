class Base:

    def __init__(self):
        # NOTE Add to '__dict__' to enable '__setattr__'
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__


class File(Base):
    def __init__(self, name: str, parents: tuple = None):
        Base.__init__(self)
        if name and "." in name:
            # name and types
            stem, _, types = name.partition(".")
            # type
            *_, type_ = types.rpartition(".")
            self._.update(stem=stem, type=type_, types=types)
        self._.update(name=name, parents=parents)

    def __call__(self, key):
        return getattr(self, key, None)

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._["name"]

    @property
    def parents(self) -> tuple:
        return self._["parents"]

    @property
    def stem(self) -> str:
        return self._.get("stem", self.name)

    @property
    def type(self) -> str:
        return self._.get("type", "")

    @property
    def types(self) -> str:
        return self._.get("types", "")


class Path(Base):
    def __init__(self, specifier: str):
        Base.__init__(self)

        path = []
        
        ##
        parts = specifier.split("/")[1:]
        ##

        ##print("parts:", parts)  ##
        length = len(parts)
        ##print("length:", length)  ##

        for index, part in enumerate(parts):
            ##print("index:", index)  ##
            ##print("part:", part)  ##
            if part:
                path.append(part)
            else:
                next_index = index + 1
                ##print("next_index:", next_index)  ##
                next_part = parts[next_index]
                if (next_index + 1) == length:
                    next_part, *_ = next_part.partition(".")
                path.append(next_part)

        path = "/".join(path)

        ##print("path:", path)  ##
        parts = [p for p in path.split("/") if p]
        name = parts[-1]

        # XXX TODO Check if agrees with // short hand. If not, move root detection to shorthand parsing
        root = "/" if path.startswith("/") else parts[0]

        self._.update(
            file=File(name, parents=tuple(parts[:-1])),
            parts=tuple(parts),
            path=path,
            root=root,
        )

    def __call__(self, key):
        return getattr(self, key, None)

    def __contains__(self, part: str) -> bool:
        return part in self.parts

    def __len__(self) -> int:
        return len(self.parts)

    def __str__(self) -> str:
        return self.path

    @property
    def file(self) -> File:
        return self._["file"]

    @property
    def parts(self) -> tuple:
        return self._["parts"]

    @property
    def path(self) -> str:
        return self._["path"]

    @property
    def root(self) -> str:
        return self._["root"]


specifier = "/stuff//ding.py"
##specifier = "/stuff"
path = Path(specifier)
print("specifier:", specifier)
print("path:", path.path)
print("parts:", path.parts)
print("root:", path.root)

print("file:", path.file)
print("name:", path.file.name)
print("stem:", path.file.stem)
print("type:", path.file.type)
print("types:", path.file.types)
print("parents:", path.file.parents)

print("stem:", path("file")("stem"))
