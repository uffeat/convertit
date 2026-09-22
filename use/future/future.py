def main(use: callable, **kwargs) -> type:
    """."""
    from anvil.js import await_promise, window

    class Future:

        def __init__(self):
            pwr = window.Promise.withResolvers()
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
