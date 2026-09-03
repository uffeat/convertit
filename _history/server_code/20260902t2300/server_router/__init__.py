from base64 import b64decode, b64encode
import json
from anvil import BlobMedia
from anvil.server import FormResponse, call
from ..server_tools import (
    Path,
    Response,
    api,
    assets,
    log,
    meta,
)


UTF_8 = "utf-8"

config: dict = json.loads(assets("/config.json", raw=True))
pages: dict = config["pages"]


@api("/")
def router(
    path: Path,
    **query,
):
    """Serves pages and assets."""
    if path.file.type:
        # Serve non-page

        # Always serve use.css as-is
        if path.path == "/use.css":
            return assets(path.path)

        encoding = query.get("encoding")

        # Serve text-based asset as text suitable for the fetch()-text() pattern.
        if query.get("raw"):
            text = assets(path.path, raw=True)
            if not text:
                text = assets("/error/error.txt", raw=True)
            return Response("text/plain", text)

        # Serve text-based asset as JS module with a single default item (Vite-style)
        if query.get("role") == "js":
            text = assets(path.path, raw=True)
            if text:
                if encoding == "base64":
                    text = b64encode(text.encode(UTF_8)).decode(UTF_8)
                text = f"export default `{text}`;"
            else:
                text = assets("/error/error.js", raw=True)

            return Response("text/javascript", text, cors=True)

        if path.file.type == "css":
            # Enable link-based sheet import without underlying css file
            content = query.get("content")
            if content:
                if encoding == "base64":
                    content: str = b64decode(content).decode(UTF_8)
                ##log("content:", content)  ##
                return BlobMedia("text/css", content.encode(UTF_8), name=path.file.name)
            # Enable JIT compilation of /main.css by local server
            if meta.DEV:
                try:
                    asset: BlobMedia = call("_sheet", path.path)
                    ##log("asset:", asset)  ##
                    if asset:
                        return asset
                except:
                    pass
            asset = assets(path.path)
            if not asset:
                return assets("/error/error.css")
            return asset

        if path.file.type == "js":
            text = assets(path.path, raw=True)
            if not text:
                text = assets("/error/error.js", raw=True)
            return Response("text/javascript", text)

        if path.file.type == "json":
            asset = assets(path.path)
            if not asset:
                return assets("/error/error.json")
            return asset

        if path.file.type == "svg":
            asset = assets(path.path)
            if not asset:
                return assets("/error/error.svg")
            return asset

        return assets(path.path)

    # Extract page
    page: str = path.parts[0] if path.parts else "main"

    if page in pages:
        # Get spec
        spec: dict = pages[page]
        redirect = spec.get("redirect")
        if redirect:
            # Serve html page
            return assets(redirect)
        # Serve form page
        return FormResponse(page, path=path.path, **query)
    else:
        ...
        # XXX TODO Serve error page
