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
    get_asset = use("use/asset/asset.py")
    Query = use("use/query/query.py")

    UTF_8 = "utf-8"

    class Router(Base):
        def __init__(self, **kwargs):
            Base.__init__(self, **kwargs)

        def __call__(self, *args, **kwargs):
            try:
                path, query = self.parse(kwargs)
                ##log("path:", path)  ##
                if path.type:
                    result = get_asset(path.path)

                    if path.type == "js":
                        response = HttpResponse(
                            headers={"access-control-allow-origin": "*"}
                        )
                        if isinstance(result, Exception):
                            response.body = BlobMedia(
                                "text/javascript",
                                f'export const error = "{str(result)}";'.encode(UTF_8),
                                name="error.js",
                            )
                        else:
                            response.body = result
                        result = response
                    else:
                        if isinstance(result, Exception):
                            result = ''


                else:
                    result = FormResponse("client", path=dict(**path), query=query)

            except:

                result = traceback.format_exc()
            return result

        @staticmethod
        def is_part(key: str) -> bool | None:
            if key.startswith("_") and key.endswith("_") and len(key) > 2:
                return key[1:-1].isnumeric()

        def parse(self, kwargs: dict) -> tuple:
            parts = [v for k, v in kwargs.items() if self.is_part(k)]
            ##log("parts:", parts)  ##
            specifier = "/".join(parts)
            ##log("specifier:", specifier)  ##
            path = Path(specifier)
            ##log("path:", repr(path))  ##
            query = Query(**{k: v for k, v in kwargs.items() if not self.is_part(k)})
            return path, query

        def setup(self, depth=5):
            ##log("Setting up routes...")  ##
            route("/")(self)
            for i in range(depth):
                signature = "".join([f"/:_{j}_" for j in range(i + 1)])
                route(signature)(self)

    router = Router()

    router.setup()
