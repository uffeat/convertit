import json
from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.server import call, callable as server_function
from anvil.tables import app_tables
from tools import connect, minify

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class bundle:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self) -> BlobMedia:
        """Creates and returns bundle."""

        bundle = {}

        for file in SOURCE.rglob("**/*.*"):
            if " " in file.name:
                continue
            if "history" in file.parts:
                continue
            if "scratch" in file.parts:
                continue
            if "test" in file.parts:
                continue
            path = f"/{file.relative_to(SOURCE).as_posix()}"
            text = file.read_text(encoding=UTF_8).strip()
            if not text:
                continue
            if file.suffix == ".css":
                text = minify.css(text)
            elif file.suffix == ".html":
                text = minify.html(text)
            bundle[path] = text

        print(f"Bundled {len(bundle)} files.")
        # Write bundle to disc
        text = json.dumps(bundle)
        file: Path = Path.cwd() / self.name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding=UTF_8)
        print("Bundle saved to local disc as:", self.name)
        bundle = self.create_blob(text)
        self.serve(bundle)
        return bundle

    @property
    def name(self):
        return "bundle.json"

    def create_blob(self, text: str) -> BlobMedia:
        return BlobMedia("application/json", text.encode(UTF_8), name=self.name)

    def serve(self, bundle: BlobMedia = None):
        """."""
        with connect("Running local server for building parcels."):
            # NOTE Allows skipping bundle recreation
            if not bundle:
                # Create bundle from disk
                text = (Path.cwd() / self.name).read_text(UTF_8)
                bundle = self.create_blob(text)

            @server_function
            def _upload_file(file: BlobMedia, path: str = None) -> dict:
                """Saves file to db."""
                try:
                    if not path:
                        path = file.name
                    row = app_tables.use.get(path=path)
                    if not row:
                        row = app_tables.use.add_row(path=path)
                    row.update(file=file)
                    return dict(ok=True)
                except:
                    return dict(ok=False, error=traceback.format_exc())

            @server_function
            def _get_file(path: str) -> dict:
                """Returns file from db."""
                try:
                    row = app_tables.use.get(path=path)
                    if not row:
                        return dict(ok=False, message=f"Row '{path}' not found.")
                    file = row.get("file")
                    if not file:
                        return dict(ok=False, message=f"File '{path}' not found.")
                    return dict(ok=True, result=file)
                except:
                    return dict(ok=False, error=traceback.format_exc())

            @server_function
            def _build() -> str:
                """."""
                file = Path.cwd() / "build.py"
                result = file.read_text(encoding=UTF_8).strip()
                return result

            response: dict = call("_upload_file", bundle)
            if response.get("ok"):
                print("Bundle uploaded.")
            else:
                # Controlled error
                print(f"Bundle upload failed. Error: {response.get('error')}")

    def upload(self, bundle: BlobMedia = None):
        # NOTE Allows upload without bundle recreation
        if not bundle:
            # Create bundle from disk
            text = (Path.cwd() / self.name).read_text(UTF_8)
            bundle = self.create_blob(text)

        try:
            connect("Connecting to upload bundle.", server=False)
        except Exception as error:
            print(f"Could not connect. Error: {str(error)}")
        else:
            try:
                response: dict = call("_upload_file", bundle)
            except Exception as error:
                # Uncontrolled error related to the server function
                print(f"Bundle not uploaded. Error: {str(error)}")
            else:
                if response.get("ok"):
                    print("Bundle uploaded.")
                else:
                    # Controlled error
                    print(f"Bundle upload failed. Error: {response.get('error')}")


bundle = bundle()


if __name__ == "__main__":
    bundle()
