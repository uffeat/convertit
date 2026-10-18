class Private(dict):

    def __init__(self, *args, **kwargs):

        self(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> "Private":
        # Create intermediary to control update order
        updates = dict()
        # Update intermediary from args
        [updates.update(a) for a in args if isinstance(a, dict)]

        def update(a):
            try:
                updates.update(dict(a))
            except:
                pass

        [updates.update(dict(a)) for a in args if not isinstance(a, dict)]
        # Update intermediary from kwargs
        updates.update(kwargs)
        # Update
        [
            dict.pop(self, k, None) if v is None else dict.update(self, {k: v})
            for k, v in updates.items()
        ]
        return self

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Private({k: self[k] for k in list(self.keys())[key]})
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        """."""
        (
            dict.pop(self, key, None)
            if value is None
            else dict.__setitem__(self, key, value)
        )

    def at(self, index: int, default=None):
        """Returns key at index. Supports positive and negative indices. Returns default if out of range."""
        return next(iter(list(self.keys())[index:]), default)

    def clear(self, *keys) -> "Private":
        """."""
        [dict.pop(self, k, None) for k in keys] if keys else dict.clear(self)
        return self

    def index(self, key, default=None):
        """Returns positive index for key. Returns default, if key missing."""
        return list(self.keys()).index(key) if key in self else default

    def transform(self, *args):
        """Decorates transformer."""
        transformer = next((a for a in args if callable(a)), None)
        if transformer:
            # Transform immediately
            self({k: transformer(i, k, v) for i, (k, v) in enumerate(self.items())})
            return transformer
        # Return function for later transformation
        return lambda transformer: lambda: self.transform(transformer)


if __name__ == "__main__":
    data = Private(foo=42, bad=None, stuff=7)
    data(boom="BOOM")
    data(boom=None, bar="BAR")
    data.clear("stuff")
    data(dict(ping="PING"), dict(pong="PONG"))
    data["ding"] = "DING"

    ##print("popped:", data.pop(["pong", "pang"]))

    print("data:", data)

    ##print("foo:", data['foo'])

    ##print("index of foo:", data.index("foo"))
    ##print("index of bar:", data.index("bar"))
    ##print("index of bad:", data.index("bad"))

    ##print("key at 0:", data.at(0))
    ##print("key at 1:", data.at(1))
    ##print("key at 2:", data.at(2))
    ##print("key at 10:", data.at(10))

    ##print("key at -1:", data.at(-1))
    ##print("key at -2:", data.at(-2))
    ##print("key at -3:", data.at(-3))

    ##print('data[0:1]:', data[0:1])
    ##print('data[0:2]:', data[0:2])
    ##print('data[0:4]:', data[0:4])
    ##print('data[1:-1]:', data[1:-1])

    @data.transform  ##()
    def transform(index, key, value):
        if key == "pong":
            return
        if isinstance(value, str):
            return value.lower()
        return value

    ##data.transform(transform)

    ##print("transform:", transform)
    ##transform()

    data[(1, 2, 3)] = True
    ##print("data:", data)

    ##data.clear()

    print("data:", data)

    class Sim:

        def __init__(self, **kwargs):
            self.__dict__.update(_=kwargs)

        def __getitem__(self, key):
            # Facilitate **-unpacking
            return self._.get(key)

        def keys(self):
            # Facilitate **-unpacking
            return self._.keys()

   

    data(Sim(a="A", b="B"))

    print("data:", data)

    print("as dict:", dict(Sim(a="A", b="B")))
