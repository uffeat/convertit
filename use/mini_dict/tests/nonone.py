def test(MiniDict):
    """."""
    data = MiniDict(foo=8)
    print("data:", data)




if __name__ == "__main__":
    import pathlib, sys

    

    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.parent.resolve()))
    from use.mini_dict import MiniDict

    test(MiniDict)
