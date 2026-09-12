def main(use, tools=None, **kwargs) -> type:
    """."""

    Base = tools.base.Base

    class PathType(Base):
        def __init__(self, specifier: str):

            path = specifier
            parts = tuple([p if p else "/" for p in path.split("/")])
            source = parts[0]
            relative = "/" + "/".join(parts[1:])
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
                _file.update(stem=name)

            Base.__init__(
                self,
                name=name,
                parent=parent,
                parents=parents,
                parts=parts,
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

        def __str__(self) -> str:
            return self.path

    def Path(specifier: str) -> PathType:
        if isinstance(specifier, PathType):
            return specifier
        return PathType(specifier)

    return Path
