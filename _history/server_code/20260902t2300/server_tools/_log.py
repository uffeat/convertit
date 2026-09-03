from anvil import app
from anvil.server import call


def log(*args) -> None:
    """Enables remote logging."""
    if app.environment.name == "development":
        try:
            call("_log", *args)
        except:
            pass
