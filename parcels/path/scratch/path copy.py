class File:
    def __init__(self, name: str):
        self.__dict__.update(__={})
        if name and "." in name:
            parts = name.split(".")
            # Extract and remove stem
            stem = parts.pop(0)
            self._.update(stem=stem, type=parts[-1], types=tuple(parts))
        self._.update(name=name)

    @property
    def _(self) -> dict:
        return self.__

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

class Path:
    def __init__(self, specifier: str):
        self.__dict__.update(__={})

        self(specifier)

        
    def __call__(self, specifier: str):
        self._.update(
            detail={},
            specifier=specifier,
        )

        source, sep, path = specifier.partition('/')
        if not source:
            source = '/'
        print('source:', source)##
       
        

        parts: list = path.split("/")

        print('parts:', parts)##

        path = f"/{path}"
        print('path:', path)##

        return
        

       
        

        

        name: str = parts.pop()
        print('name:', name)##

       

        stem, sep, types = name.partition('.')
        print('stem:', stem)##
        types = types.split(".")
        print('types:', types)##

        file_type = types[-1]
        print('type:', file_type)##
        suffix = f".{file_type}"


        print('parts:', parts)##

        ##path = '/' + '/'.join(parts)

        return
        self._.update(
            file=file,
            full=source + path,
            parts=tuple(parts),
            path=path,
            # Ensure that no source is '/'
            source=source,
        )






       


        return


        # Extract and remove source
        source = parts.pop(0)
        # Extract file name
        name = parts[-1]
        # Construct file
        file = File(name)
        # Construct path
        path = "/" + "/".join(parts)
        
        self._.update(
            file=file,
            full=source + path,
            parts=tuple(parts),
            path=path,
            # Ensure that no source is '/'
            source=source or "/",
        )

        # Remove file part so that parts represents parents
        parts.pop()

        self._.update(
            parents=tuple(parts),
        )

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
    

path = Path('/foo/foo.py.html')