from types import MappingProxyType, MethodType


class Dictionary(dict):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(__={})
        self.update(*args, **kwargs)

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, *args, **kwargs) -> "Dictionary":
        self.update(*args, **kwargs)
        return self

    def X__getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Dictionary({k: self[k] for k in list(self.keys())[key]})
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        """."""
        self.update({key: value})

    def __sub__(self, other):
        return self.difference(other)

    def pop(self, key, default=None):
        if isinstance(key, list):
            values = [self.get(k, default) for k in key]
            self.update({k: None for k in key})
            return values
        value = self.get(key, default)
        self.update({key: None})
        return value

    def popitem(self, index=-1) -> tuple:
        """."""
        key = self.at(index)
        value = self.pop(key)
        return key, value

    def setdefault(self, key, default=True):
        """."""
        if key not in self:
            self.update(**{key: default})
        # NOTE Use get since None-values are never written
        return self.get(key)

    def update(self, *args, **kwargs):
        # Create intermediary to control update order
        updates = dict()
        # Update intermediary from args
        [updates.update(a) for a in args]
        # Update intermediary from kwargs
        updates.update(kwargs)
        difference = self.difference(updates)
        [
            dict.pop(self, k, None) if other is None else dict.update(self, {k: other})
            for k, (own, other) in difference.items()
        ]

        result = (
            MappingProxyType({k: v for k, (_, v) in difference.items()}),
            MappingProxyType({k: v for k, (v, _) in difference.items()}),
        )

        if hasattr(self, "onchange"):
            
            self.onchange(*result)

        return result

    def at(self, index: int, default=None):
        """Returns key at index. Supports positive and negative indices. Returns default if out of range."""
        return next(iter(list(self.keys())[index:]), default)

    def clear(self, *keys) -> "Dictionary":
        """."""
        if not keys:
            keys = self.keys()
        self.update({k: None for k in keys})
        return self

    def difference(self, other: dict) -> dict:
        """."""
        return MappingProxyType(
            {
                k: (self.get(k), v)
                for k, v in other.items()
                if (k in self and v is None)
                or (k in self and v != self[k] or (k not in self and v is not None))
            }
        )

    def enumerate(self):
        """."""
        return enumerate(self.items())

    def index(self, key, default=None):
        """Returns positive index for key. Returns default, if key missing."""
        return list(self.keys()).index(key) if key in self else default

    def onchange(self, current, previous):
        """."""
        onchange = self._.get('onchange')
        if callable(onchange):
            onchange(self, current, previous)


    def transform(self, *args):
        """Decorates transformer."""
        transformer = next((a for a in args if callable(a)), None)
        if transformer:
            # Transform immediately
            self.update(
                {k: transformer(i, k, v) for i, (k, v) in enumerate(self.items())}
            )
            return self
        # Return function for later transformation
        return lambda transformer: lambda: self.transform(transformer)


if __name__ == "__main__":
    data = Dictionary(foo=42, bad=None, stuff=7)
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

    ##print("data.enumerate():", data.enumerate())
    ##print("data.enumerate():", [*data.enumerate()])
    ##print("data.enumerate():", [(index, item[0], item[1]) for index, item in data.enumerate()],)

    def onchange(self, current, previous):
        """."""
        print("previous:", previous)
        print("current:", current)

    ##data.__dict__.update(onchange=MethodType(onchange, data))

    data._.update(onchange=onchange)


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

    ##print("popped:", data.popitem())

    print("data:", data)

    other = dict(foo=42, bar=8, kapow=True, no=None, ding=None)
    difference = data.difference(other)
    difference = data - other
    ##print("difference:", difference)
