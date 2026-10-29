class List(list):
    def __init__(self, *args, **kwargs):
        """."""
        self.append(*args)

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.get(index)
        if isinstance(index, slice):
            slices = (index.start, index.stop, index.step,)
            if all([s is None or isinstance(s, int) for s in slices]):
                return self.slice(*slices)

           
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
        defaults = [-1, None]
        index, default = [*args, *defaults[len(args) :]]
        return list.pop(self, index) if (-len(self) <= index < len(self)) else default

    def get(self, *args, **kwargs):
        """."""
        defaults = [-1, None]
        index, default = [*args, *defaults[len(args) :]]
        return (
            list.__getitem__(self, index)
            if (-len(self) <= index < len(self))
            else default
        )

    def slice(self, *args, **kwargs):
        defaults = [None, None, None]
        slices = [*args, *defaults[len(args) :]]
        return list.__getitem__(self, slice(*slices))
        



if __name__ == "__main__":

    def test_get():

        data = List(1, 2, 3)


       
        print("data[0:1]:", data[0:1])
        print("data[0:1]:", data.slice(0, 1))



        

        print("data:", data)
        print("first:", data[0])
        print("first:", data.get(0))

        print("last:", data[-1])
       
        print("last:", data.get(-1))
        print("last:", data.get())

        print("over:", data[3])
        print("over:", data.get(3, False))
        print("under:", data[-4])
        print("under:", data.get(-4, False))

    test_get()
