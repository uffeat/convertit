def main(
    use: callable,
    path=None,
    test: bool = None,
    **kwargs,
) -> callable:

    ##import convertit.tools as tools

    count = dict(value=0)

    def ping(*args, **kwargs):
        result = f"{path} x {count['value']}"
        count["value"] += 1
        return result

    return ping
