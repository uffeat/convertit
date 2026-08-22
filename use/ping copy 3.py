


def main(
    use: callable, log=None, path: str = None, test: bool = None, ping=None, **kwargs
) -> callable:

    if test:
        log(f"Unbuilt version of {path.full}")

    count = dict(value=0)

    def ping(*args, **kwargs) ->str:
        value = count['value']
        result = f"Ping count: {value}"
        return "PING"

    return ping
