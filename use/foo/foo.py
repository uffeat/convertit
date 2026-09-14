def main(use: callable, Base: type = None, log=None, **kwargs) -> dict:
    """."""
    log("use.meta.DEV:", use.meta.DEV)  ##

    

    class Foo(Base):
        def __init__(self):
            Base.__init__(self, foo="Foo")

    def foo():
        return "foo"

    
   
    return dict(Foo=Foo, foo=foo)
