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

    @classmethod
    def properties(cls):
        return {k: v for k, v in cls.__dict__.items() if isinstance(v, property)}

    def __init__(self, *args, **kwargs):
        Base.__init__(self)
        if kwargs:
            self._.update(**kwargs)
        else:
            self._.update(path=next(iter(args), ""))
            if "/" in self.path:
                # Avoid leading '' in parts when path starts with /
                parts = [p if i or p else "/" for i, p in enumerate(self.path.split("/"))]
                source = parts[0]
                name = parts[-1]
                self._.update(name=name, parts=parts, source=source)
                if source:
                    self._.update(relative=f"/{'/'.join(parts[1:])}")
            if "." in self.name:
                stem, _, types = self.name.partition(".")
                self._.update(
                    stem=stem,
                    type=types.split(".")[-1],
                    types=types,
                )

    def __call__(self):
        """."""

    def __contains__(self, part: str) -> bool:
        """Tests membership with respect to parts."""
        return part in self._.get("parts", [])

    def __repr__(self) -> str:

        result = dict(**self)

        for key in self.__class__.properties().keys():

            if key not in result:

                result[key] = getattr(self, key)

        return str(result)

        return str(self._)

    def __str__(self) -> str:
        return self._.get("path", "")

    @property
    def file(self):
        return "type" in self._

    @property
    def name(self):
        return self._.get("name", self._.get("path", ""))

    @property
    def parts(self):
        return tuple(self._.get("parts", [self._.get("path", "")]))

    @property
    def relative(self):
        return self._.get("relative", f"/{self._.get('path', '')}")

    @property
    def source(self):
        return self._.get("source", "")

    @property
    def stem(self):
        return self._.get("stem", self.name)

    @property
    def type(self):
        return self._.get("type", "")


specifier = "use/foo.py"
path = Path(specifier)
path = Path(**path)
print(f"{specifier} -> ", repr(path))

print("path.path:", path.path)
print("path.name:", path.name)
print("path.parts:", path.parts)
print("path.source:", path.source)
print("path.type:", path.type)
print("path.relative:", path.relative)
