def main(
    use: callable,
    log=None,
    meta=None,
    path: str = None,
    test: bool = None,
    **kwargs,
) -> callable:

    log("meta.DEV:", meta.DEV)

    
    if test:
        log(f"Unbuilt version of {path}")

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"{path} x {count['value']}"
        count["value"] += 1
        return result

    

    return ping
