from tools import file, server


class test:
    

    def __call__(self):
        with server("Running local server for serving tests."):

            @server.function
            def _test(path: str) -> str:
                """Returns code text from local disc."""
                return file(path)


test = test()


if __name__ == "__main__":
    test()
