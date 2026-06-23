import json
from pathlib import Path
from anvil import BlobMedia
from anvil.server import call, connect, disconnect

SOURCE = Path.cwd() / "bundle.json"
UTF_8 = "utf-8"


class upload:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self) -> None:
        """Uploads bundle."""
        name = "bundle.json"
        text = (Path.cwd() / name).read_text(UTF_8)
        bundle = BlobMedia("application/json", text.encode(UTF_8), name=name)
        ##print("bundle:", bundle)  ##
        connect(
            (json.loads((Path.cwd() / "secrets.json").read_text(encoding=UTF_8)))[
                "development"
            ]["client"]
        )
        try:
            response: dict = call("_upload_bundle", bundle)
        except Exception as error:
            print(f"Bundle NOT uploaded. Error: {str(error)}")
        else:
            if response.get('ok'):
                print("Bundle uploaded.")
            else:
                message = f"Bundle upload failed. Message: {response.get('error')}"
                raise ValueError(message)
                

        


upload = upload()


if __name__ == "__main__":
    upload()
