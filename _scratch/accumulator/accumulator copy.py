class Accumulator:
    def __init__(self, name=None, owner=None, result=None):
        self.__dict__.update(__={})
        self._.update(detail={}, name=name, owner=owner, _registry=[], _result=result)

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, value=None, *args, **kwargs):
        """."""
        compute: callable = self._.get("_compute")

        if not compute:

            def compute(*args, **kwargs):
                """."""

        final: callable = self._.get("_final")
        if final and isinstance(final, type):
            expects = getattr(
                final.__dict__.get("__init__"), "__annotations__", {}
            ).keys()
            if "owner" in expects:
                final = final(owner=self)
            else:
                final = final()

        registry: list = self._["_registry"]
        result = self._["_result"]
        if isinstance(compute, type):
            expects = getattr(
                compute.__dict__.get("__init__"), "__annotations__", {}
            ).keys()
            if "owner" in expects:
                compute = compute(owner=self)
            else:
                compute = compute()
        result = compute(value, result=result) or result
        previous = value
        for index, stored in enumerate(registry):
            runner = stored[0]
            if isinstance(runner, type):
                # Lazy instantiation
                runner = runner()
                stored[0] = runner
            value = runner(previous, index, result, self, *args, **kwargs)
            if value is False:
                # NOTE By convention, False wraps up based on previous runs
                value = previous
                break
            if value is not None:
                previous = value
                result = compute(value, result=result) or result

        if final:
            return final(result)

        return result

    @property
    def detail(self) -> dict:
        return self._["detail"]

    @property
    def name(self):
        return self._["name"]

    @property
    def owner(self):
        return self._["owner"]

    def compute(self, value: callable):
        """."""
        if value is None:
            return self._.pop("_compute", None)
        self._["_compute"] = value
        return value

    def clear(self) -> "Accumulator":
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
        return value

    def final(self, value: callable):
        """."""
        if value is None:
            return self._.pop("_final", None)
        self._["_final"] = value
        return value

    def remove(self, index: int):
        """."""
        registry: list = self._["_registry"]
        size = len(registry)
        # XXXUse pop?
        if -size < index <size+1:
            value = registry.index(index)
            registry.remove(value)

        

    