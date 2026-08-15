def ping():
    return "PING.PY"


def main(
    use: callable, log=None, path: str = None, test: bool = None, ping=None, **kwargs
) -> callable:

    if test:
        log(f"Unbuilt version of {path}")

    return ping
