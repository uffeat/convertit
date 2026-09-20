def main(use, Base: type = None, log: callable = None, **kwargs):
    """."""

    from anvil import BlobMedia, app
    from anvil.server import call

    get_asset = app.get_asset

    class Asset(Base):

        def __init__(self):
            Base.__init__(self)

        def __call__(self, path: str) -> BlobMedia:
            """."""
            if use.meta.DEV:
                try:
                    result: BlobMedia = call("_asset", path)
                except:
                    result = self.get_asset(path)
            else:
                result = self.get_asset(path)
            return result

        def get_asset(self, path: str) -> BlobMedia:
            blob: BlobMedia = get_asset(path)
            if "/" in path:
                blob = BlobMedia(blob.content_type, blob.get_bytes(), name=path)
            return blob

    asset = Asset()

    return asset
