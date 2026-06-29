from anvil.server import call
from tools import meta

_ = dict()


def log(*args) -> None:
    """Enables remote logging."""
    if not meta.DEV or _.get("connects") is False:
        return

    if _.get("connects"):
        call("_log", *args)
        return

    try:
        call("_log", *args)
        _.update(connects=True)
    except:
        _.update(connects=False)
