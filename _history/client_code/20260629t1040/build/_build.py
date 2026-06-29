from datetime import datetime, timezone
import json
from anvil import BlobMedia, HtmlTemplate
from anvil.server import call
from anvil.tables import app_tables
from anvil.js.window import btoa
from ..tools import Path

UTF_8 = "utf-8"


def main():
    """."""
    # Get bundle
    bundle: BlobMedia = app_tables.use.get(key="files")["bundle"]
    print("Got bundle from db.")
    # Unpack bundle
    bundle: dict = json.loads(bundle.get_bytes().decode(UTF_8))
    #  Parse bundle
    use_rules, main_styles = [], []
    for path, text in bundle.items():
        path = Path(path)
        # XXX text can be manipulated here
        use_rules.append(f'[__path__="{path.path}"] {{\n  --__use__: "{btoa(text)}";}}')
        # NOTE sheets with same-parcel name are made global (aligns with Vite's lib mode)
        if path.file.type == "css" and len(path) > 1 and path.parts[-2] == path.file.stem:
            main_styles.append(text)


    def upload(sheet: BlobMedia):
        """."""
        try:
            response: dict = call("_upload_sheet", sheet)
        except Exception as error:
            print(f"Sheet not uploaded. Error: {str(error)}")
        else:
            if response.get("ok"):
                print("Sheet uploaded.")
            else:
                print(f"Sheet upload failed. Error: {response.get('error')}")


    # Create and upload use.css
    text = "\n".join(use_rules)
    upload(BlobMedia("text/css", text.encode(UTF_8), name="use.css"))
    # Create and upload upload(BlobMedia("text/css", text.encode(UTF_8), name="main.css"))
    text = "\n".join(main_styles)
    upload(BlobMedia("text/css", text.encode(UTF_8), name="main.css"))




class build(HtmlTemplate):
    def __init__(self, path: str = None, **query):
        """."""
        main()
