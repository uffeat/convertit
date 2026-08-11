def main(use, **kwargs)-> type:

    
    class List(list):
        def __init__(self, *items):
            """."""
            self.append(*items)

        def __getitem__(self, arg):
            if isinstance(arg, int):
                if not (-len(self) <= arg < len(self)):
                    return
            return super().__getitem__(arg)

        @property
        def size(self):
            return len(self)

        def append(self, *items):
            for item in items:
                super().append(item)
            return self

        def extend(self, *items):
            for item in items:
                super().extend(item)
            return self

        def index(self, *args, default=None):
            try:
                return super().index(*args)
            except:
                return default

        def pop(self, index=-1, default=None):
            if not (-len(self) <= index < len(self)):
                return default
            return super().pop(index)

        def filter(self, predicate: callable) -> list:
            """."""

            def filter():
                return [
                    item for index, item in enumerate(self) if predicate(item, index, self)
                ]

            return filter

        def find(self, predicate: callable):
            """."""
            for index, item in enumerate(self):
                if predicate(item, index, self):
                    return item

        def map(self, transformer: callable) -> list:
            """."""
            return [transformer(item, index, self) for index, item in enumerate(self)]

        def reduce(self):
            """."""


    
        
    return List
        






