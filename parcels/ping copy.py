def main(
    use: callable, path: str = None, test: bool = None, export=None, **kwargs
) -> callable:

    print("globals()", globals())  ##

    if test:
        print(f"Unbuilt version of {path}")

    @export
    ##@export('ping')
    def ping():
        return "PING.PY"

    ##export(ping)
    ##export(ping=ping)

    ##return ping
