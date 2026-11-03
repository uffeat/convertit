def main(use, *args, **kwargs):

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
        ... incl intentional (for exploration) different approaches to args and kwargs parsing

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

        def __floordiv__(self, other):
            """TODO Use sets.
            Does not take into account order."""
            # //: Div med nedrund

        def __mod__(self, other):
            """TODO Use sets."""
            # %: Rest

        def __sub__(self, other):
            """TODO Use sets."""

        def __truediv__(self, other):
            """TODO Use sets."""

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

    return Dictionary

