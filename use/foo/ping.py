def main(
    use: callable,
    log: callable,
    path=None,
    test: bool = None,
    **kwargs,
) -> callable:

    if test:
        log('Using uncommitted version of', path.full)

    meta = use('tools/meta.py')
    log('meta.DEV:', meta.DEV)

    

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"{path} x {count['value']}"
        count["value"] += 1
        return result

    return ping
