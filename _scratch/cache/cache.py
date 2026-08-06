class Cache:
    def __init__(self, *args, **kwargs):
        self.__dict__.update(__={})
        self._.update(_cache=kwargs)

        create = next(iter([a for a in args if callable(a)]), None)
        if create:
            self._.update(_create=create)

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, *args, **kwargs):
        """."""
        cache: dict = self._["_cache"]

        # Set
        for k, v in kwargs.items():
            if v is None:
                # NOTE None removes
                cache.pop(k, None)
            else:
                cache[k] = v

        key = next(iter(args), None)

        if key is None:
            return self

        # Get
        if key in cache:
            return cache[key]

        # Not in cache
        create: callable = self._.get("_create")
        if create:
            value = create(key)
            if value is not None:
                # NOTE Never store None
                cache[key] = value
                return value

    def __contains__(self, key) -> bool:
        return key in self._["_cache"]

    def __getitem__(self, key):
        return self(key)

    def __len__(self) -> int:
        return len(self._["_cache"])

    def __setitem__(self, key, value):
        self(**{key: value})

    def __str__(self):
        return str(self._["_cache"])

    def get(self, key):
        return self(key)

    def pop(self, key, default=None):
        value = self(key)
        self(**{key: None})
        return default if value is None else value

    def onget(self, create: callable) -> callable:
        """."""
        self._.update(_create=create)
        return create
