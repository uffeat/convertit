def main(use, **kwargs):
    """."""
    from base64 import b64encode
    import json
    from anvil import BlobMedia
    from anvil.tables import app_tables
    from anvil.server import call

    UTF_8 = "utf-8"

    