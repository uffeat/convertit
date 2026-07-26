def main(use: callable, path: str=None, test: bool=None, **kwargs) -> callable:
    

    if test:
        print(f'Unbuilt version of {path}')

    def ping():
        return "PING.PY"

    return ping
