from anvil.server import call
from tools import meta


def access() -> bool:
    """Returns access flag."""
    if meta.DEV:
        try:
            return call("_access")
        except:
            pass
    return False
