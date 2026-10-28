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


sequence = List(1, 2, 3)


print("sequence:", sequence)
print("first:", sequence[0])
print("first:", sequence[-len(sequence)])
print("last:", sequence[-1])
print("last:", sequence[len(sequence) - 1])
print("bad:", sequence[3])
print("bad:", sequence[-4])

##sequence[0] = 10
##print("first:", sequence[0])

print("popped:", sequence.pop(-4))
print("sequence:", sequence)



numbers = List(1, 2, 3, 4, 5, 6, 7)


