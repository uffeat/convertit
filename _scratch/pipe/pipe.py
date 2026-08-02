class Pipe:
    def __init__(self, name=None, owner=None):
        self.__dict__.update(__={})
        self._.update(detail={}, name=name, owner=owner, _registry=[])

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, value=None, *args, **kwargs):
        """."""

        registry: list = self._["_registry"]
        previous = value
        for index, stored in enumerate(registry):
            runner = stored[0]
            if isinstance(runner, type):
                # Do lazy instantiation
                runner = runner()
                stored[0] = runner

            value = runner(previous, index, self, *args, **kwargs)

            if value is False:
                value = previous
                break

            if value is not None:
                previous = value

        return value

    @property
    def detail(self) -> dict:
        return self._["detail"]

    @property
    def name(self):
        return self._["name"]

    @property
    def owner(self):
        return self._["owner"]

    def clear(self) -> "Pipe":
        """."""
        registry: list = self._["_registry"]
        registry.clear()
        return self

    def add(self, value: callable, index=None):
        """."""
        registry: list = self._["_registry"]
        # Wrap in mutable to enable replacement
        stored = [value]
        registry.append(stored)

    def remove(self, value):
        """."""
        registry: list = self._["_registry"]

    def index(self, value: callable):
        """."""
