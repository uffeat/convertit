def main(
    use: callable, log=None, meta=None, path: str = None, test: bool = None, **kwargs
) -> callable:

    

    log("meta.DEV:", meta.DEV)

   

    pong = use("use/pong.py").pong
    log("pong:", pong())

    if test:
        log(f"Unbuilt version of {path.full}")

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"PING x {count['value']}"
        count["value"] += 1
        return result

    def load(caller):
        log("caller:", caller)
        
        return ping

    return load
