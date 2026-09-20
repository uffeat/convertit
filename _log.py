from tools import server


def _log(*args) -> None:
    try:
        print(*args)
    except:
        return print("Could not not print.")


if __name__ == "__main__":
    with server("Running local server for logging."):
        server.function("_log", _log)
