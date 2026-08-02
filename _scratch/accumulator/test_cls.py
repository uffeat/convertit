from accumulator import Accumulator

accumulator = Accumulator()


@accumulator.compute
class cls:
    def __init__(self, owner: type = None):
        ##print("accumulator owner:", owner)  ##
        self.__dict__.update(__={})
        self._.update(_result=[])

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self, value, **kwargs):
        result: list = self._["_result"]
        result.append(value)
        return tuple(result)


@accumulator.add
class cls:
    def __call__(self, value, index, result, owner, *args, **kwargs):
        print("value:", value)
        print("index:", index)
        print("result:", result)
        print("owner:", owner)
        return value - 1


@accumulator.add
class cls:
    def __call__(self, value, index, result, owner, *args, **kwargs):
        print("result:", result)
        return 2 * value


print("result:", accumulator(2))  # (2, 2, 4)
