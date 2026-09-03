from anvil import app
from anvil.server import call



def access() -> bool:
    """Returns access flag."""
    if app.environment.name == "development":
        try:
            return call("_access")
        except:
            pass
    return False
