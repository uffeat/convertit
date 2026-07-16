import json

def main(anvil=None):
    """."""
    BlobMedia = anvil.anvil.BlobMedia
    call = anvil.server.call


    def get_bundle():
        """."""
        response: dict = call("_get_file", "bundle.json")
        bundle= response.get("result")
        print("Downloaded", bundle.name)
        return bundle
    