from anvil import Media, URLMedia
from anvil.server import call
from ._meta import meta
from ._manifest import paths




class assets:
    """."""

    def __call__(self, path: str, raw=False, test=True):
        if meta.DEV and test:
            try:
                result = call("_assets", path, raw=raw)
                return result
            except:
                if path not in paths:
                    return

        result: Media = URLMedia(f"{meta.origin}/_/theme{path}")
        if raw:
            result: str = result.get_bytes().decode("utf-8").strip()
        return result


assets = assets()
