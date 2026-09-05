def main(use, *args, **kwargs):
    """."""
    from base64 import b64decode, b64encode
    from datetime import datetime, timezone
    import json
    from pathlib import Path
    from mimetypes import guess_type
    import traceback
    from jinja2 import Template
    from anvil import BlobMedia, Media, URLMedia, app, is_server_side
    from anvil.server import (
        HttpResponse,
        FormResponse,
        call,
        callable as server_function,
        context,
        request,
        route,
        session,
        get_app_origin,
    )

    UTF_8 = "utf-8"

    def client(*args, **kwargs):
        return FormResponse("client", *args, **kwargs)

    route("/")(client)
    route(f"/:_1_")(client)
    route(f"/:_1_/:_2_")(client)

    
