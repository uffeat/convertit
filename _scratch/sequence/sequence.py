class List(list):
    def __init__(self, *args, **kwargs):
        """."""
        self.append(*args)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get(index)
        return list.__getitem__(self, index)

    def __setitem__(self, index, value):
        # Never add None
        if value is not None:
            if not (-len(self) <= index < len(self)):
                # append if out of range
                index = len(self)
            return list.__setitem__(self, index, value)

    def append(self, *args, **kwargs):
        for value in args:
            # Never add None
            if value is not None:
                list.append(self, value)
        return self

    def extend(self, *args, **kwargs):
        """."""
        for extension in args:
            # Never add None
            list.extend(self, [v for v in extension if v is not None])
        return self

    def index(self, *args, **kwargs):
        """Returns index for first occurance of a given value."""
        value, *args = args
        if value in self:
            return list.index(self, value, *args)

    def insert(self, *args, **kwargs):
        """."""
        args = iter(args)
        index, value = next(args, -1), next(args, True)
        if value is not None:
            list.insert(self, index, value)
        return self

    def pop(self, *args, **kwargs):
        """."""
        if args:
            index, *args = args
            default = args[0] if args else None
        else:
            index = -1
            default = kwargs.get('default')

        if not (-len(self) <= index < len(self)):
            return default
        return list.pop(self, index)

    def get(self, *args, **kwargs):
        """."""
        index, *args = args
        default = args[0] if args else None
        return list.__getitem__(self, index) if (-len(self) <= index < len(self)) else default

        
        


       
       


if __name__ == "__main__":

    def test():

        sequence = List(1, 2, 3)

        print(":", sequence[-4:])

        print("sequence:", sequence)
        print("first:", sequence[0])
        print("first:", sequence.get(0))

        print("last:", sequence[-1])
        print("last:", sequence.get(-1))

        print("bad:", sequence[3])
        print("bad:", sequence[-4])
        print("bad:", sequence.get(-4, False))

        ##sequence[0] = 10
        ##print("first:", sequence[0])

        ##print("popped:", sequence.pop(-4))
        ##print("sequence:", sequence)

        ##numbers = List(1, 2, 3, 4, 5, 6, 7)

    test()
