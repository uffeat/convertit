def main(use, anvil=None, js=None, window=None, **kwargs) -> type:
    """."""

    Promise = window.Promise
    await_promise = anvil.js.await_promise

    class Future:

        def __init__(self):
            pwr = Promise.withResolvers()
            self._ = dict(promise=pwr.promise, resolve=pwr.resolve)

        def __call__(self, value=True) -> "Future":
            """Resolves promise."""
            self._["resolve"](value)
            return self

        def wait(self):
            """Awaits promise and returns resolved value."""
            value = await_promise(self._["promise"])
            return value

    return Future
