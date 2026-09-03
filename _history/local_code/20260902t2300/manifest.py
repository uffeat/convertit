import json
from pathlib import Path
from anvil import BlobMedia

SOURCE = Path.cwd() / "theme/assets"
UTF_8 = "utf-8"


class build:
    def __init__(self):
        self.__dict__.update(__={})

    @property
    def _(self) -> dict:
        return self.__

    def __call__(self) -> None:
        """."""
        assets = {}
        for file in SOURCE.rglob("**/*.*"):
            if " " in file.stem:
                continue
            path = f"/{file.relative_to(SOURCE).as_posix()}"
            text = file.read_text(encoding=UTF_8).strip()
            assets[path] = text

        paths = list(assets.keys())
        code = f"paths = set({paths})"

        file: Path = Path.cwd() / "server_code/server_tools/_manifest.py"
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(code, encoding=UTF_8)

        print(f"Created manifest with {len(paths)} items.")


build = build()


if __name__ == "__main__":
    build()
