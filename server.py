import json
from pathlib import Path
from anvil import BlobMedia
from anvil.server import (
    callable as server_function,
    connect,
    disconnect,
    wait_forever,
)

UTF_8 = "utf-8"


def Bundle() -> BlobMedia:
    """."""
    name = "bundle.json"
    file = Path.cwd() / name
    content = file.read_text(encoding=UTF_8).strip()
    content = content.encode(UTF_8)
    return BlobMedia("application/json", content, name=name)


class Server:
    def __init__(self):
        """."""
        self.__dict__.update(__={})
        self._.update(bundle=Bundle())

    def __call__(self):
        """."""
        connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["server"]
        )

        @server_function
        def _bundle() -> BlobMedia:
            return self._["bundle"]

        @server_function
        def _log(*args) -> None:
            print(*args)

        print("Running local server.")

        # HACK Sometimes fails at first run
        try:
            wait_forever()
        except:
            wait_forever()

    @property
    def _(self) -> dict:
        return self.__


if __name__ == "__main__":
    Server()()
