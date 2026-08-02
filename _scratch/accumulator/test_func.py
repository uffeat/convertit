from accumulator import Accumulator

accumulator = Accumulator(result=[])


@accumulator.compute
def compute(value, result: list = None):
    result.append(value)
    return result


@accumulator.add
def subtract(value, index, result, owner, *args, **kwargs):
    print("value:", value)
    print("index:", index)
    print("owner:", owner)
    return value - 1


@accumulator.add
def double(value, index, result, owner, *args, **kwargs):
    return 2 * value


@accumulator.final
def final(result):
    return tuple(result)



print("result:", accumulator(2))  # (2, 2, 4)
