
data = [0, 1, 2, dict, 3, dict]
predicate = lambda i, v: v is dict
result = next(iter([data.pop(i) for i, v in enumerate(data) if all([predicate(i, v)])]), None)
print("cleaned:", data)
print("result:", result)


