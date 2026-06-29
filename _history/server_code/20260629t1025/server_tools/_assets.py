from anvil import BlobMedia
from tools import get_asset as _get_asset, get_asset_text as _get_asset_text


def get_asset(path: str) -> BlobMedia:
    """Returns asset as blob."""
    return _get_asset(path)


def get_asset_text(path: str, test=False) -> str:
    """Returns asset as text."""
    return _get_asset_text(path, test=test)
