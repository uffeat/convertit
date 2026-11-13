def main(use, *args, **kwargs):
    """."""
    class MiniDict(dict):

        def __call__(self, *args, **kwargs):
            return self.update(*args, **kwargs)

        def __getitem__(self, key):
            return dict.get(self, key)

        def __setitem__(self, key, value):
            getattr(dict, "pop" if value is None else "__setitem__")(self, key, value)
            return self

        def pop(self, *args, **kwargs):
            return dict.pop(self, *[*args, *[None, None][len(args) :]][0:2])

        def update(self, *args, **kwargs):
            for value in args:
                kwargs.update(value)
            for key, value in kwargs.items():
                getattr(dict, "pop" if value is None else "__setitem__")(self, key, value)
            return self

    return MiniDict
