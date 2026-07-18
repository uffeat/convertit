from pathlib import Path
import traceback
from anvil import BlobMedia
from anvil.tables import app_tables
from anvil.server import call, callable as server_function
from tools import connect
from bundle import bundle

SOURCE = Path.cwd() / "build"
UTF_8 = "utf-8"


class Build:
    

    def __call__(self):
        with connect("Running local server for building."):

            @server_function
            def _upload_file(file: BlobMedia, path: str=None) -> dict:
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
                    file = row.get('file')
                    if not file:
                        return dict(ok=False, message=f"File '{path}' not found.")
                    return dict(ok=True, result=file)
                except:
                    return dict(ok=False, error=traceback.format_exc())
                
            
            @server_function
            def _build(path: str) -> str:
                """Returns code text from local disc."""
                print("path:", path)  ##
                file = SOURCE / path[1:]
                result = file.read_text(encoding=UTF_8).strip()
                return result
            

            file = bundle()
            response: dict = call("_upload_file", file)
            if response.get("ok"):
                print("Bundle uploaded.")
            else:
                # Controlled error
                print(f"Bundle upload failed. Error: {response.get('error')}")


build = Build()


if __name__ == "__main__":
    build()
