from tools import file, server


def test(path: str) -> str:
    """Returns test code from local disc."""
    return file(path)


if __name__ == "__main__":
    with server("Running local server for serving tests."):
        server.function('_test')(test)
        
