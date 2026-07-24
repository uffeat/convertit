from tools import server

from access import access
from bundle import bundle
from log import log
from sheet import sheet
from test import test
from use import use

sources = [
    access,
    bundle,
    log,
    sheet,
    test,
    use,
]


if __name__ == "__main__":
    with server("Running multi-purpose local server."):
        for source in sources:
            name = (
                f"_{source.__name__}"
                if hasattr(source, "__name__")
                else f"_{source.__class__.__name__}".lower()
            )
            print("name:", name)  ##
            server.function(name)(source)
