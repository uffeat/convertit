from tools import server


class access:

    def __call__(self):
        """Runs local server for granting access."""

        with server(self.__class__.__dict__["__call__"].__doc__):

            @server.function
            def _access() -> bool:
                return True


access = access()


if __name__ == "__main__":
    access()
