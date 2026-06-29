import json
from anvil.server import HttpResponse


types = dict(
    css="text/css",
    csv="text/csv",
    html="text/html",
    js="text/javascript",
    json="application/json",
    md="text/markdown",
    svg="image/svg+xml",
    txt="text/plain",
)


def Response(
    body=None, content_type: str = "", cors: bool = False, status: int = 200
) -> HttpResponse:
    """Returns http response with basic config."""
    http_response = HttpResponse(status=status)
    # Set CORS
    if cors:
        http_response.headers["access-control-allow-origin"] = (
            "*" if cors is True else cors
        )
    # Set content type
    if content_type:
        http_response.headers["content-type"] = types.get(content_type, content_type)
    if body:
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
        http_response.body = body
    return http_response
