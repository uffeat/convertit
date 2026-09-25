class Dictionary(dict):
    def __call__(self, *args, **kwargs) -> 'Dictionary':
        self.update(*args, **kwargs)
        return self

