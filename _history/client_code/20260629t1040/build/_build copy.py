from datetime import datetime, timezone
import json
from anvil import BlobMedia, Spacer
from anvil.server import call
from anvil.tables import app_tables
from anvil.js import ProxyType, import_from, new
from anvil.js.window import CSSStyleSheet, Reflect, atob, btoa, console, globalThis
from ..tools import Base, Path, meta

UTF_8 = "utf-8"


# Get bundle
try:
    bundle: BlobMedia = call("_get_file", "bundle.json")
    print("Got bundle from disc.")
except Exception as error:
    bundle: BlobMedia = app_tables.use.get(key="files")["bundle"]
    print("Got bundle from db.")
# Unpack bundle
bundle: dict = json.loads(bundle.get_bytes().decode(UTF_8))
#  Parse bundle
rules, styles = [], []
for path, text in bundle.items():
    path = Path(path)
    # XXX text can be manipulated here
    rules.append(f'[__path__="{path.path}"] {{\n  --__use__: "{btoa(text)}";}}')
    # NOTE sheets with same-parcel name are made global (aligns with Vite's lib mode)
    if path.file.type == "css" and len(path) > 1 and path.parts[-2] == path.file.stem:
        styles.append(text)
# Create main sheet
# NOTE Style rules after code rules -> easier to read
rules.extend(styles)
text = "\n".join([r for r in rules])
sheet = BlobMedia("text/css", text.encode(UTF_8), name="use.css")
# Upload sheet
try:
    response: dict = call("_upload_sheet", sheet)
except Exception as error:
    print(f"Sheet not uploaded. Error: {str(error)}")
else:
    if response.get("ok"):
        print("Sheet uploaded.")
    else:
        print(f"Sheet upload failed. Error: {response.get('error')}")


# HACK Inherit from Spacer -> simplest component that allows server routing
class build(Spacer):
    def __init__(self, path: str = None, **query):
        """."""
