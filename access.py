from tools import server

# XXX Over-complicated on purpose to demo pattern


class Access:

    def __call__(self) -> bool:
        """Runs local server for granting access."""
        return True


access = Access()


if __name__ == "__main__":
    with server(access.__class__.__dict__["__call__"].__doc__):
        server.function("_access")(access)
