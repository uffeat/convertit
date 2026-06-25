import json
from pathlib import Path
from anvil import BlobMedia
from anvil.server import call, connect, disconnect
from create_bundle import bundle


UTF_8 = "utf-8"

def upload():
    bundle.upload()


if __name__ == "__main__":
    upload()
