class log:
    def __init__(self):
        """."""
        self.__dict__.update(__=dict(foo=42))

    def __call__(self, *args):
        """Enables remote logging."""
        print(self.__['foo'])


log = log()


log()