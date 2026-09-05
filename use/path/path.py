def main(use, Base=None, **kwargs) -> type:
    """."""

    def parse(specifier: str) -> dict:
        """."""
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

        return dict(
            name=name,
            parent=parent,
            parents=parents,
            parts=parts,
            path=path,
            relative=relative,
            source=source,
            **_file,
        )

    class Path(Base):
        def __init__(self, specifier: str):
            Base.__init__(self)
            self(specifier)


        def __call__(self, specifier: str):
            parsed = parse(specifier)
            self._.update(**parsed)
            return parsed

        def __contains__(self, part: str) -> bool:
            """Tests membership with respect to parts."""
            return part in self.parts

        def __str__(self) -> str:
            return self.path

    return Path
