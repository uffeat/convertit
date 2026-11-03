from pathlib import Path
import sys
# Insert path to enable super imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.resolve()))



from tools import use

##from _scratch.error import error



Dictionary = use("_scratch/dictionary/dictionary.py")





if __name__ == "__main__":

    ##print("text:", use("_scratch/dictionary/dictionary.py", text=True))

    def run(*args, **kwargs):
        def run(test: callable):
            return test(*args, **kwargs)

        return run

    ##@run()
    def test():
        """Tests init and update."""

        data = Dictionary(foo=42)
        print("data:", data)

        class Sim:

            def __init__(self, **kwargs):
                self.__dict__.update(_=kwargs)

            def __getitem__(self, key):
                # Facilitate **-unpacking
                return self._.get(key)

            def keys(self):
                # Facilitate **-unpacking
                return self._.keys()

        data = Dictionary(Sim(a="A", b="B", c=None))
        data(Sim(d="D", b=None), foo=42)

        print("data:", data)

    ##@run()
    def test():
        """Tests at method."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)
        print("first key:", data.at(0))
        print("first key:", data.at(-3))
        print("last key:", data.at(2))
        print("last key:", data.at(-1))
        print("key at 3:", data.at(3))
        print("key at -4:", data.at(-4))

    ##@run()
    def test():
        """Tests get method."""

        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        print("first value:", data.get("a"))
        print("first value:", data.get([0]))

        print("last value:", data.get("c"))  # 3
        print("last value:", data.get([-1]))

        print("missing value:", data.get("d", False))
        print("missing value:", data.get([3], False))

    ##@run()
    def test():
        """Tests slicing features."""

        data = Dictionary(a=1, b=2, c=3, d=4)
        print("data:", data)

        print("first slice:", data[0:1])
        print("first slice:", data.slice(0, 1, 1, 1, 1, 1))

        print("reversed:", data.slice(None, None, -1))

        print("every second:", data.slice(0, 4, 2))

        ##print("data[3:10]:", data[3:10])
        ##print("data[-4:10]:", data[-4:10])

    ##@run()
    def test():
        """Tests index method."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)
        print("index of a:", data.index("a"))
        print("index of c:", data.index("c"))
        print("index of e:", data.index("e", "missing"))

    ##@run()
    def test():
        """Tests transform."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        @data.transform
        def transform(index, key, value):
            if isinstance(value, int):
                return 2 * value
            return value

        print("data:", data)

        @data.transform(42, foo=42)
        class transform:
            def __init__(self, owner, *args, **kwargs):
                """."""
                print("owner:", owner)  ##
                print("args:", args)  ##
                print("kwargs:", kwargs)  ##

            def __call__(self, index, key, value):
                if isinstance(value, int):
                    return value + 2
                return value

        print("data:", data)

    ##@run()
    def test():
        """Tests find."""
        data = Dictionary(a=1, b=2, c=3)
        print("data:", data)

        # Decorated function
        @data.find
        def find(index, key, value):
            if index == 2:
                return 2 * value

        print("found:", find())

        # Decorated class
        @data.find()
        class find:
            def __init__(self, owner, *args, **kwargs):
                self._.update(owner=owner)

            @property
            def _(self) -> dict:
                return self.__dict__.setdefault("__", {})

            def __getattr__(self, key: str):
                if key not in self._:
                    raise AttributeError(key)
                return self._[key]

            def __call__(self, index, key, value):
                if index == 0:
                    return {key: value}, str(self.owner)

        print("found:", find())

        # External class
        class find:
            def __init__(self, owner, *args, **kwargs):
                self._.update(owner=owner, foo=kwargs.pop("foo", None))

            @property
            def _(self) -> dict:
                return self.__dict__.setdefault("__", {})

            def __getattr__(self, key: str):
                if key not in self._:
                    raise AttributeError(key)
                return self._[key]

            def __call__(self, index, key, value):
                return self.owner.get("a"), self.foo

        print("found:", data.find(find, foo=42)())

        # External function
        def find(index, key, value):
            if index == 2:
                return index, key, value

        print("found:", data.find(find)())

    @run()
    def test():
        """Tests pop."""

        data = Dictionary(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=9, i=10)
        print("data:", data)

        popped = data.pop([-1])
        print("popped:", popped)
        print("data:", data)

        popped = data.pop([20], 42)
        print("popped:", popped)
        print("data:", data)

        popped = data.pop("b")
        print("popped:", popped)
        print("data:", data)

        data["c"] = None
        print("data:", data)

        data.update(e=None)
        print("data:", data)

        data(d=None, f=None)
        print("data:", data)

    ##@run()
    def test():

        data = Dictionary(foo=42)

        print("foo:", data("foo"))
        print("bar:", data("bar", 8))
        print("data:", data)
        print("bar:", data("bar", "BAR", True))
        print("data:", data)

        _data = Dictionary.create(data)

        Dictionary.create()

        data(bar="new bar")

        print("_data:", _data)

        data = Dictionary(foo=42, bad=None, stuff=7)
        data(boom="BOOM")
        data(boom=None, bar="BAR")
        data.clear("stuff")
        data(dict(ping="PING"), dict(pong="PONG"))
        data["ding"] = "DING"
        data[(1, 2, 3)] = True

        print("data:", data)

        ##print("foo:", data['foo'])

        ##print("index of foo:", data.index("foo"))
        print("index of bar:", data.index("bar"))
        ##print("index of bad:", data.index("bad"))

        ##print("key at 0:", data.at(0))
        ##print("key at 1:", data.at(1))
        print("key at 2:", data.at(2))
        print("key at 10:", data.at(10))

        ##print("key at -1:", data.at(-1))
        ##print("key at -2:", data.at(-2))
        print("key at -3:", data.at(-3))

        ##print('data[0:1]:', data[0:1])
        ##print('data[0:2]:', data[0:2])
        ##print('data[0:4]:', data[0:4])
        print("data[3:10]:", data[3:10])
        print("data[1:-1]:", data[1:-1])

        @data.transform
        def transform(index, key, value, **kwargs):
            if isinstance(value, str):
                return value.lower()
            return value

        @data.transform(test=42)
        class transform:
            def __init__(self, owner, **kwargs):
                """."""
                ##print("kwargs:", kwargs)##

            def __call__(self, index, key, value):
                if key == "pong":
                    return
                return value

        transform()

        ##print("data:", data)

        ##data.clear()

        print("data:", data)

        class Sim:

            def __init__(self, **kwargs):
                self.__dict__.update(_=kwargs)

            def __getitem__(self, key):
                # Facilitate **-unpacking
                return self._.get(key)

            def keys(self):
                # Facilitate **-unpacking
                return self._.keys()

        data(Sim(a="A", b="B"))

        data.pop([-2])

        print("data.id:", data.id)
        print("data:", data)

        print("'a' in data:", "a" in data)
        print("'b' in data:", "b" in data)

        data[None] = True  ###

        print("data:", data)

        @data.find()
        def find(index, key, value):
            if index == 0:
                return {key: value}

        found = find()
        print("found:", found)

        @data.find()
        class find:
            def __init__(self, owner, **kwargs):
                """."""
                ##print("kwargs:", kwargs)##

            def __call__(self, index, key, value):
                if index == 0:
                    return {key: value}

        found = find()
        print("found:", found)
