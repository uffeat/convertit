class Cache:
    def __init__(self, *args, owner=None, **cache):
        self.__dict__.update(__={})

        
        ##create =  next(iter([a for a in args if callable(a)]), None)
        create =  next(iter([a for a in args if callable(a)]), None)


        

        self._.update(_cache=cache, _create=create, owner=owner)

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, *args, **kwargs):
        """."""
        cache: dict = self._["_cache"]
        if kwargs:
            # Batch-set
            cache.update(kwargs)
            return self


        args = iter(args)
        key = next(args, '')
        value = next(args, None)
        
        if value is None:
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
            #  Implicit None return if no result
        else:
            # Set
            cache[key] = value
            return self

    def __contains__(self, key) -> bool:
        """."""
        return key in self._["_cache"]

    def __getitem__(self, key):
        return self.get(key)

    def __len__(self) -> int:
        """."""
        return len(self._["_cache"])

    def __setitem__(self, key, value):
        self(key, value)

    def __str__(self):
        return str(self._["_cache"])

    @property
    def owner(self):
        return self._["owner"]

    def get(self, key):
        """."""
        return self(key)

    def pop(self, key):
        """."""
