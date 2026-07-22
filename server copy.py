from tools import server

from access import access
from bundle import bundle
from log import log
from sheet import sheet
from test import test
from use import use




if __name__ == "__main__":
    with server(
            "Running multi-purpose local server."
        ):

        server_functions = [
            access,
            bundle,
            log,
            sheet,
            test,
            use,
        ]

        for server_function in server_functions:
            if hasattr(server_function, '__name__'):
                name = f"_{server_function.__name__}"
            else:
                name = f"_{server_function.__class__.__name__}".lower()

            print('name:', name)

            server.function(name)(server_function)



        
