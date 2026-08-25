def main(
    use: callable,
    log=None,
    meta=None,
    path: str = None,
    session: callable = None,
    test: bool = None,
    **kwargs,
) -> callable:

    ##log("meta.DEV:", meta.DEV)

    pong = use("use/pong.py").pong
    ##pong = use("use/pong.py")
    log("pong:", pong())

    if test:
        log(f"Unbuilt version of {path}")

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"{path} x {count['value']}"
        count["value"] += 1
        return result

    def load(session):
        log("session:", session)

        return ping

    return load
