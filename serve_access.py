from anvil.server import callable as server_function
from tools import connect


class access:

    def __call__(self):
        """Runs local server for granting access."""

        doc = self.__class__.__dict__['__call__'].__doc__
        print(doc)


        with connect("Running local server for granting access."):

            @server_function
            def _access() -> bool:
                return True


access = access()


if __name__ == "__main__":
    access()
