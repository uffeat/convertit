from anvil.server import call
from anvil.js import import_from, new, window
import convertit as package
from ..tools import Base, Construct, Log, meta

document = window.document

_ = dict(meta=window.Object.freeze(dict(meta.meta)))


class use(Base):
    def __init__(self, *args, **kwargs):
        """."""
        Base.__init__(self, **kwargs)
        name = self.__class__.__name__
        node = document.createElement("div")
        node.id = name
        node.setAttribute(name, "")
        document.body.append(node)
        self._.update(_cache={}, name=name, node=node)

    def __call__(self, path: str, *args, **kwargs):
        """Returns result from import engine."""
        if path in self._cache:
            parcel = self._cache[path]
        else:
            node = document.createElement("div")
            node.setAttribute("__path__", path[len(self.name) :])
            self.node.append(node)
            parcel = dict(node=node, state=dict())
            if self.meta.DEV:
                try:
                    text = call(f"_{self.name}", path)
                    parcel.update(test=True)
                except:
                    text = self._get_text(node)
            else:
                text = self._get_text(node)
            parcel.update(text=text)
            if path.endswith(".js"):
                text = f"{text}\n//# sourceURL={path}"
                blob = new(window.Blob, [text], dict(type="text/javascript"))
                url = window.URL.createObjectURL(blob)
                module = import_from(url)
                window.URL.revokeObjectURL(url)
                value = module.default(self, dict(meta=_["meta"], path=path, **parcel))
                if value is not None:
                    parcel.update(default="value", value=value)
            elif path.endswith(".py"):
                value = Construct(text, use)(
                    Base=Base,
                    log=Log(path),
                    path=path,
                    **parcel,
                )
                if value is not None:
                    parcel.update(default="value", value=value)
            else:
                parcel.update(default="text")
            self._cache[path] = parcel

        key = parcel.get("default", "text")
        result = parcel.get(key)

        if (
            isinstance(result, dict)
            or window.Object.prototype.toString.call(result)[8:-1] == "Object"
        ):
            result = window.Object.freeze(result)
        return result

    def _get_text(self, node) -> str:
        """Returns uncached text from sheet."""
        value = (
            window.getComputedStyle(node).getPropertyValue(f"--__{self.name}__").strip()
        )
        text = window.atob(value[1:-1])
        return text


use = use(meta=meta.meta, package=package)
use = use("use/use/use.py")
