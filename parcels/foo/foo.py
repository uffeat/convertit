def main(use: callable) -> dict:
    """Returns Foo."""
    Base = use("@@/base/base.py").Base

    class Foo(Base):
        def __init__(self):
            Base.__init__(self)
            self._.update(foo="Py foo")

        @property
        def foo(self):
            return self._["foo"]
        
    def foo():
        print('Foo')

    return dict(Foo=Foo, foo=foo)
