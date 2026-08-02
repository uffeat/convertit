from pipe import Pipe

pipe = Pipe()


@pipe.add
class cls:
    def __call__(self, value, index, owner, *args, **kwargs):
        print("value:", value)
        print("index:", index)
        print("owner:", owner)
        return value


@pipe.add
class cls:
    def __call__(self, value, index, owner, *args, **kwargs):
        if isinstance(value, int):
            if value > 10:
                return False
            return 2 * value


print("result:", pipe(2))
print(" ")
print("result:", pipe(42))
