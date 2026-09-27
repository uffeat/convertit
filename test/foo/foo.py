def main(
    use: callable,
    Base: type = None,
    locals: dict = None,
    log: callable = None,
    path: str = None,
    test: callable = None,
    **kwargs
) -> dict:
    """test/foo/foo.py"""
    from anvil.js import window

    Path = use("use/path/path.py")
    log("Path:", Path)  ##

    log("window:", window)  ##
    log("use.package:", use.package)  ##
    log("use.meta.DEV:", use.meta.DEV)  ##

    log("locals:", locals)  ##

    log("Future:", use("use/future/future.py"))  ##

    log("Bar:", test("test/foo/bar.py").Bar)  ##

    log("foo:", test("test/foo/foo.js").foo())  ##

    class Foo(Base):
        def __init__(self):
            Base.__init__(self, foo="Foo")

    def foo():
        return "foo"

    return foo
