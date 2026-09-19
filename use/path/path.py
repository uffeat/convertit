def main(use, Base: type = None, **kwargs) -> type:
    """."""

    
    class Path(Base):

        def __init__(self, *args, **kwargs):
            Base.__init__(self)
            if kwargs:
                self._.update(**kwargs)
            else:
                self._.update(**self(*args))

        def __call__(self, *args) -> dict:
            """."""
            first = next(iter(args), "")
            if isinstance(first, self.__class__):
                return dict(**first)
            result = dict()
            path = first
            # dirs
            if "/" in path:
                # Avoid leading '' in parts when path starts with /
                parts = [p if i or p else "/" for i, p in enumerate(path.split("/"))]
                source, name = parts[0], parts[-1]
            else:
                parts, name, source = [path], path, ""
            # file
            if "." in name:
                stem, _, types = name.partition(".")
                result.update(type=types.split(".")[-1])
            else:
                stem, types = name, ""
                result.update(type=types)
            result.update(
                file=bool(types),
                name=name,
                parts=tuple(parts),
                path=path,
                relative=f"/{'/'.join(parts[1:])}" if source else f"/{path}",
                source=source,
                stem=stem,
                types=types,
            )
            return result

        def __bool__(self) -> bool:
            return bool(self._.get("path", ""))

        def __contains__(self, part: str) -> bool:
            """Tests membership with respect to parts."""
            return part in self._.get("parts", [])

        def __len__(self) -> int:
            return len(self._.get("parts", []))

        def __repr__(self) -> str:
            return str(self._)

        def __str__(self) -> str:
            return self._.get("path", "")

    return Path
