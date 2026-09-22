def main(use: callable, Base: type = None, **kwargs):

    class Bar(Base):
        def __init__(self):
            Base.__init__(self, bar="BAR")

    return Bar
