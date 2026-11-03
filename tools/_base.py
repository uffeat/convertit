class Base:

    def __init__(self, **kwargs):
        self._.update({k: v for k, v in kwargs.items() if v is not None})

    @property
    def _(self) -> dict:
        return self.__dict__.setdefault("__", {})

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    

    
