import json
from pathlib import Path
import sys
from anvil import BlobMedia
from anvil.tables import app_tables
from tools import assets, connect

sys.path.insert(0, str(Path(__file__).parent.parent.resolve()))
from client_code.tools import Base


UTF_8 = "utf-8"




class Build(Base):
    def __init__(self):
        super().__init__()

    def __call__(self) -> None:
        """Creates asset files."""
        connect("Uplink connection created for building.")
        
        table = getattr(app_tables, "use")
        
        # Create use.css
        row: dict = table.get(path="use.css")
        file: BlobMedia = row.get("file")
        text: str = file.get_bytes().decode(UTF_8)
        assets("use.css", text)

        # Create main.css
        row: dict = table.get(path="main.css")
        file: BlobMedia = row.get("file")
        text: str = file.get_bytes().decode(UTF_8)
        assets("main.css", text)

        
        # Create bundle.json
        row: dict = table.get(path="bundle.json")
        file: BlobMedia = row.get("file")
        text: str = file.get_bytes().decode(UTF_8)
        assets("bundle.json", text)
        
        # Create hyper-media files
        bundle: dict = json.loads(text)
        for path, text in bundle.items():
            path: str = path
            if path.endswith(".css") or path.endswith(".svg"):
                assets(path, text)

            


build = Build()


if __name__ == "__main__":
    build()
