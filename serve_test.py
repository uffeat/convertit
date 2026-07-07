from pathlib import Path
from anvil.server import callable as server_function
from tools import connect

SOURCE = Path.cwd()
UTF_8 = "utf-8"


class test:
    

    def __call__(self):
        with connect("Running local server for serving tests."):

            @server_function
            def _test(path: str) -> str:
                """Returns code text from local disc."""
                ##print("path:", path)  ##
                file = SOURCE / path[1:]
                result = file.read_text(encoding=UTF_8).strip()
                ##print("result:", result)  ##
                return result


test = test()


if __name__ == "__main__":
    test()
