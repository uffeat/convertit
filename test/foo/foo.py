"""
test/foo/foo.py
"""


def main(
    use: callable, Base: type = None, log: callable = None, path: str = None, **kwargs
) -> dict:
    """."""
    from anvil.js import window

    log("window:", window)  ##
    log("use.package:", use.package)  ##
    log("use.meta.DEV:", use.meta.DEV)  ##

    Future = use("use/future/future.py")
    log("Future:", Future)  ##

    class Foo(Base):
        def __init__(self):
            Base.__init__(self, foo="Foo")

    def foo():
        return "foo"

    return dict(Foo=Foo, foo=foo)
