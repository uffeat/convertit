from anvil.server import HttpResponse



def Response(
    content_type: str, body: str, cors: bool | str = True, status: int = 200
) -> HttpResponse:
    """."""
    http_response = HttpResponse(status=status)
    http_response.headers["content-type"] = content_type
    http_response.body = body
    if cors:
        http_response.headers["access-control-allow-origin"] = (
            "*" if cors is True else cors
        )

    return http_response
