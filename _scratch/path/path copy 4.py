class Base:

    def __init__(self):
        # NOTE Add to '__dict__' to enable '__setattr__'
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__


class File(Base):
    def __init__(self, name: str):
        Base.__init__(self)
        if name and "." in name:
            # name and types
            stem, _, types = name.partition(".")
            # type
            *_, type_ = types.rpartition(".")
            self._.update(stem=stem, type=type_, types=types)
        self._.update(name=name)

    def __call__(self, key):
        return getattr(self, key, None)

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

    @property
    def types(self) -> str:
        return self._.get("types", "")


class Path(Base):
    def __init__(self, specifier: str):
        Base.__init__(self)

       
        
       
        parts = specifier.split("/")
        root = parts[0] or "/"
        name = parts[-1]
        file=File(name)

        size = len(parts)



        for index, part in enumerate(parts):
            print("index:", index)  ##
            print("part:", part)  ##






        

        






       
        ##path = "/" + "/".join(parts[1:])
        full = "/".join(parts)

        parts.pop(0)

        path = "/" + "/".join(parts)

       

       
        

        self._.update(
            file=file,
            full=full,
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
    def full(self) -> str:
        return self._["full"]

    @property
    def parts(self) -> tuple:
        return self._["parts"]

    @property
    def path(self) -> str:
        return self._["path"]

    @property
    def root(self) -> str:
        return self._["root"]


specifier = "@/stuff/ding.py"
##specifier = "/stuff"
path = Path(specifier)
print("specifier:", specifier)
print("full:", path.full)
print("path:", path.path)
print("parts:", path.parts)
print("root:", path.root)

##print("file:", path.file)
print("name:", path.file.name)
print("stem:", path.file.stem)
print("type:", path.file.type)
print("types:", path.file.types)
##print("parents:", path.file.parents)

##print("stem:", path("file")("stem"))
