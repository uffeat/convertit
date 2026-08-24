def main(use: callable, Base=None, **kwargs) -> callable:
    """."""

    class Registry(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, _registry={}, **kwargs)

        def __call__(self, *keys, **kwargs):
            """Registers callable."""
            if keys:
                if callable(keys[-1]):
                    keys = list(keys)
                    value = keys.pop()
                    keys = tuple(keys)
                else:
                    value = None
            else:
                value = None

            # NOTE Reliable alternative to using 'global'
            context = dict(keys=keys)

            def register(value):
                keys = context["keys"]
                if not keys:
                    keys = tuple([value.__name__])
                # NOTE Create 'stored' once - NOT in keys loop!
                stored = dict(keys=keys, value=value, kwargs=kwargs)
                for key in keys:
                    self._registry[key] = stored
                return value

            if not value:
                return register
            return register(value)

        def __contains__(self, key) -> bool:
            return key in self._registry

        def __getitem__(self, key):
            """Returns instance."""
            if key in self:
                stored: dict = self._registry[key]
                value = stored["value"]
                if isinstance(value, type):
                    ##print("Instantiating for:", key)  ##
                    kwargs = stored.get("kwargs")
                    if "__init__" in value.__dict__:
                        value = value(owner=self, **kwargs)
                    else:
                        value = value()
                    stored.update(value=value)
                return value

    

    def load(caller):
        return Registry

    return load
