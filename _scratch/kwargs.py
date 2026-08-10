def foo(*args, **kwargs):
    """."""
    options = {k: v for k, v in kwargs.items() if v is True}

    ##key = [k for k, v in kwargs.items() if v is True]
    ##key = key[0] if key else None

    key = next(iter([k for k, v in kwargs.items() if v is True]), "value")

    print("key:", key)


foo(text=True)
