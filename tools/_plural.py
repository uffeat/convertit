def plural(count: int) -> str:
    if not isinstance(count, int):
        count = len(count)
    return '' if count == 1 else 's'

