def main(use, Base=None, **kwargs):
    """."""

    DASH = "/"
    DOT = "."

    class Path(Base):
        def __init__(self, specifier: str):
            Base.__init__(self, specifier=specifier)
            source, _, _path = specifier.partition(DASH)
            path = f"{DASH}{_path}"
            _parents, _, name = specifier.rpartition(DASH)
            parents = _parents.split(DASH)
            parents.pop(0)
            if DOT in name:
                # Handle file
                stem, _, types = name.partition(DOT)
                shapes, _, type_ = types.rpartition(DOT)
                self._.update(
                    # is-file flag
                    file=True,
                    # file suffixes without file type
                    shapes=shapes,
                    # file type
                    type=type_,
                    # All file suffixes
                    types=types,
                )
            else:
                stem = name
            self._.update(
                # path with source
                full=source + path,
                # name of file of leaf dir
                name=name,
                # parents of file or leaf dir. Does not include source
                parents=tuple(parents),
                # path parts without source, but with file or leaf dir stem
                parts=tuple([*parents, stem]),
                # path relative to source. Always starts with '/'
                path=path,
                # Ensure that no source is interpreted as '/'
                source=source or DASH,
                # stem of file or leaf dir
                stem=stem,
            )

        @property
        def _(self) -> dict:
            return self.__

        def __contains__(self, part: str) -> bool:
            """Tests membership with respect to parts."""
            return part in self.parts

        def __getitem__(self, a):
            """Returns parts part of slice."""
            if isinstance(a, slice):
                start, stop = a.start, a.stop
                if (
                    isinstance(start, int)
                    and not isinstance(start, bool)
                    and isinstance(stop, int)
                    and not isinstance(stop, bool)
                ):
                    # Standard slicing
                    return self.parts[a]

                print(f"Not implemented: {start}:{stop}")  ##
                return

            elif isinstance(a, int) and not isinstance(a, bool):
                # Standard item by index, but without index errors; out-of-index returns None
                if -len(self) <= a < len(self):
                    return self.parts[a]

            print(f"Not implemented: [{a}]")  ##

        def __len__(self) -> int:
            """Returns number of parts."""
            return len(self.parts)

        def __repr__(self) -> str:
            return str(self._)

        def __str__(self) -> str:
            return self.full

    def load(caller):
        return Path

    return load
