from tools import Blob, file, server


def _asset(path: str):
    ##print("path:", path)  ##
    text = file(f"assets/{path}")
    blob = Blob(path, text)
    return blob


if __name__ == "__main__":
    with server("Running local server for serving assets."):
        server.function('_asset', _asset)
        
        
