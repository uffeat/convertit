from tools import Path as _Path


class File:
    """."""

    @property
    def name(self) -> str:
        """."""


    @property
    def type(self) -> str:
        """."""

    @property
    def types(self) -> tuple:
        """."""


class Path(_Path):
    def __init__(self, specifier):
        _Path.__init__(self, specifier)

    @property
    def file(self) -> File:
        return self._["file"]

    @property
    def parts(self) -> tuple:
        return self._["parts"]

    @property
    def path(self) -> str:
        return self._["path"]
