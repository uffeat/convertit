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

        def __call__(self, *keys, **kwargs):
            """Registers creator."""

            keys = list(keys)
            if keys:
                if callable(keys[-1]):
                    creator = keys.pop()
                else:
                    creator = None
            else:
                creator = None

            # NOTE Alternative to using 'global'
            context = dict(keys=keys)

            def register(creator):
                keys = context["keys"]
                if not keys:
                    keys = [creator.__name__]
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

    @my_parcel("foo", "Foo")
    class cls(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, key):
            return "FOO"

    @my_parcel
    class bar(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, key):
            return "BAR"

    class ding(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, key):
            return "DING"

    my_parcel("ding", ding)

    class dong(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, key):
            return "DONG"

    my_parcel(dong)

    @my_parcel
    def ping(key):
        """."""
        return "PING"

    log("foo:", my_parcel["foo"])
    log("Foo:", my_parcel["Foo"])
    log("bar:", my_parcel["bar"])
    log("ding:", my_parcel["ding"])
    log("dong:", my_parcel["dong"])
    log("ping:", my_parcel["ping"])
