class Base:

    def __init__(self, **kwargs):
        self.__dict__.update(__={})
        self._.update({k: v for k, v in kwargs.items() if v is not None})

    @property
    def _(self) -> dict:
        return self.__

    def __getattr__(self, key: str):
        return self._.get(key)



export = Base


