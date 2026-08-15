def main(
    use: callable, log=None, path: str = None, test: bool = None, **kwargs
) -> callable:

    print("globals()", globals())  ##

    if test:
        log("Unbuilt")
        print(f"Unbuilt version of {path}")

    
    def ping():
        return "PING.PY"

    
    return ping
