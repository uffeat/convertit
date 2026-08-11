def main(use: callable, **kwargs) -> dict:
    """."""
    Base = use("/tools/base.py")

    class Foo(Base):
        def __init__(self):
            Base.__init__(self, foo="Py foo")
           

        @property
        def foo(self):
            return self._["foo"]
        
    def foo():
        print('foo')

    
    return Foo, foo
    return dict(Foo=Foo, foo=foo)
