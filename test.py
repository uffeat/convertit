from tools import file, server


def test(path: str) -> str:
    return file(path)


if __name__ == "__main__":
    with server("Running local server for serving tests."):

        @server.function
        def _test(path: str) -> str:
            return file(path)
