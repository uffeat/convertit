from anvil.server import call
import convertit as package
from tools import Base, Construct, Log, meta

log = Log("server")


class use(Base):
    def __init__(self, *args, **kwargs):
        Base.__init__(self, _cache={}, **kwargs)

    def __call__(self, path: str, *args, **kwargs):
        ##log("Using:", path)  ##
        if path in self._cache:
            parcel = self._cache[path]
        else:
            parcel = dict(state=dict())
            if self.meta.DEV:
                try:
                    text = call("_use", path)
                    parcel.update(test=True)
                except:
                    text = self._get_text(path)
            else:
                text = self._get_text(path)
            if isinstance(text, str):
                parcel.update(text=text)
                value = Construct(text, use)(
                    Base=Base,
                    log=Log(path),
                    path=path,
                    **parcel,
                )
                if value is not None:
                    parcel.update(value=value)
            self._cache[path] = parcel
        result = parcel.get(kwargs.get("key", "value"))
        if isinstance(result, dict):
            result = Base(**result)
        return result

    def _get_text(self, path: str) -> str:
        return ""  ##


use = use(meta=meta.meta, package=package)
use("server/router/router.py")
