def main(use, *args, **kwargs) -> dict:

    

    class Bar:
        def __init__(self):
            """."""

        @property
        def bar(self):
            return 'BAR'

    bar = Bar()
            

    def stuff():
        return 42

    return Bar, stuff, dict(bar=bar)
