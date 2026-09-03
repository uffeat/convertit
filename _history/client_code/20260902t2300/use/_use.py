from ..log import Log
from ..document import document
from ..js import js
from ..tools import Base, Path, meta
from ..works import works
from  ..window import window
from ._registry import Registry




class Use(Base):
    def __init__(self):
        Base.__init__(
            self,
            _cache={},
            _public=dict(
                anvil=works,
                console=console,
                document=document,
                js=js,
                meta=meta,
                sources=Registry(owner=self),
                transpilers=Registry(owner=self),
                window=window,
            ),
        )

    def __call__(self, specifier: str, *args, **kwargs):
        """."""
        _cache: dict = self._["_cache"]
        path = Path(specifier)
        key = str(path)  # Full path
        # Get parcel
        if key in _cache:
            parcel = _cache[key]
        else:
            # Build parcel
            source = self.sources[path.source]
            if source:
                parcel: dict = source(path.path)
                transpile = self.transpilers[path.type]
                if transpile:
                    value = transpile(path=path.path, **parcel)
                    parcel.update(value=value)
                else:
                    value = parcel.pop("text")
                    parcel.update(value=value)
                _cache[key] = parcel
        # Deliver from parcel
        key = next(iter([k for k, v in kwargs.items() if v is True]), "value")
        return parcel.get(key)

    def __getattr__(self, key):
        """."""
        _public: dict = self._["_public"]
        return _public[key]

use = Use()



@use.sources("/")
class cls(Base):

    def __init__(self, owner=None):
        Base.__init__(self, owner=owner)

    def __call__(self, path: str) -> dict:
        """."""
        if meta.DEV:
            try:
                text = works.server.call("_use", path)
                parcel = dict(test=True, text=text)
                log(f"Got {path} from local server.")  ##
            except works.server.UplinkDisconnectedError as error:
                parcel = self._get(path)
                log(f"Got {path} from sheet.")  ##
        else:
            parcel = self._get(path)
        return parcel

    def _get(self, path: str) -> dict:
        """Returns uncached parcel from sheet."""
        node = document.createElement("div")
        node.setAttribute("__path__", path)
        document.head.append(node)
        value = (
            js.getComputedStyle(node)
            .getPropertyValue("--__use__")
            .strip()
        )
        if not value:
            raise ValueError(f"Invalid {path}.")
        node.remove()
        text = js.atob(value[1:-1])
        parcel = dict(node=node, text=text)
        return parcel

@use.transpilers("py")
class cls(Base):

    def __init__(self, owner=None):
        Base.__init__(self, owner=owner)

    def __call__(
        self, node=None, path: str = None, text: str = None, test: bool = None
    ):
        """Returns transpiled parcel."""
        locals = {}
        exec(text, {}, locals)
        main = locals.get("main")
        if main:

            log = Log(path=path)

            result = main(
                use,
                Base=Base,
                Path=Path,
                Log=Log,
                anvil=works,
                console=console,
                document=document,
                js=js,
                log=log,
                meta=meta,
                node=node,
                path=path,
                test=test,
                window=window,
            )

            if isinstance(result, tuple):
                result = {a.__name__: a for a in result}

            if isinstance(result, (dict, list)):
                result = js.freeze(result)

            return result

        else:
            result = js.freeze(locals)

        return result
