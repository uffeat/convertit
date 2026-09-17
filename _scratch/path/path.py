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
        if kwargs:
            Base.__init__(self, **kwargs)
        else:
            specifier = next(iter(args), None)
            if specifier:

                parts = [p if p else "/" for p in specifier.split("/")]
                if len(parts) == 1:
                    source = ''
                    relative = "/" + specifier
                else:
                    source = parts[0]
                    relative = "/" + "/".join(parts[1:])



                

                


                
                

                path = specifier



                parents = tuple(parts[1:-1])
                parent = parents[-1] if parents else ""


                name = parts[-1]
                _file = {}
                if "." in name:
                    stem, sep, types = name.partition(".")
                    _file.update(
                        file=True,
                        stem=stem,
                        type=types.split(sep)[-1],
                        types=types,
                    )
                else:
                    _file.update(file=False, stem=name)
                Base.__init__(
                    self,
                    name=name,
                    parent=parent,
                    parents=parents,
                    parts=tuple(parts),
                    path=path,
                    relative=relative,
                    source=source,
                    **_file,
                )

    def __call__(self):
        return {**self}

    def __contains__(self, part: str) -> bool:
        """Tests membership with respect to parts."""
        return part in self.parts

    def __repr__(self) -> str:
        return str(self._)

    def __str__(self) -> str:
        return self.path


specifier = '/foo.py'
path = Path(specifier)
print(specifier, repr(path))