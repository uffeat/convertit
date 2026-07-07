class Base:

    def __init__(self):
        # NOTE Add to '__dict__' to enable '__setattr__'
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__


class AttributeMixin:
    def __call__(self, *args):
        """Dynamic combined getter/setter."""
        if len(args) == 1:
            key = args[0]
            return getattr(self, key, None)
        if len(args) >= 2:
            key, value, *_ = args
            setattr(self, key, value)


class File(Base, AttributeMixin):
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


class Path(Base, AttributeMixin):
    def __init__(self, specifier):
        Base.__init__(self)

        if isinstance(specifier, str):
            specifier = specifier.split("/")

        source = specifier.pop(0)
        name = specifier[-1]
        file = File(name)
        size = len(specifier)

        # Enable '//' syntax for injection of next part
        constructed = []
        for index, part in enumerate(specifier):
            if part:
                constructed.append(part)
            else:
                next_index = index + 1
                if next_index < size:
                    constructed.append(
                        file.stem if next_index + 1 == size else specifier[next_index]
                    )

        path = "/" + "/".join(constructed)
        parts = tuple(constructed)
        if constructed:
            constructed.pop()

        self._.update(
            detail={},
            file=file,
            full=source + path,
            parents=tuple(constructed),
            parts=parts,
            path=path,
            source=source or "/",
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


specifier = "@/stuff//ding.svg.js"
##specifier = "//ding.py"
##specifier = "//stuff//ding.py"
##specifier = "/stuff/ding.py"
##specifier = "/"
##specifier = ['/', 'stuff','ding.py']
##specifier = "/"


path = Path(specifier)
print("specifier:", specifier)
print("full:", path.full)
print("path:", path.path)
print("parents:", path.parents)
print("parts:", path.parts)
print("source:", path.source)

##print("file:", path.file)
print("name:", path.file.name)
print("stem:", path.file.stem)
print("type:", path.file.type)
print("types:", path.file.types)

print("first part:", path[0])
print("part:", path[2])
print("part:", path[-2])

print("part:", path[-3])
##print("parents:", path.file.parents)

print("slice:", path[-5:5])

print("stem:", path("file")("stem"))
path("file")("types", "ding.dong")
print("type:", path.file.type)
