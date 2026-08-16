def main(
    Base: type = None,
    Log: type = None,
    Path: callable = None,
    anvil=None,
    document=None,
    js=None,
    log: callable = None,
    meta=None,
    path: str = None,
    window=None,
    server=None,
    **kwargs,
):
    """."""

    class Parcel(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _creators={}, _data={}, **kwargs)

        def __call__(self, *args, **kwargs):
            """Registers creator."""
            if callable(args[0]):
                creator, *keys = args
            else:
                creator, keys = None, args

            def register(creator):
                for key in keys:
                    stored = dict(creator=creator, kwargs=kwargs)
                    self._creators[key] = stored

            if not creator:
                return register
            register(creator)

        def __getitem__(self, key):
            """Returns item value."""
            if key in self._data:
                return self._data[key]

            if key in self._creators:
                stored: dict = self._creators[key]
                creator = stored["creator"]
                if isinstance(creator, type):
                    kwargs = stored.pop("kwargs", {})
                    creator = creator(owner=self, **kwargs)
                    stored["creator"] = creator
                value = creator(key)
                self._data[key] = value
                return value

    my_parcel = Parcel()

    @my_parcel("foo")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, key):
            """."""
            return "FOO"

    log("foo:", my_parcel["foo"])
