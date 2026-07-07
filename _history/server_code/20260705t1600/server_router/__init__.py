from base64 import b64decode, b64encode
import json
from anvil import BlobMedia
from anvil.server import FormResponse, call
from ..server_tools import (
    Path,
    Response,
    api,
    get_asset,
    get_asset_text,
    log,
    meta,
)
from ._manifest import paths

UTF_8 = "utf-8"

config: dict = json.loads(get_asset_text("/config.json"))
pages: dict = config["pages"]




@api("/")
def router(
    path: Path,
    **query,
):
    """Serves pages and assets."""
    if path.file.type:
        # Serve non-page
        encoding = query.get("encoding")
        test = query.get("test")

        if query.get("raw"):
            # Serve text-based asset as text suitable for the fetch()-text() pattern.
            if path.path in paths:
                text = get_asset_text(path.path, test=test)
            else:
                text = get_asset_text('/error/error.txt')
            return Response("text/plain", text)

        if query.get("role") == "js":
            # Serve text-based asset as JS module with a single default item (Vite-style)
            if path.path in paths:
                text = get_asset_text(path.path, test=test)
                if encoding == "base64":
                    text = b64encode(text.encode(UTF_8)).decode(UTF_8)
                text = f"export default `{text}`;"
            else:
                text = get_asset_text('/error/error.js')
            return Response("text/javascript", text, cors=True)

        if path.file.type == "css":
            content = query.get("content")
            if content:
                # Enable link-based sheet import without underlying css file
                if encoding == "base64":
                    content: str = b64decode(content).decode(UTF_8)
                ##log("content:", content)  ##
                return BlobMedia("text/css", content.encode(UTF_8), name=path.file.name)
            if path.path not in paths:
                return get_asset('/error/error.css')
            if meta.DEV and path.path != "/use.css":
                try:
                    # NOTE Local server delivers live compilation of /main.css
                    sheet: BlobMedia = call("_sheet", path.path)
                    ##log("sheet:", sheet)  ##
                    if sheet:
                        return sheet
                except:
                    pass
            return get_asset(path.path)

        if path.file.type == "js":
            if path.path in paths:
                ##text = f"export const error = `{path.path}`;"
                text = get_asset_text(path.path, test=test)
            else:
                text = get_asset_text('/error/error.js')
            return Response("text/javascript", text)
        
        if path.file.type == "json":
            if path.path not in paths:
                return get_asset('/error/error.json')
        
        if path.file.type == "svg":
            if path.path not in paths:
                return get_asset('/error/error.svg')


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
