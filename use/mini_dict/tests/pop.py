def main(use, *args, **kwargs):
    """."""
    MiniDict = use('use/mini_dict/mini_dict.py')
    data = MiniDict(foo=42, bar=8)
    print("data:", data)
    data(bar=None)
    print("data:", data)





