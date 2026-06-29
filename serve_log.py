from anvil.server import callable as server_function
from tools import connect


class log:
    def __init__(self):
        """."""

    def __call__(self):
        with connect("Running local server for logging."):

            @server_function
            def _log(*args) -> None:
                print(*args)


log = log()


if __name__ == "__main__":
    log()
