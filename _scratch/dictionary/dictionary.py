class Uid:

    def __init__(self):
        self.__dict__.update(_=dict(value=-1))

    def __call__(self) -> int:
        self._["value"] += 1
        return self.value

    @property
    def value(self):
        return self._["value"]


Uid = Uid()


class Dictionary(dict):

    def __init__(self, *args, **kwargs):
        self.__dict__.update(_=dict(id=Uid()))
        self(*args, **kwargs)

    def __call__(self, *args, **kwargs) -> "Dictionary":
        # Create intermediary to control update order
        updates = dict()
        # Update intermediary from args
        [updates.update(a) for a in args if isinstance(a, dict)]
        [updates.update(dict(a)) for a in args if not isinstance(a, dict)]
        # Update intermediary from kwargs
        updates.update(kwargs)
        # Update
        [
            dict.pop(self, k, None) if v is None else dict.update(self, {k: v})
            for k, v in updates.items()
        ]
        return self

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __getitem__(self, key):
        """Returns item value by key or item section by slice."""
        if isinstance(key, slice):
            return Dictionary({k: self[k] for k in list(dict.keys(self))[key]})
        # NOTE Never key error; missing keys return None
        return dict.get(self, key)

    def __setitem__(self, key, value):
        """Sets item. None-value removes."""
        (
            dict.pop(self, key, None)
            if value is None
            else dict.__setitem__(self, key, value)
        )

    def at(self, index: int, *args):
        """Returns key at index. Supports positive and negative indices. Returns default if out of range."""
        default = next(iter(args), None)
        return next(iter(list(dict.keys(self))[index:]), default)

    def clear(self, *keys) -> "Dictionary":
        """Removes all items or items with specific keys."""
        [dict.pop(self, k, None) for k in keys] if keys else dict.clear(self)
        return self

    def find(self, *args, **kwargs):

        # XXX TODO Refactor to accomodate kwargs; see transform
        predicate = next((a for a in args if callable(a)), None)
        if predicate:

            def result():
                for i, (k, v) in enumerate(dict.items(self)):
                    entry = (i, k, v)
                    result = predicate(*entry)
                    if result is not None:
                        return result

            return result
        else:
            return self.find
            

    @staticmethod
    def from_items(*args):
        """."""
        result = Dictionary()
        for items in args:
            for k, v in items:
                result.set(k, v)
        return result

    def get(self, key, *args, patch=False):
        """Returns item value by key or index."""
        # NOTE patch controls setdefault vs. get
        default = next(iter(args), True if patch else None)
        if isinstance(key, list) and key:
            key = self.at(key[0])
        return (
            dict.setdefault(self, key, default)
            if patch
            else dict.get(self, key, default)
        )

    def index(self, key, default=None):
        """Returns positive index for key. Returns default, if key missing."""
        return list(dict.keys(self)).index(key) if key in self else default

    def pop(self, key, *args):
        """Pops item by key or index (optional default)."""
        default = next(iter(args), None)
        if isinstance(key, list) and key:
            key = self.at(key[0])
        return dict.pop(self, key, default)

    def set(self, key, value):
        """Sets item. None-value removes."""
        self[key] = value
        return self

    def transform(self, *args, **kwargs):
        """Decorates transformer for in-place mutation."""
        # NOTE Inspired by JS map and filter array methods.
        transformer = next((a for a in args if callable(a)), None)
        if transformer:
            # Transform immediately
            if isinstance(transformer, type):
                transformer = (
                    transformer(self, **kwargs)
                    if "__init__" in transformer.__dict__
                    else transformer()
                )
            self({k: transformer(i, k, v) for i, (k, v) in enumerate(dict.items(self))})
            return transformer
        # Return function for later transformation
        # (applies when declared as 'parameter decorator')
        def Transform(transformer):
            def transform():
                return self.transform(transformer, **kwargs)
            return transform
        return Transform
        return lambda transformer: lambda: self.transform(transformer, **kwargs)


if __name__ == "__main__":
    data = Dictionary(foo=42, bad=None, stuff=7)
    data(boom="BOOM")
    data(boom=None, bar="BAR")
    data.clear("stuff")
    data(dict(ping="PING"), dict(pong="PONG"))
    data["ding"] = "DING"
    data[(1, 2, 3)] = True

    print("data.id:", data.id)

    print("data:", data)

    ##print("foo:", data['foo'])

    ##print("index of foo:", data.index("foo"))
    print("index of bar:", data.index("bar"))
    ##print("index of bad:", data.index("bad"))

    ##print("key at 0:", data.at(0))
    ##print("key at 1:", data.at(1))
    print("key at 2:", data.at(2))
    print("key at 10:", data.at(10))

    ##print("key at -1:", data.at(-1))
    ##print("key at -2:", data.at(-2))
    print("key at -3:", data.at(-3))

    ##print('data[0:1]:', data[0:1])
    ##print('data[0:2]:', data[0:2])
    ##print('data[0:4]:', data[0:4])
    print("data[3:10]:", data[3:10])
    print("data[1:-1]:", data[1:-1])

    @data.transform
    def transform(index, key, value, **kwargs):
        if isinstance(value, str):
            return value.lower()
        return value

    @data.transform(test=42)
    class transform:
        def __init__(self, owner, **kwargs):
            """."""
            ##print("kwargs:", kwargs)##

        def __call__(self, index, key, value):
            if key == "pong":
                return
            return value

    transform()

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

    data.pop([-2])

    print("data:", data)

    print("'a' in data:", "a" in data)
    print("'b' in data:", "b" in data)

    data = Dictionary.from_items(data.items(), [["name", "uffe"]])
    print("data:", data)

    @data.find()
    def find(index, key, value):
        if index == 0:
            return {key: value}

    found = find()
    print("found:", found)
