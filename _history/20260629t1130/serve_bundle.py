import json
from mimetypes import guess_type
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.server import callable as server_function
from anvil.tables import app_tables
from tools import connect

PARCELS = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class server:
    def __init__(self):
        """."""
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self):
        """."""
        with connect("Running local server for uploading bundle."):

            @server_function
            def _upload_bundle(bundle: BlobMedia) -> dict:
                """Saves bundle to db."""
                try:
                    app_tables.use.get(key="files").update(bundle=bundle)
                    return dict(ok=True)
                except:
                    return dict(ok=False, error=traceback.format_exc())


server = server()


if __name__ == "__main__":
    server()
