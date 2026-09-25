from anvil.server import call
from .meta import meta


def Log(path=""):
    def log(*args, **kwargs):
        if meta.DEV:
            if path:
                args = [*args, f"\n(trace: {path})"]
            if meta.side("server"):

                def text(value):
                    if isinstance(value, (bool, float, int, str)):
                        return value
                    try:
                        return str(value)
                    except:
                        if hasattr(value, "__name__"):
                            return value.__name__
                        if hasattr(value, "__class__"):
                            return text(value.__class__)
                        return "ERROR"

                try:
                    call("_log", *[text(a) for a in args])
                except:
                    try:
                        print(*args)
                    except:
                        pass
            else:
                out = kwargs.get("out", print)
                out(*args)

    return log
