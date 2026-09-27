def main(use, Base: type = None, log=None, node=None, text=None, **kwargs) -> dict:

    class Bar(Base):
        def __init__(self):
            Base.__init__(self, bar="BAR")

    def bar():
        return 42

    return dict(Bar=Bar)
