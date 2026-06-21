import json
from pathlib import Path
from anvil import BlobMedia
from anvil.server import (
    call,
    connect,
)

SOURCE = Path.cwd() / "parcels"
UTF_8 = "utf-8"


class Bundle:
    def __init__(self):
        """."""
        self.__dict__.update(__={})
        self._.update(bundle={})

    def __call__(self) -> "Bundle":
        """."""
        for file in SOURCE.rglob("**/*.*"):
            if "test" in file.parts:
                continue
            key = f"/{file.relative_to(SOURCE).as_posix()}"
            value = file.read_text(encoding=UTF_8).strip()
            self._["bundle"][key] = value

        self._.update(text=json.dumps(self._["bundle"]))

        print(f'Bundled {len(self._["bundle"])} files.')

        return self

    @property
    def _(self) -> dict:
        return self.__

    def save(self) -> "Bundle":
        """."""
        file = Path.cwd() / "bundle.json"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(self._["bundle"]), encoding=UTF_8)
        return self
    
    def upload(self) -> "Bundle":
        """."""
        content = json.dumps(content)
        content = content.encode(UTF_8)
        blob = BlobMedia(content_type, content, name=name)
        
        return self


if __name__ == "__main__":
    Bundle()().save()
