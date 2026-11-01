class Dictionary(dict):
    """
    Native dict subclass with leaner syntax and enhanced features for data
    extraction and in-place mutation.

    Implements a 'no-None' pattern, so that neither keys, nor values can be None.
    Returned None values therefore always means 'no-membership'.
    Setting a None value instructs item deletion.

    Exploits the fact that dicts are ordered.
    Keys can be extracted based on index with a JS-inspired 'at' method.
    Values can be extracted based on index by passing a list with a single integer value to 'get'.


    A word on signatures...
    ... incl intentional (for exploration) different approaces to args and kwargs parsing

    A word on internal state...


    """

    @classmethod
    def create(cls, *args, **kwargs):
        """."""
        if args and isinstance(args[0], cls):
            instance, *args = args
            return instance.update(*args, **kwargs)
        return cls(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Hybrid update/get."""
        # NOTE get role only works for string keys
        key = next((a for a in args if isinstance(a, str)), None)
        return self.get(*args) if key else self.update(*args, **kwargs)

    def __getitem__(self, key):
        """Returns item value by key."""
        if isinstance(key, slice):
            return self.slice(key)

        return self.get(key)

    def __setitem__(self, key, value):
        """Sets item."""
        self.update({key: value})

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def at(self, *args, **kwargs):
        """Returns key at index. Supports positive and negative indices. Returns default if out of range."""
        defaults = [0, None]
        index, default = [*args, *defaults[len(args) :]]
        return (
            list(dict.keys(self))[index]
            if (-len(self) <= index < len(self))
            else default
        )

    def clear(self, *args, **kwargs):
        """Removes all items or items with specific keys."""
        [self.pop(k) for k in args] if args else dict.clear(self)
        return self

    def copy(self):
        """TODO option for deep."""
        return Dictionary(dict.copy(self))

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
        """
        Returns value by key or index.
        Mimics native 'setdefault' if truthy third arg (no index support).
        """
        args = iter(args)
        key, default, patch = next(args, None), next(args, None), next(args, False)
        if patch:
            if default is not None:
                return dict.setdefault(self, key, default)
        else:

            if isinstance(key, list) and len(key) == 1:
                key = self.at(key[0])
            return dict.get(self, key, default)

    def index(self, *args, **kwargs):
        """Returns positive index for key. Returns default, if key missing."""
        args = iter(args)
        key, default = next(args, None), next(args, None)
        return list(dict.keys(self)).index(key) if key in self else default

    def pop(self, *args, **kwargs):
        """Pops item by key (optional default)."""
        args = iter(args)
        key, default = next(args, None), next(args, None)
        if isinstance(key, list) and len(key) == 1:
            key = self.at(key[0])
        return dict.pop(self, key, default)

    def setdefault(self, *args, **kwargs):
        """Native setdefault with support for special None-paradigm."""
        args = iter(args)
        key, value = next(args, None), next(args, None)
        if key is not None:
            if value is None:
                return self.pop(key)
            return dict.setdefault(self, key, value)

    def slice(self, *args, **kwargs) -> "Dictionary":
        """Returns sliced data."""
        _ = {0: None, 1: None, 2: None, **{i: v for i, v in enumerate(args)}}


      

        spec = (
            _[0] if isinstance(_[0], slice) else slice(*list(_.values())[0:3])
        )

        return self.__class__(
            {k: dict.__getitem__(self, k) for k in list(dict.keys(self))[spec]}
        )

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
        """Updates items. None-values remove. None-keys ignored. Supports multiple pos args. Chainable"""

        # Update kwargs from args
        [
            kwargs.update(a)
            for a in (self.dict(a) for a in (a for a in args if a is not None))
        ]
        # Update self
        [
            self.pop(k) if v is None else dict.update(self, {k: v})
            for k, v in kwargs.items()
            if k is not None
        ]
        return self

    @staticmethod
    def dict(value) -> dict:
        """Returns dict-cast non-dict values if possible.
        Returns None, if casting is not possible.
        Returns dict values as-is (no-copying)."""
        if isinstance(value, dict):
            return value
        try:
            return dict(value)
        except:
            pass

    @staticmethod
    def fromkeys(keys, value):
        return Dictionary(dict.fromkeys(keys, value))


if __name__ == "__main__":

    def run(*args, **kwargs):
        def run(test: callable):
            return test(*args, **kwargs)

        return run

    ##@run()
    def test_at():
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)
        print("first key:", data.at(0))
        print("first key:", data.at(-3))
        print("last key:", data.at(2))
        print("last key:", data.at(-1))
        print("key at 3:", data.at(3))
        print("key at -4:", data.at(-4))

    ##@run()
    def test_get():

        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        print("first value:", data.get("a"))
        print("first value:", data.get([0]))

        print("last value:", data.get("c"))  # 3
        print("last value:", data.get([-1]))

        print("missing value:", data.get("d", False))
        print("missing value:", data.get([3], False))

        print("added value:", data.get("d", 4, True))  # 4
        print("data:", data)

    @run()
    def test_slice():

        data = Dictionary(a=1, b=2, c=3, d=4)
        print("data:", data)

        print("first slice:", data[0:1])
        print("first slice:", data.slice(0, 1, 1, 1, 1, 1))

        print("reversed:", data.slice(None, None, -1))

        print("every second:", data.slice(0, 4, 2))

        ##print("data[3:10]:", data[3:10])
        ##print("data[-4:10]:", data[-4:10])

    ##@run()
    def test():

        data = Dictionary(foo=42)

        print("foo:", data("foo"))
        print("bar:", data("bar", 8))
        print("data:", data)
        print("bar:", data("bar", "BAR", True))
        print("data:", data)

        _data = Dictionary.create(data)

        Dictionary.create()

        data(bar="new bar")

        print("_data:", _data)

        data = Dictionary(foo=42, bad=None, stuff=7)
        data(boom="BOOM")
        data(boom=None, bar="BAR")
        data.clear("stuff")
        data(dict(ping="PING"), dict(pong="PONG"))
        data["ding"] = "DING"
        data[(1, 2, 3)] = True

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
