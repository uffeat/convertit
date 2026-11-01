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

    @property
    def _(self) -> dict:
        """."""
        return self.__dict__.setdefault("__", {})

    def __getattr__(self, key: str):
        # Ensure that getattr and hasattr works
        if key not in self._:
            raise AttributeError(key)
        return self._[key]

    def __call__(self, *args, **kwargs):
        """Hybrid update/get."""
        # NOTE get role only works for string keys and index lists
        key = next((a for a in args if isinstance(a, (list, str))), None)
        return self.get(*args) if key else self.update(*args, **kwargs)

    def __getitem__(self, key):
        """Returns item value by key."""
        if isinstance(key, slice):
            return self.slice(key)
        return self.get(key)

    def __setitem__(self, key, value):
        """Sets item."""
        self.update({key: value})

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
        """Decorates find callable for first-occurrence search."""
        find = next((a for a in args if callable(a)), None)
        if find:
            find, *args = args
            if isinstance(find, type):
                find = (
                    find(self, *args, **kwargs)
                    if "__init__" in find.__dict__
                    else find()
                )

            def result(*args, **kwargs):
                for index, item in enumerate(dict.items(self)):
                    result = find(index, *item)
                    if result is not None:
                        return result

            return result
        return self.find

    def get(self, *args, **kwargs):
        """Returns value by key or index."""
        args = iter(args)
        key = next(args, None)
        if isinstance(key, list) and key:
            key = self.at(key[0])
        return dict.__getitem__(self, key) if key in self else next(args, None)

    def index(self, *args, **kwargs):
        """Returns positive index for key. Returns default, if key missing."""
        args = iter(args)
        key = next(args, None)
        return list(dict.keys(self)).index(key) if key in self else next(args, None)

    def pop(self, *args, **kwargs):
        """Pops item by key (optional default)."""
        args = iter(args)
        key, default = next(args, None), next(args, None)
        if isinstance(key, list) and key:
            key = self.at(key[0])
        return dict.pop(self, key, default)

    def setdefault(self, *args, **kwargs):
        """Native setdefault with support for special None-paradigm."""
        args = iter(args)
        key, value = next(args, None), next(args, None)
        if key is not None and value is not None:

            return dict.setdefault(self, key, value)

    def slice(self, *args, **kwargs) -> "Dictionary":
        """Returns sliced data."""
        defaults = dict.fromkeys(range(3), None)
        args = {
            **defaults,
            **{i: v for i, v in enumerate(args) if i < len(defaults)},
        }
        spec = args[0] if isinstance(args[0], slice) else slice(*args.values())
        return self.__class__(
            {k: dict.__getitem__(self, k) for k in list(dict.keys(self))[spec]}
        )

    def transform(self, *args, **kwargs):
        """Decorates transformer for in-place mutation."""
        # NOTE Inspired by JS map and filter array methods.
        transformer = next((a for a in args if callable(a)), None)
        if transformer:
            # Transform
            transformer, *args = args
            if isinstance(transformer, type):
                transform = (
                    transformer(self, *args, **kwargs)
                    if "__init__" in transformer.__dict__
                    else transformer()
                )
            else:
                transform = transformer
            self.update(
                {k: transform(i, k, v) for i, (k, v) in enumerate(dict.items(self))}
            )
            return transformer
        return self.transform

    def update(self, *args, **kwargs):
        """Updates items. None-values remove. None-keys ignored. Supports multiple pos args. Chainable"""
        updates = {}
        for a in args:
            try:
                updates.update(dict(a))
            except:
                continue
        updates.update(kwargs)
        if self:
            for key, value in updates.items():
                if key is not None:
                    getattr(dict, "pop" if value is None else "__setitem__")(
                        self, key, value
                    )
        else:
            dict.update(
                self,
                {k: v for k, v in updates.items() if k is not None and v is not None},
            )
        return self

    @staticmethod
    def fromkeys(keys, value):
        return Dictionary(dict.fromkeys(keys, value))


if __name__ == "__main__":

    def run(*args, **kwargs):
        def run(test: callable):
            return test(*args, **kwargs)

        return run

    ##@run()
    def test():
        """Tests init and update."""

        data = Dictionary(foo=42)
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

        data = Dictionary(Sim(a="A", b="B", c=None))
        data(Sim(d="D", b=None), foo=42)

        print("data:", data)

    ##@run()
    def test():
        """Tests at method."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)
        print("first key:", data.at(0))
        print("first key:", data.at(-3))
        print("last key:", data.at(2))
        print("last key:", data.at(-1))
        print("key at 3:", data.at(3))
        print("key at -4:", data.at(-4))

    ##@run()
    def test():
        """Tests get method."""

        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        print("first value:", data.get("a"))
        print("first value:", data.get([0]))

        print("last value:", data.get("c"))  # 3
        print("last value:", data.get([-1]))

        print("missing value:", data.get("d", False))
        print("missing value:", data.get([3], False))

    ##@run()
    def test():
        """Tests slicing features."""

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
        """Tests index method."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)
        print("index of a:", data.index("a"))
        print("index of c:", data.index("c"))
        print("index of e:", data.index("e", "missing"))

    ##@run()
    def test():
        """Tests transform."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        @data.transform
        def transform(index, key, value):
            if isinstance(value, int):
                return 2 * value
            return value

        print("data:", data)

        @data.transform(42, foo=42)
        class transform:
            def __init__(self, owner, *args, **kwargs):
                """."""
                print("owner:", owner)  ##
                print("args:", args)  ##
                print("kwargs:", kwargs)  ##

            def __call__(self, index, key, value):
                if isinstance(value, int):
                    return value + 2
                return value

        print("data:", data)

    ##@run()
    def test():
        """Tests find."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        # Decorated function
        @data.find
        def find(index, key, value):
            if index == 2:
                return 2 * value

        print("found:", find())

        # Decorated class
        @data.find()
        class find:
            def __init__(self, owner, *args, **kwargs):
                self._.update(owner=owner)

            @property
            def _(self) -> dict:
                return self.__dict__.setdefault("__", {})

            def __getattr__(self, key: str):
                if key not in self._:
                    raise AttributeError(key)
                return self._[key]

            def __call__(self, index, key, value):
                if index == 0:
                    return {key: value}, str(self.owner)

        print("found:", find())

        # External class
        class find:
            def __init__(self, owner, *args, **kwargs):
                self._.update(owner=owner, foo=kwargs.pop("foo", None))

            @property
            def _(self) -> dict:
                return self.__dict__.setdefault("__", {})

            def __getattr__(self, key: str):
                if key not in self._:
                    raise AttributeError(key)
                return self._[key]

            def __call__(self, index, key, value):
                return self.owner.get("a"), self.foo

        print("found:", data.find(find, foo=42)())

        # External function
        def find(index, key, value):
            if index == 2:
                return index, key, value

        print("found:", data.find(find)())

    ##@run()
    def test():
        """Tests pop."""

        data = Dictionary(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=9, i=10)
        print("data:", data)

        popped = data.pop([-1])
        print("popped:", popped)
        print("data:", data)

        popped = data.pop([20], 42)
        print("popped:", popped)
        print("data:", data)

        popped = data.pop("b")
        print("popped:", popped)
        print("data:", data)

        data["c"] = None
        print("data:", data)

        data.update(e=None)
        print("data:", data)

        data(d=None, f=None)
        print("data:", data)

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
