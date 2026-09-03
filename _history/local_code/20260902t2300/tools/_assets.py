from pathlib import Path

UTF_8 = "utf-8"


def assets(path: str, text: str) -> None:
    """Writes file to disc."""
    if path.startswith("/"):
        path = path[1:]
    file: Path = Path.cwd() / "theme/assets" / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(text, encoding=UTF_8)
    print(f"Created '{path}'.")
