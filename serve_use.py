from pathlib import Path
from anvil.server import callable as server_function
from tools import connect

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class use:

    def __call__(self):
        """."""
        with connect(
            "Running local server for serving uncommitted raw parcels."
        ):

            @server_function
            def _use(path: str) -> str:
                """Returns code text from local disc."""
                ##print("path:", path)  ##
                file = SOURCE / path[1:]
                result = file.read_text(encoding=UTF_8).strip()
                ##print("result:", result)  ##
                return result


use = use()


if __name__ == "__main__":
    use()
