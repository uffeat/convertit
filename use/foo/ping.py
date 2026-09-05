def main(
    use: callable,
    log: callable,
    path: str=None,
    test: bool = None,
    **kwargs,
) -> callable:

    if test:
        log('Using uncommitted version of', path)

   
    log('use.meta.DEV:', use.meta.DEV)

    

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"{path} x {count['value']}"
        count["value"] += 1
        return result

    return ping
