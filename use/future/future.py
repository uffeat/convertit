def main(use, **kwargs) -> type:
    """."""

    class Future:

        def __init__(self):
            pwr = use.js.Promise.withResolvers()
            self._ = dict(promise=pwr.promise, resolve=pwr.resolve)

        def __call__(self, value=True) -> "Future":
            """Resolves promise."""
            self._["resolve"](value)
            return self

        def wait(self):
            """Awaits promise and returns resolved value."""
            value = use.anvil.js.await_promise(self._["promise"])
            return value

    return Future
