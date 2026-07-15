import traceback
from anvil import BlobMedia
from anvil.server import callable as server_function
from anvil.tables import app_tables
from ..server_tools import meta

if meta.DEV:

    UTF_8 = "utf-8"

    @server_function
    def _upload_bundle(bundle: BlobMedia) -> dict:
        """Saves bundle to db."""
        try:
            app_tables.use.get(key="files").update(bundle=bundle)
            return dict(ok=True)
        except:
            return dict(ok=False, error=traceback.format_exc())

    @server_function
    def _upload_sheet(sheet: BlobMedia) -> dict:
        """Saves sheet to disc and to db."""
        try:

            column, *_ = sheet.name.partition(".")
            app_tables.use.get(key="files").update(**{column: sheet})
            return dict(ok=True)
        except:
            return dict(ok=False, error=traceback.format_exc())
