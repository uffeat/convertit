from types import MappingProxyType
from accumulator import Accumulator

accumulator = Accumulator(result={})


@accumulator.compute
def compute(value, result: dict = None):
    if isinstance(value, dict):
        result.update(value)
        return result


@accumulator.add
def name(value, index, result, owner, *args, **kwargs):
    return dict(name='Uffe')


@accumulator.add
def score(value, index, result, owner, *args, **kwargs):
    return dict(score=100)

@accumulator.add
def year(value, index, result, owner, *args, **kwargs):
    return dict(year=1969)


@accumulator.final
def final(result):
    return MappingProxyType(result)


accumulator.remove(score)
accumulator.remove(0)




result = accumulator()
print("result:", result)

try:
    result['foo'] = 42
except TypeError as error:
    print(str(error))


