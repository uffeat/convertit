def main(
    use,
    *args,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> None:
    """."""
    from base64 import b64decode, b64encode
    from datetime import datetime, timezone
    import json
    ##from pathlib import Path
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

    from tools import Base, Log

    log("ping():", use("use/foo/ping.py")())
    log("ping():", use("use/foo/ping.py")())

    ##log("use:", use)  ##

    Path = use('use/path/path.py')

    test_path = Path('foo/foo.py')

    log("test_path:", dict(**test_path))  ##
    
    ##log("Path:", Path)  ##

    

    ##log("Log:", Log)  ##

    UTF_8 = "utf-8"

    ##log("Setting up routes...")  ##

    def is_part(key: str):
        if key.startswith("_") and key.endswith("_") and len(key) > 2:
            return key[1:-1].isnumeric()

    def client(*args, **kwargs):

        ##log("client route got kwargs:", kwargs)  ##

        parts = [v for k, v in kwargs.items() if is_part(k)]
        log("parts:", parts)  ##
        query = {k: v for k, v in kwargs.items() if not is_part(k)}
        log("query:", query)  ##

        return FormResponse("client", *args, **kwargs)

    route("/")(client)
    route(f"/:_1_")(client)
    route(f"/:_1_/:_2_")(client)
