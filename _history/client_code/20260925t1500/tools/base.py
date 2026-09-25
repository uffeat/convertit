from .dictionary import Dictionary


class Base:

    def __init__(self, *args, **kwargs):
        _ = Dictionary({k: v for k, v in kwargs.items() if v is not None})
        # Enable use of __setattr__
        self.__dict__.update(__=_)

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
