def main(use):
    Base = use("@@/base/base.py").Base

    class Foo(Base):
        def __init__(self):
            Base.__init__(self)
            self._.update(foo="Py foo")

        @property
        def foo(self):
            return self._['foo']

    return dict(Foo=Foo)
