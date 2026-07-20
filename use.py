from tools import file, server



class use:

    def __call__(self):
        with server(
            "Running local server for serving uncommitted raw parcels."
        ):

            @server.function
            def _use(path: str) -> str:
                """Returns code text from local disc."""
                return file(f"parcels{path}")
                


use = use()


if __name__ == "__main__":
    use()
