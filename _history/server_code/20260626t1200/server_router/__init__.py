import json
from anvil import BlobMedia
from anvil.server import FormResponse
from ..server_tools import (
    Path,
    Response,
    api,
    encode,
    get_asset,
    get_asset_text,
    log,
    types,
)

UTF_8 = "utf-8"

config: dict = json.loads(get_asset_text("/config.json"))
pages: dict = config["pages"]


@api("/")
def router(
    path: Path,
    **query,
):

    # XXX TODO raw and test

    if path.file.type:
        # Serve non-page

        role = query.get("as")
        encoding = query.get("encoding")
        raw = query.get("raw")
        test = query.get("test")

        if path.path== '/ding.css':
            text = 'h2 { color: green; }'
            return BlobMedia("text/css", text.encode(UTF_8), name='ding.css')

        if role == "js":
            # Serve text-based asset as JS module with a single default item (Vite-style)
            text = get_asset_text(path.path, test=test)
            if encoding == 'base64':
                text = encode(text)
            body = f"export default `{text}`;"
            return Response(body=body, content_type="js", cors=True)

        if raw or role == "txt":
            # Serve text-based asset as text suitable for the fetch()-text() pattern.
            return Response(
                body=get_asset_text(path.path, test=test), content_type="txt", cors=True
            )

        if path.file.type == "html" and len(path.file.types) > 1:
            # Serve text-based asset wrapped as html
            # HACK Enables exploitation of Anvil's fast html import in client-code.
            content_type = types.get(path.file.types[0], "text/plain")
            ##log("content_type:", content_type)  ##
            text = get_asset_text(path.path)
            return BlobMedia(content_type, text.encode(UTF_8), name=path.file.name)

        if path.file.type == "js":
            return Response(
                body=get_asset_text(path.path, test=test), content_type="js", cors=True
            )

        return get_asset(path.path)

    # Extract page
    page: str = path.parts[0] if path.parts else "main"

    if page in pages:
        # Get spec
        spec: dict = pages[page]
        redirect = spec.get("redirect")
        if redirect:
            # Serve html page
            return get_asset(redirect)
        # Serve form page
        return FormResponse(page, path=path.path, **query)
    else:
        ...
        # XXX TODO Serve error page
