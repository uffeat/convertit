from tools import file, server



def use(path: str) -> str:
    """Returns parcel code from local disc."""
    return file(f"parcels{path}")



if __name__ == "__main__":
    with server(
            "Running local server for serving uncommitted raw parcels."
        ):

        @server.function
        def _use(path: str) -> str:
            return use(path)

