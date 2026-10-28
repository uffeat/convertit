class Iterator:
    def __init__(self, data):
        self.__dict__.update(_=dict(data=iter(data)))

    def __call__(self, default=None):
        return next(self._["data"], default)


_ = dict()


class Dictionary(dict):
    @classmethod
    def create(cls, *args, **kwargs):
        """."""
        if args:
            instance, *_args = args
            if isinstance(instance, cls):
                return instance.update(*_args, **kwargs)
        return cls(*args, **kwargs)

    def __init__(self, *args, **kwargs):

        self.update(*args, **kwargs)
        self._.update(id=_.setdefault("id", 0))
        _["id"] += 1

    def __call__(self, *args, **kwargs):
        """Hybrid update/get."""
        key = next((a for a in args if isinstance(a, str)), None)
        return self.get(*args) if key else self.update(*args, **kwargs)

    def __getitem__(self, key):
        """Returns item value by key."""
        if isinstance(key, slice):
            return self.__class__({k: self[k] for k in list(self.keys())[key]})
        return self.get(key)

    def __setitem__(self, key, value):
        """Sets item."""
        self.update({key: value})

    @property
    def _(self) -> dict:
        if "__" not in self.__dict__:
            self.__dict__.update(__={})
        return self.__

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    @property
    def id(self) -> int:
        """."""
        return self._.get("id")

    def at(self, *args, **kwargs):
        """Returns key at index. Supports positive and negative indices. Returns default if out of range."""
        args = iter(args)
        index, default = next(args, 0), next(args, None)
        return next(iter(list(self.keys())[index:]), default)

    def clear(self, *args, **kwargs):
        """Removes all items or items with specific keys."""
        [self.pop(k) for k in args] if args else dict.clear(self)
        return self

    def find(self, *args, **kwargs):
        """."""
        predicate = next((a for a in args if callable(a)), None)
        if predicate:

            if isinstance(predicate, type):
                predicate = (
                    predicate(self, **kwargs)
                    if "__init__" in predicate.__dict__
                    else predicate()
                )

            def result():
                for i, (k, v) in enumerate(self.items()):
                    entry = (i, k, v)
                    result = predicate(*entry)
                    if result is not None:
                        return result

            return result

        return self.find

    def get(self, *args, **kwargs):
        """Returns value by key or default, if provided as second arg and key not in items.
        Updates items with default, if key not in items and a third truthy arg provided.
        """
        args = iter(args)
        key, default = next(args, None), next(args, None)
        return (
            self.setdefault(key, default)
            if next(args, False)
            else dict.get(self, key, default)
        )

    def index(self, *args, **kwargs):
        """Returns positive index for key. Returns default, if key missing."""
        args = iter(args)
        key, default = next(args, None), next(args, None)
        return list(self.keys()).index(key) if key in self else default

    def pop(self, *args, **kwargs):
        """Pops item by key (optional default)."""
        args = iter(args)
        key, default = next(args, None), next(args, None)
        if key and isinstance(key, list):
            key = self.at(key[0])

        return dict.pop(self, key, default)

    def setdefault(self, *args, **kwargs):
        """Native setdefault with support for None-value removes."""
        args = iter(args)
        key, value = next(args, None), next(args, None)
        if value is None:
            return self.pop(key)
        return dict.setdefault(self, key, value)

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
            self.update(
                {k: transformer(i, k, v) for i, (k, v) in enumerate(self.items())}
            )
            return transformer

        # Return function for later transformation
        # (applies when declared as 'parameter decorator')
        def Transform(transformer):
            def transform():
                return self.transform(transformer, **kwargs)

            return transform

        return Transform

    def update(self, *args, **kwargs):
        """Updates items. None-values remove. Supports multiple pos args. Chainable"""
        # Update kwargs from args
        [kwargs.update(dict(a)) for a in args]
        # Update self
        [
            self.pop(k) if v is None else dict.update(self, {k: v})
            for k, v in kwargs.items()
        ]
        return self

    @staticmethod
    def fromkeys(keys, value):
        return Dictionary(dict.fromkeys(keys, value))


if __name__ == "__main__":

    data = Dictionary(foo=42)
    print("data.id:", data.id)
    print("foo:", data("foo"))
    print("bar:", data("bar", 8))
    print("data:", data)
    print("bar:", data("bar", "BAR", True))
    print("data:", data)

    _data = Dictionary.create(data)

    Dictionary.create()

    data(bar="new bar")
    print("_data.id:", _data.id)
    print("_data:", _data)

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

    print("data.id:", data.id)
    print("data:", data)

    print("'a' in data:", "a" in data)
    print("'b' in data:", "b" in data)

    print("data.id:", data.id)

    data[None] = True  ###

    print("data:", data)

    @data.find()
    def find(index, key, value):
        if index == 0:
            return {key: value}

    found = find()
    print("found:", found)

    @data.find()
    class find:
        def __init__(self, owner, **kwargs):
            """."""
            ##print("kwargs:", kwargs)##

        def __call__(self, index, key, value):
            if index == 0:
                return {key: value}

    found = find()
    print("found:", found)
