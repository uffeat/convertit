def main(
    use: callable, log=None, path: str = None, test: bool = None, **kwargs
) -> callable:

    

    log("use.meta.DEV:", use.meta.DEV)

   

    pong = use("use/pong.py")
    log("pong:", pong)

    if test:
        log(f"Unbuilt version of {path.full}")

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"PING x {count['value']}"
        count["value"] += 1
        return result

    def load(*args, caller=None, session: int = None, **kwargs):
        log("caller:", caller)
        log("session:", session)
        return ping

    return load
