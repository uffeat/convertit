from accumulator import Accumulator

accumulator = Accumulator()





@accumulator.add
def name(value, index, result, owner, *args, **kwargs):
    return dict(name='Uffe')


@accumulator.add
def score(value, index, result, owner, *args, **kwargs):
    return dict(score=100)


print("result:", accumulator())
