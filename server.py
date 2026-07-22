from tools import server

from access import access
from bundle import bundle
from log import log
from sheet import sheet
from test import test
from use import use

functions = [
    access,
    bundle,
    log,
    sheet,
    test,
    use,
]

server_functions = {f"_{f.__name__}" if hasattr(f, "__name__") else f"_{f.__class__.__name__}".lower(): f for f in functions}


print("server_functions:", server_functions)


if __name__ == "__main__":
    ...
