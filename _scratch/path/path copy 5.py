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
            # name and types
            stem, _, types = name.partition(".")
            # type
            *_, type_ = types.rpartition(".")
            self._.update(stem=stem, type=type_, types=types)
        self._.update(name=name)

    def __str__(self) -> str:
        return self.name

    @property
    def name(self) -> str:
        return self._["name"]

    @property
    def stem(self) -> str:
        return self._.get("stem", self.name)

    @property
    def type(self) -> str:
        return self._.get("type", "")

    @type.setter
    def type(self, type: str):
        return self._.update(type=type)

    @property
    def types(self) -> str:
        return self._.get("types", self.type)

    @types.setter
    def types(self, types: str):
        return self._.update(types=types)


class Path(Base, AttributeMixin):
    def __init__(self, specifier):
        Base.__init__(self)

        if isinstance(specifier, str):
            specifier = specifier.split("/")
        

        root = specifier.pop(0)
        name = specifier[-1]
        file = File(name)
        size = len(specifier)

        # Enable '//' for injection of next part
        constructed = []
        for index, part in enumerate(specifier):
            if part:
                constructed.append(part)
            else:
                
                constructed.append(file.stem if index + 2 == size else specifier[index + 1])

        path = "/" + "/".join(constructed)
        parts = tuple(constructed)
        constructed.pop()
     
        self._.update(
            detail={},
            file=file,
            full=root + path,
            parents=tuple(constructed),
            parts=parts,
            path=path,
            root=root or "/",
        )

    def __contains__(self, part: str) -> bool:
        return part in self.parts

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
        """Returns path witrh root."""
        return self._["full"]

    @property
    def parents(self) -> tuple:
        """Returns path parts without root and file."""
        return self._["parents"]

    @property
    def parts(self) -> tuple:
        """Returns path parts without root."""
        return self._["parts"]

    @property
    def path(self) -> str:
        """Returns path relative to root. Always starts with '/'."""
        return self._["path"]

    @property
    def root(self) -> str:
        return self._["root"]


specifier = "//stuff//ding.py"
##specifier = "/stuff"
specifier = "/"

##specifier = ['/', 'stuff','ding.py']


path = Path(specifier)
print("specifier:", specifier)
print("full:", path.full)
print("path:", path.path)
print("parents:", path.parents)
print("parts:", path.parts)
print("root:", path.root)

##print("file:", path.file)
print("name:", path.file.name)
print("stem:", path.file.stem)
print("type:", path.file.type)
print("types:", path.file.types)
##print("parents:", path.file.parents)

print("stem:", path("file")("stem"))


path("file")("type", "foo", 42)
print("type:", path.file.type)
