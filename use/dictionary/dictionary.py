

def main(
    use,
    Base: type = None,
    log: callable = None,
    path: str = None,
    state:dict=None,
    **kwargs,
):



    class Dictionary(dict):
        def __init__(self, *args, **kwargs):
            dict.__init__(self)
            self(*args, **kwargs)

        def __call__(self, *args, **kwargs) -> "Dictionary":
            for a in args:
                try:
                    kwargs.update(**a)
                except:
                    pass
            for k, v in kwargs.items():
                self.pop(k, None) if v is None else self.update({k: v})
            return self



    return Dictionary
