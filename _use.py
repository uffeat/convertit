from tools import file, server


def use(path: str) -> str:
    """Returns parcel code from local disc."""
    return file(f"use{path}")


if __name__ == "__main__":
    with server("Running local server for serving uncommitted raw parcels."):

        @server.function
        def _use(path: str) -> str:
            print("path:", path)  ##
            return use(path)
