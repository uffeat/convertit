
args = tuple([0, 1, 2, dict, 3, dict])
args = list(args)
predicate = lambda i, v: v is dict
result = next(iter([args.pop(i) for i, v in enumerate(args) if all([predicate(i, v)])]), None)
print("args:", args)
print("result:", result)


