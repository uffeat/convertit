def main(
    use,
    Base: type = None,
    log: callable = None,
    path: str = None,
    **kwargs,
) -> None:
    """."""
    from base64 import b64decode, b64encode
    from datetime import datetime, timezone
    import json
    import pathlib
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

    from tools import Log

    Path = use("use/path/path.py")

    UTF_8 = "utf-8"

    ##log("Setting up routes...")  ##

    def is_part(key: str):
        if key.startswith("_") and key.endswith("_") and len(key) > 2:
            return key[1:-1].isnumeric()

    class Router(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(*args, **kwargs):
            ##log("router got kwargs:", kwargs)  ##
            parts = [v for k, v in kwargs.items() if is_part(k)]
            ##log("parts:", parts)  ##
            specifier = "/" + "/".join(parts)
            ##log("specifier:", specifier)  ##
            path = Path(specifier)
            ##log("path:", repr(path))  ##
            query = {k: v for k, v in kwargs.items() if not is_part(k)}
            ##log("query:", query)  ##
            if path.file:
                ...
            else:
                return FormResponse("client", path=dict(**path), query=query)


    router = Router()

    def setup(handler: callable, depth=5):
        route("/")(handler)
        for i in range(depth):
            signature = ''.join([f'/:_{j}_' for j in range(i+1)])
            route(signature)(handler)

    setup(router)
            




    
