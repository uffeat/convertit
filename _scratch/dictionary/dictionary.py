class Dictionary(dict):
    def __call__(self, *args, **kwargs) -> "Dictionary":
        self.update(*args, **kwargs)
        return self

    def __getitem__(self, key):
        if isinstance(key, slice):
            return
        return dict.__getitem__(self, key)

    def index(self, key):
        if key in self:
            for i, k in enumerate(self.keys()):
                if key == k:
                    return i

    def at(self, index: int) -> tuple:

        # XXX TODO Handle negative


        for i, item in enumerate(self.items()):
            if index == i:
                return item
        return (None, None)


data = Dictionary(foo="FOO", bar="BAR")
data(ding="DING")

print("index:", data.index("ding"))

for n in [1, 2]:
    data[n] = n

print("1:", data[1])

print("data:", data)

print("foo:", data.get("foo"))

print("at 1:", data.at(1))
