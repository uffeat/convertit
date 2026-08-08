def main(use, **kwargs):
    Base = use("/tools/base.py")

    class Bar(Base):
        def __init__(self):
            Base.__init__(self)
            self._.update(foo="Py bar")

        @property
        def bar(self):
            return self._['bar']

    return Bar
