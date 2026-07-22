from tools import server


def log(*args) -> None:
    try:
        print(*args)
    except:
        pass





if __name__ == "__main__":
    with server("Running local server for logging."):

        @server.function
        def _log(*args) -> str:
            log(*args)
            result = ' '.join([str(a) for a in args])
            return result
